"""Governance-aware Artifact Harness: execution, evaluation and mutation."""
import hashlib
import json
import time
import traceback
from dataclasses import dataclass, field, replace
from typing import Any, Callable

from .constraints import ConstraintLevel
from .tests import TestCase, TestResult
from ..governance import (
    AuditEvent, CRITERIA_FINGERPRINT_LIMITATIONS, GovernanceStatus,
    assert_no_offline_disguise, sha256_value,
)

def _identity(inputs, output, context):
    return 1.0 if output not in (None, "") else 0.0

def _callable_fingerprint(fn: Any) -> Any:
    if fn is None:
        return None
    code = getattr(fn, "__code__", None)
    if code is None:
        return {"type": type(fn).__qualname__, "repr": repr(fn)}
    return {
        "module": getattr(fn, "__module__", None),
        "name": getattr(fn, "__name__", None),
        "qualname": getattr(fn, "__qualname__", None),
        "bytecode": code.co_code.hex(),
        "constants": [repr(value) for value in code.co_consts],
        "defaults": repr(getattr(fn, "__defaults__", None)),
        "kwdefaults": repr(getattr(fn, "__kwdefaults__", None)),
    }

def criteria_fingerprint(evaluator=None, tests=None, criteria_spec=None) -> str:
    """Fingerprint evaluator structure, test structure and explicit criteria specification.

    This is a structural fingerprint, not a proof that all runtime dependencies are unchanged.
    """
    payload = {
        "evaluator": _callable_fingerprint(evaluator),
        "tests": [
            {"name": test.name, "predicate": _callable_fingerprint(test.predicate),
             "level": test.level.value, "message": test.message}
            for test in (tests or [])
        ],
        "criteria_spec": criteria_spec,
    }
    return sha256_value(payload)

@dataclass
class ExecutionResult:
    artifact: str
    version: int
    inputs: dict
    outputs: dict
    value: Any
    test_results: list[TestResult] = field(default_factory=list)
    duration_ms: float = 0.0
    error: str | None = None
    context: dict = field(default_factory=dict)

    @property
    def passed(self):
        return self.error is None and all(
            result.passed for result in self.test_results
            if result.level is ConstraintLevel.ASSERT
        )

@dataclass
class EvalRow:
    prompt: str
    output: Any
    score: float
    passed: bool
    error: str | None = None
    status: str = GovernanceStatus.INFERRED.value

@dataclass
class EvalRun:
    artifact: str
    version: int
    dataset: str
    rows: list[EvalRow] = field(default_factory=list)
    training_score: float | None = None
    validation_score: float | None = None

    @property
    def scores(self):
        return [row.score for row in self.rows]

    @property
    def mean_score(self):
        return sum(self.scores) / len(self.rows) if self.rows else 0.0

    @property
    def pass_rate(self):
        return sum(row.passed for row in self.rows) / len(self.rows) if self.rows else 0.0

@dataclass
class Artifact:
    name: str
    fn: Callable[..., Any]
    interface: str = "kwargs -> value"
    evaluator: Callable = _identity
    tests: list[TestCase] = field(default_factory=list)
    config: dict = field(default_factory=dict)
    provenance: dict = field(default_factory=dict)
    version: int = 1
    history: list[dict] = field(default_factory=list)
    criteria_spec: Any = None
    criteria_version: int = 1
    criteria_digest: str = ""
    mutation_audit: list[AuditEvent] = field(default_factory=list)

    def __post_init__(self):
        if not self.criteria_digest:
            self.criteria_digest = criteria_fingerprint(
                self.evaluator, self.tests, self.criteria_spec
            )

    def with_config(self, **overrides):
        if not overrides:
            return self
        return replace(
            self,
            config={**self.config, **overrides},
            version=self.version + 1,
            history=[*self.history, {"event": "config", "before": dict(self.config),
                                     "after": {**self.config, **overrides}}],
        )

    def with_criteria(self, evaluator=None, tests=None, criteria_spec=None, **config_overrides):
        next_evaluator = self.evaluator if evaluator is None else evaluator
        next_tests = self.tests if tests is None else list(tests)
        next_spec = self.criteria_spec if criteria_spec is None else criteria_spec
        next_digest = criteria_fingerprint(next_evaluator, next_tests, next_spec)
        updated = self.with_config(**config_overrides) if config_overrides else self
        if next_digest == self.criteria_digest:
            return updated
        event = AuditEvent(
            event_type="criteria_mutation", artifact_id=self.name,
            rationale="Criteria fingerprint changed",
            before={"criteria_fingerprint": self.criteria_digest,
                    "criteria_version": self.criteria_version},
            after={"criteria_fingerprint": next_digest,
                   "criteria_version": self.criteria_version + 1},
        )
        return replace(
            updated, evaluator=next_evaluator, tests=next_tests, criteria_spec=next_spec,
            criteria_digest=next_digest, criteria_version=self.criteria_version + 1,
            version=max(updated.version, self.version + 1),
            history=[*updated.history, {"event": "criteria", "before": self.criteria_digest,
                                        "after": next_digest}],
            mutation_audit=[*self.mutation_audit, event],
        )

    def to_dict(self):
        return {
            "name": self.name, "interface": self.interface, "version": self.version,
            "criteria_version": self.criteria_version,
            "criteria_fingerprint": self.criteria_digest,
            "config": self.config, "provenance": self.provenance,
            "criteria_spec": self.criteria_spec,
            "tests": [{"name": test.name, "level": test.level.value,
                       "message": test.message} for test in self.tests],
        }

class ArtifactHarness:
    def __init__(self, name="harness"):
        self.name = name
        self.log = []

    def create_code_artifact(self, name, fn, interface="kwargs -> value",
                             evaluator=None, tests=None, config=None, provenance=None,
                             criteria_spec=None):
        return Artifact(
            name=name, fn=fn, interface=interface, evaluator=evaluator or _identity,
            tests=list(tests or []), config=dict(config or {}),
            provenance=dict(provenance or {}), criteria_spec=criteria_spec,
        )

    def execute(self, artifact, inputs=None, context=None):
        supplied = dict(inputs or {})
        execution_context = dict(context or {})
        clean_inputs = {}
        for key, value in supplied.items():
            if key.startswith("_boundary"):
                execution_context[key] = value
            else:
                clean_inputs[key] = value
        merged = {**artifact.config, **clean_inputs}
        start = time.perf_counter()
        value = None
        error = None
        try:
            value = artifact.fn(**merged)
        except Exception:
            error = traceback.format_exc(limit=3)
        duration = (time.perf_counter() - start) * 1000
        tests = [test.run(value) for test in artifact.tests] if error is None else []
        result = ExecutionResult(
            artifact.name, artifact.version, merged, {"output": value}, value,
            tests, duration, error, execution_context,
        )
        self.log.append({
            "event": "execute", "artifact": artifact.name, "version": artifact.version,
            "passed": result.passed, "duration_ms": round(duration, 2),
        })
        return result

    def evaluate(self, artifact, dataset, max_samples=None):
        from .dataset import EvalDataset
        boundary = getattr(dataset, "boundary", None)
        assert_no_offline_disguise(boundary)
        run = EvalRun(artifact.name, artifact.version, dataset.name)
        cases = dataset.cases if max_samples is None else dataset.cases[:max_samples]
        for case in cases:
            result = self.execute(
                artifact, {"prompt": case.prompt, **case.metadata},
                context={"_boundary": boundary} if boundary is not None else {},
            )
            if result.error or not result.passed:
                run.rows.append(EvalRow(
                    case.prompt, result.value, 0.0, False,
                    (result.error or "test failure").strip().splitlines()[-1],
                    GovernanceStatus.INCOMPLETE.value if result.error else GovernanceStatus.INFERRED.value,
                ))
                continue
            try:
                score = max(0.0, min(1.0, float(artifact.evaluator(
                    result.inputs, result.value,
                    {"duration_ms": result.duration_ms, "config": artifact.config,
                     "context": result.context, "boundary": boundary},
                ))))
            except Exception as exc:
                run.rows.append(EvalRow(
                    case.prompt, result.value, 0.0, False, str(exc),
                    GovernanceStatus.INCOMPLETE.value,
                ))
                continue
            run.rows.append(EvalRow(
                case.prompt, result.value, score, True, None,
                GovernanceStatus.INFERRED.value,
            ))
        self.log.append({
            "event": "evaluate", "artifact": artifact.name, "dataset": dataset.name,
            "mean_score": run.mean_score, "pass_rate": run.pass_rate,
        })
        return run

    def critique(self, run, samples=3):
        failures = [row for row in run.rows if not row.passed]
        ranked = sorted(run.rows, key=lambda row: row.score)
        return {
            "artifact": run.artifact, "version": run.version, "dataset": run.dataset,
            "mean_score": run.mean_score, "pass_rate": run.pass_rate,
            "failure_count": len(failures),
            "failure_reasons": sorted({row.error or "unknown" for row in failures}),
            "weakest_samples": [
                {"prompt": row.prompt, "score": row.score, "output": str(row.output)[:400]}
                for row in ranked[:samples]
            ],
        }

    def default_mutator(self, artifact, critique):
        config = dict(artifact.config)
        low = critique.get("mean_score", 0) < 0.6
        config["temperature"] = round(min(1.2, config.get("temperature", 0.9)
                                          + (0.05 if low else -0.05)), 3)
        config["top_p"] = round(min(0.99, max(0.7, config.get("top_p", 0.95)
                                              + (0.02 if low else -0.02))), 3)
        if low:
            config["max_length"] = int(config.get("max_length", 256) * 1.25)
        return artifact.with_config(**config)

    def optimize(self, artifact, train_data, mutator=None, rounds=3, validation_data=None):
        mutate = mutator or self.default_mutator
        validation = train_data if validation_data is None else validation_data
        best = artifact
        best_run = self.evaluate(artifact, validation)
        current = artifact
        for index in range(rounds):
            train_run = self.evaluate(current, train_data)
            candidate = mutate(current, self.critique(train_run))
            before_criteria = criteria_fingerprint(
                current.evaluator, current.tests, current.criteria_spec
            )
            after_criteria = criteria_fingerprint(
                candidate.evaluator, candidate.tests, candidate.criteria_spec
            )
            criteria_changed = before_criteria != after_criteria
            config_changed = candidate.config != current.config
            if not config_changed and not criteria_changed:
                break
            trial = self.evaluate(candidate, validation)
            trial.training_score = train_run.mean_score
            trial.validation_score = trial.mean_score
            self.log.append({
                "event": "optimize_round", "round": index,
                "candidate": candidate.version, "training_score": train_run.mean_score,
                "validation_score": trial.mean_score,
                "criteria_changed": criteria_changed, "config_changed": config_changed,
            })
            if trial.mean_score > best_run.mean_score:
                best, best_run, current = candidate, trial, candidate
            else:
                break
        return best, best_run

    def compose(self, artifacts, name=None, evaluator=None, tests=None):
        stages = list(artifacts)
        if not stages:
            raise ValueError("compose() requires at least one artifact")
        def run(prompt="", **kwargs):
            value = prompt
            for stage in stages:
                result = self.execute(stage, {"prompt": value, **kwargs})
                if not result.passed:
                    raise RuntimeError(f"stage {stage.name!r} failed: {result.error or result.test_results}")
                value = result.value
            return str(value)
        return self.create_code_artifact(
            name or "pipeline_" + "_".join(stage.name for stage in stages),
            run, "prompt -> script", evaluator or stages[-1].evaluator, tests,
            provenance={"stages": [stage.name for stage in stages]},
        )
