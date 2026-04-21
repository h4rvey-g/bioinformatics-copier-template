# data/

Store large inputs and bulky derived files here.

Recommended naming rules:

- keep directories shallow, ideally no more than 3 levels deep
- avoid spaces or special characters; use `_` or `-` when separators help readability
- prefer lowercase names for portability across systems
- consider numeric step prefixes such as `101_raw_data/` and `102_qc/`
- keep step prefixes aligned across code, data, and results for the same stage

Example step-aligned layout:

- `workflows/101_ingest.nf`
- `data/101_raw_data/`
- `results/101_qc/`

This directory is ignored by Git by default.
Do not put small example metadata here; use `assets/` for that instead.
