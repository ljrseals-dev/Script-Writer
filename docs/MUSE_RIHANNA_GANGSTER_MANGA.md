# Muse by Rihanna × Gangster Manga

## Integration contract

```
Muse by Rihanna core (preserved source)
  ├─ nine-stage narrative pyramid
  ├─ colors / lights / thoughts / symbols
  ├─ decision recording and symbolic extraction
  └─ optional life-story, wizard, prose modules
          │
          ▼
muse_bridge.py (sidecar; no core enum or stage mutation)
  ├─ gangster_manga palette interpretation
  ├─ localized stage questions
  └─ optional symbolic readings
          │
          ▼
MUSE-GM decision surface (existing factorial/rubric engine)
  └─ independent ranking and evidence-status reporting
```

The original `muse_engine.py`, `muse_lifestory.py`, `muse_wizard.py`, and `muse_prose.py` sources are preserved under `muse_core/`. Their source repository is `ljrseals-dev/stunning-happiness` at commit `99048bb31d8c8c212287f867eb9be9690dc5655f` (MIT). Markdown-wrapped Python files were extracted from their fenced code blocks; the wizard source was copied as its standalone Python module.

## Narrative stages

The base order remains Ordinary World → Inciting Incident → Rising Action → First Climax (False Victory) → Fall → Dark Night → Second Climax (True Choice) → Falling Action → Resolution. Gangster Manga prompts interrogate hierarchy, territory, loyalty, debt, complicity, succession, and the cost of power. They do not prescribe plot outcomes.

## Multilingual and model policy

English is canonical for model prompts, model IDs, internal evaluation, and reproducibility. Included interface prompt locales: English, Simplified Chinese, Spanish, Japanese, and French. The bridge falls back to English for unsupported locales. The repository does not bundle model weights or perform implicit downloads. English-first model candidates are documented in `model_policy.json`; adapters remain optional and must record model/revision/translation metadata.

## Extraction boundary

The four first-class Python modules above are extracted into the destination repository. The source repository also contains historical ZIP bundles. Those binary ZIP payloads are not represented as extracted files in this change; their exact archive contents must be unpacked and cross-checked separately before claiming complete archive extraction. The destination's pre-existing `Muse_GM/Zip/` archives are likewise left untouched.

## Running

```bash
python -m muse_core --stage ordinary_world --language en --symbol colors:black --symbol symbols:crown
python -m unittest tests.test_muse_bridge -v
```

The original engine remains directly runnable with `python muse_core/muse_engine.py --help`. Optional model use is not required for core consultations.
