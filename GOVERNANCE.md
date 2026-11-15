# Muse Screenplay Governance

## Purpose and scope

This document defines provenance, evaluation, attribution, and mutation controls for the
experimental `muse_screenplay` module. It does not replace the existing `muse_core` or
`muse_gm` packages. It governs the new screenplay module and its bundled Artifact Harness.

## Concept and implementation provenance

Concept evidence and implementation evidence are separate streams. Neither is presumed to
always precede the other. A concept may be refined by implementation, and implementation
may expose constraints or defects that change the concept.

When recording a relationship between artifacts, use one of:

- `implements`
- `challenges`
- `constrains`
- `inspires`
- `unknown`

Do not infer a relationship merely because two artifacts are related by topic, date, or name.

## Evidence status vocabulary

Use these labels consistently:

- **Verified** — directly supported by inspectable evidence and a reproducible check.
- **Inferred** — a reasoned interpretation, not direct proof.
- **Disputed** — credible evidence or accounts conflict.
- **Unknown** — available evidence does not establish the claim.
- **Incomplete** — evidence or evaluation is missing, failed, or insufficient to support a conclusion.

An evaluator exception produces an `Incomplete` row, not a passing score.

## Attribution and credits

Requested credits and evidenced contributions are separate fields. A requested credit records
an attribution request; it does not prove authorship, ownership, employment, consent, a legal
relationship, or endorsement. Evidenced contributions should describe specific work and point
to evidence where available.

Do not collapse a credit list into a claim that every listed person performed the same role.
Do not infer contribution from family relationships, names, chronology, or proximity to a project.
Do not add or remove a person's credit as a substitute for resolving a factual dispute.

## Dataset provenance and fallback

Every evaluation dataset should be distinguishable as:

- `remote` — loaded from the declared remote source.
- `offline` — intentionally using bundled local fixtures.
- `fallback` — a remote load was attempted but failed, so local fixtures were substituted.
- `unknown` — provenance has not been established.

Fallback evaluation must include both `fallback_reason` and a clear disclaimer. The harness
calls `assert_no_offline_disguise` before evaluation. A fallback must never be represented as
a successful remote-dataset evaluation.

## Criteria as first-class artifacts

Evaluator logic, tests, and the explicit `criteria_spec` are part of evaluation identity.
`criteria_fingerprint` provides a deterministic structural fingerprint. A changed criteria
fingerprint increments `criteria_version`, even when model configuration is unchanged.

The callable fingerprint is deliberately limited. It includes callable name, qualified name,
bytecode, constants, and defaults. It does not capture closure values, mutable globals,
referenced objects, environment variables, files, remote services, or external configuration.
A matching fingerprint is not proof that all runtime dependencies are identical.

Optimization must compare candidates on the same validation dataset. Training scores are recorded
separately. A candidate is a no-op only when both configuration and criteria are unchanged.

## Mutation audit

Record the reason for a mutation, the before/after evaluation, and the before/after criteria
fingerprints. Preserve original artifacts and their hashes. Hashes establish byte consistency;
they do not establish authorship, ownership, priority, or legal rights.

## Ledger and evidence integrity

The append-only JSONL ledger defaults to `.muse/ledger.jsonl`. Export snapshots go under
`data/ledger/`. Each entry includes a format version, canonical JSON digest, sequence number,
and previous-entry digest. The ledger verifies the existing chain before accepting an append.
Persistence writes a temporary file and atomically replaces the ledger file.

A hash chain is tamper-evident, not immutable. Without an independent external anchor, a person
with control of the entire ledger can rewrite the whole chain. Keep independent copies of
important evidence when long-term verification matters.

## Licensing and legal boundaries

The repository's MIT license applies only to rights that the relevant rights holders have
authorized for this project. No third-party code, datasets, model weights, institutional
endorsement, or other rights are assumed by this governance layer. Follow each upstream
model and dataset's own license and terms.

A working agreement or attribution record is not a signed contract, copyright assignment,
release, or legal opinion. Any "Brute Genius" hold-harmless or warranty addendum remains a
counsel-review draft unless separately executed by the appropriate parties. This document is
engineering governance, not legal advice.

## Validation

Run the minimum local gate:

```bash
pip install -e ".[dev]"
pytest tests/test_governance_schema.py tests/test_governance_integration.py -q
python scripts/integration_check.py
```

Then run the full suite:

```bash
pytest
```

The integration checker verifies selected interface contracts. It does not replace behavioral
tests, runtime model validation, remote dataset verification, legal review, or independent
evidence review.
