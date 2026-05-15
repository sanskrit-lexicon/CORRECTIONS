# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**CORRECTIONS** is the central correction-history repository for all Cologne Digital Sanskrit Lexicons (CDSL). It aggregates correction submissions from the public correction form, per-dictionary error analyses, cross-dictionary headword normalization data, and shared reference files used by correction workflows across all dictionary repos.

## Architecture

| File/Directory | Purpose |
|---|---|
| `correctionform.txt` | Master log of all corrections submitted via the Cologne correction web form |
| `dictionaries/` | Per-dictionary subdirectories; each contains `<DICT>_correctionform.txt` with that dict's correction log |
| `history.txt` | Summary of major correction topics across all dictionaries |
| `sanhw1/` | Master Sanskrit headword list (`sanhw1.txt`) — primary cross-reference used by `hwnorm1` |
| `sanhw2/` | Extended headword list with L-numbers |
| `daily/` | Daily correction processing logs and scripts |
| `english/` | English word reference files for spell-checking |
| `english_error/` | Per-dictionary English spelling error lists |
| `ngram/` | N-gram frequency tables for Sanskrit spell-checking |
| `nonalphabet/` | Non-alphabetic character analysis across dictionaries |
| `k1k2/` | K1/K2 headword comparison analysis |
| `nochange/` | Corrections submitted but requiring no change |
| `corrections_nochange.txt` | Log of no-change decisions |
| `afem/` | A-feminine headword research |
| `cfr.tsv` / `cfr.zip` | Cross-reference (cfr) data |
| `redo_cfr.sh` | Regenerates cross-reference data |
| `redo_sanhw12.sh` | Regenerates `sanhw1` and `sanhw2` from source dictionaries |
| `correction_form_app/` | Source code for the web-based correction submission form |
| `spreadsheets/` | Correction data in spreadsheet format |
| `dhaval/` | Dhaval-contributed correction analyses |
| `dictionaries/` | Per-dictionary correction history directories |

### `sanhw1/` — Shared Headword List

`sanhw1.txt` lists all distinct Sanskrit headwords across all CDSL dictionaries with their dictionary affiliations (format: `headword:dict1,dict2,...`). This file is the primary input for `hwnorm1/sanhw1/sanhw1.py`.

```bash
sh redo_sanhw12.sh   # regenerates sanhw1.txt and sanhw2.txt
```

## Dependencies

- **Python 3**
- **csl-orig** sibling repo — source digitization files (read for headword extraction)
