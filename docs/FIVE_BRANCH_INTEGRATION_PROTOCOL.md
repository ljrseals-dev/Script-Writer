# Five-Branch Integration Protocol

**Status:** Workflow specification. This document defines governance and interfaces; it does not claim that every control is already enforced by software.

## A. Branch roles and limits

1. **Muse — narrative architecture.** Maps an approved premise through Ordinary World, Inciting Incident, Rising Action, First Climax (False Victory), Fall, Dark Night, Second Climax (True Choice), Falling Action, and Resolution. Applies the project's declared symbolic registers (colors, lights, thoughts, symbols). It organizes dramatic meaning; it does not establish facts, rank premises, or approve a draft.

2. **MUSE-GM — factorial evaluation.** Defines and enumerates a finite configuration space, applies a versioned rubric and weight profile, uses a declared deterministic tie-break, and exports rankings and sensitivity results. Rubric values are encoded editorial judgments. Scores are conditional outputs, not truth, ethics, quality, or market-success measurements.

3. **Brute Genius — completeness audit.** Defines what counts as the declared search space and reconciles expected combinations against evaluated, filtered, invalid, failed, and unprocessed combinations. It distinguishes full-space and filtered-subspace exhaustive runs from samples, heuristics, and incomplete runs. Completeness is relative to the declared space; it does not prove that every imaginable premise was considered.

4. **Writing room — governance and evidence.** Maintains human approval gates, claim-level provenance, revision history, and separation of verified fact, disputed claim, interpretation, fiction, and research gap. Model output is never approval. A source citation without a traceable locator is not verification. Silence is not consent.

5. **Hollywood craft lens — screenplay execution.** Proposes revisions in structure, character causality, dialogue, pacing, genre conventions, production awareness, and audience legibility. It must declare and version genre, audience, market, and production assumptions and expose them to sensitivity analysis. It proposes; humans decide. It cannot alter the rubric, conceal exclusions, invent evidence, or bypass approval. Professional craft is not a guarantee of saleability, financing, distribution, awards, or audience response.

Political economy and commercial pressures may be represented as declared structural variables—financing, labor conditions, distribution, censorship, or market assumptions. They must not be concealed moral verdicts or unstated partisan assumptions.

## B. Integration protocol

**0. Freeze the project contract.** Record project/protocol version, format, genre, tone, audience hypothesis, fictional/historical/mixed scope, evidence standards, declared market variables, decision owners, versions of all engines/rubrics, and deterministic settings. A change creates a new version and change record.

**1. Declare the configuration space.** List every dimension, allowed value, dependency, invalid combination, and exclusion. Calculate expected cardinality and hash the canonical configuration. Label each run as full-space exhaustive, filtered-subspace exhaustive, sampled/heuristic, or incomplete. Only the first two may be called exhaustive, and their scope must be explicit.

**2. Freeze rubric and weights.** For each criterion preserve definition, scale, direction, anchors, rationale, missing-value policy, and interactions. Preserve the weight vector, normalization, and tie-break rule. Changing any of these after seeing results requires a new run.

**3. Reconcile completeness and rank.** Brute Genius checks expected versus evaluated, filtered, invalid, failed, and unprocessed counts. Unexplained differences fail the completeness gate. MUSE-GM exports per-criterion scores, weighted totals, deterministic ordering, and sensitivity analysis using plausible alternative weights and perturbations.

**4. Select a premise.** A named human records selected configuration ID, rank, component scores, run ID, sensitivity findings, alternatives, rationale, and any departure from rank order. Human selection may differ from rank order but must not rewrite the computed result.

**5. Establish evidence.** Assign each factual proposition one current status: **Verified fact** (traceable source and locator); **Disputed claim** (attributed with disagreement preserved); **Interpretation** (inference distinguished from source content); **Fiction** (invented, composite, reconstructed, or altered); or **Research gap** (unresolved question). Source records should preserve creator, title, date, archive/publisher, collection/document ID, page/folio/timecode, stable URL/catalogue reference, access date, rights/access notes, and corroboration. Link claims to scenes. A scene dependent on a gap is blocked, explicitly fictionalized, or handled through a scoped human decision under project policy.

**6. Compile into Muse.** Each stage records protagonist objective, pressure/event, choice or failure to choose, causal consequence, stakes/opposition, symbolic register, factual claims, fictional inventions, and open questions. The First Climax must produce a legible false victory whose cost causes the Fall. The Dark Night forces reassessment. The Second Climax requires a consequential true choice. Symbolism supports causality; it does not replace it.

**7. Run the craft pass.** Give the craft lens frozen copies of the approved premise, Muse outline, character sheets, scene cards, evidence ledger, format constraints, and declared genre/audience/production assumptions. Each proposal records problem, affected stage/scene, baseline and alternative, craft rationale, production implications, evidence claims affected, assumptions, uncertainty, and whether it changes premise, evidence, or presentation only. Premise changes return to Step 4; factual changes to Step 5; symbolic-convention changes to Step 6. No silent upstream mutation.

**8. Obtain human approval.** Present baseline and proposal side by side. Record reviewer, role, timestamp, artifact hash, scope, accept/reject/defer decision, rationale, and conditions. Obtain distinct approvals for premise selection, evidence-sensitive treatment, Muse outline, craft revision, screenplay draft, and production/release. Craft approval does not imply historical clearance.

**9. Draft and preserve lineage.** Each scene records originating Muse stage, character objective, evidence dependencies, and accepted craft decisions. Revisions create new versions and hashes; they do not erase prior drafts or approvals. Material changes reopen the relevant gate.

**10. Package the audit.** Include narrative artifacts, evidence ledger, approvals, configuration/rubric snapshots, run manifest, sensitivity results, craft assumptions, change history, and validation report. State separately what was computed, researched, interpreted, invented, approved, and left unknown.

## C. Decision gates and authority

| Gate | Evidence required | Authorizer |
|---|---|---|
| G0 Contract | Versioned contract and owners | Project lead |
| G1 Space | Dimensions, constraints, cardinality, hash | Schema validation plus human configuration owner |
| G2 Rubric | Criteria, anchors, weights, missing-data and tie-break rules | Human rubric owner |
| G3 Completeness | Reconciled disposition counts | Brute Genius check plus human reviewer |
| G4 Selection | Ranking, sensitivity, alternatives | Named human editor |
| G5 Evidence | Claim ledger, source locators, disputes, gaps | Research lead |
| G6 Muse | Nine-stage causal outline | Named story editor |
| G7 Craft | Comparative proposal memo and assumptions | Human writer/showrunner or delegate |
| G8 Draft | Full draft, provenance, unresolved issues | Authorized creative owner; research lead for evidence-sensitive clearance |
| G9 Release | Production, rights, and final audit records | Relevant production/legal/release authorities |

Software may validate schemas, hashes, counts, and required fields. It must not impersonate a human approver or infer approval.

## D. Reproducibility artifacts

| Stage | Required artifacts |
|---|---|
| Contract | Project contract, protocol version, decision-owner register |
| Configuration | Factor-space definition, dimension dictionary, constraints, filters, cardinality, SHA-256 |
| Rubric | Rubric, weights, anchors, missing-value policy, tie-break specification, hashes |
| Enumeration | Command, software/dependency versions, seed if applicable, timestamps, disposition counts, completeness report |
| Ranking | Ranked CSV/JSON, per-criterion scores, manifest, output hashes |
| Sensitivity | Alternative profiles, perturbation plan, results, stability summary |
| Selection | Decision record, configuration ID, alternatives, rationale, reviewer, timestamp |
| Research | Evidence ledger, source metadata, claim-to-scene links, gap register |
| Muse | Nine-stage outline, symbolic-register version, character/causality map, hash |
| Craft | Genre/audience/market/production assumptions, craft memo, proposal decisions |
| Writing room | Scoped approvals, reviewer roles, timestamps, rationale, artifact hashes |
| Draft/release | Script, scene provenance map, revision lineage, consolidated manifest, validation and rights/production records |

Use documented canonical serialization before hashing and retain the artifacts themselves. If external models prevent exact reproduction, record model identifier/version, inference settings, runtime details, and the limitation.

## E. Failure modes and controls

| Failure | Control |
|---|---|
| Shortlist called exhaustive | Declared space, cardinality, filters, reconciled counts |
| Weights changed after winner seen | Freeze/hash inputs; new run and sensitivity comparison |
| High score treated as truth | Conditional-score label; independent sources for factual claims |
| Generated passage treated as evidence | Fiction/draft status unless independently verified |
| Interpretation presented as fact | Claim-level statuses and source locators |
| Symbolism replaces causality | Event, choice, consequence required at each stage |
| Craft overrides rubric | Proposal-only craft pass; reopen upstream gate |
| Hidden market assumptions | Declare, version, sensitivity-test |
| Market pressure becomes moral verdict | Explicit structural variables; no hidden labels |
| AI output treated as approval | Named human, scope, timestamp, rationale, hash |
| Production guess treated as budget fact | Validate in a specific production context |
| Revision erases history | Immutable lineage and hashes |
| Missing sources hidden by fluent scenes | Claim-to-scene links and visible research gaps |

## F. Worked example — fictional port-city family drama

This is invented and makes no claim about a real city, family, labor dispute, or redevelopment plan.

**Declared space:** five binary dimensions: setting (port/inland), era (contemporary/near-future), family pressure (succession/debt), external pressure (labor disruption/redevelopment), and protagonist role (dispatcher/apprentice mechanic). Expected cardinality is 2 × 2 × 2 × 2 × 2 = 32. Brute Genius reconciles 32 evaluated, 0 filtered, 0 invalid, 0 failed. This proves completeness only for these 32 declared configurations.

**Illustrative rubric:** character agency 0.30, causal pressure 0.30, dramatic reversibility 0.25, production tractability 0.15; each scored 1–5. These weights are editorial choices. In this invented run P-017 ranks first at 4.25/5 and P-009 second at 4.20/5. P-017 remains top three under two alternative profiles but falls to fifth when production tractability receives substantially more weight. A human editor selects P-017 because character and causal dimensions matter more than lowest-cost production. The choice and alternatives are recorded without altering the score.

**Premise:** A port dispatcher discovers that a proposed redevelopment plan will displace the repair cooperative employing her family; she must decide whether to protect a relative's concealed agreement or expose the plan's consequences. The city, cooperative, plan, family, and agreement are Fiction. Any real-world analogue creates research gaps until independently sourced.

**Muse outline:**

| Stage | Dramatic movement | Symbolic proposal |
|---|---|---|
| Ordinary World | Dispatcher keeps cooperative schedules running; values reliability and family loyalty. | Steady harbor light: routine |
| Inciting Incident | Draft relocation notice appears; she investigates. | Flickering signal: uncertainty |
| Rising Action | She discovers a relative's private negotiation; relationship strains. | Reflected light: divided knowledge |
| First Climax — False Victory | Relative offers a deal that appears to save core jobs; she accepts. | Floodlight: apparent rescue |
| Fall | Deal shifts costs to apprentices; her choice harms those she meant to protect. | Long shadow: hidden cost |
| Dark Night | She reviews the agreement and listens to workers. | Darkened signal room: reflection |
| Second Climax — True Choice | She releases the complete fictional agreement to the cooperative. | Harbor beacon: shared orientation |
| Falling Action | Cooperative organizes from clearer information; she repairs trust through action. | Several work lights: shared effort |
| Resolution | Future remains uncertain; the cooperative chooses its next step together. | Beacon visible, not a promise of safety |

**Craft proposals:** (1) Show the false victory through a shift roster that excludes apprentices rather than explaining it in dialogue. (2) Make her obtain the agreement through a costly choice rather than coincidence. (3) Stage the disclosure at a cooperative meeting where she must decide whether to read the clause implicating her relative. A production option limits primary locations to the dispatch office, cooperative floor, and meeting room; this is a hypothesis, not a budget estimate. “Adult viewers of character-driven family drama” is an audience-positioning hypothesis, not a fact about all viewers.

The writer accepts proposal 1, revises proposal 2 to preserve family complexity, and defers proposal 3 pending a table read. Decisions are attached to artifact hashes. None changes P-017, the rubric, evidence statuses, or completeness result. Changing the selected configuration reopens the selection gate.

**Interpretation:** Enumeration and scores are conditional computational outputs; selection is human judgment; Muse is dramatic interpretation; craft revisions are proposals; market and production notes are hypotheses. None establishes history, ethical authority, or commercial success.

## Implementation acceptance criteria

Conformance requires code and tests for: canonical serialization and hashes; cardinality and disposition reconciliation; reproducible ranking/tie-breaking; non-mutating sensitivity analysis; claim-level evidence statuses; nine-stage causal compilation; separate craft proposals and approved state; human approval events; revision lineage and reopened gates; and audit-package export. A specification or prompt alone must not be represented as software enforcement.
