# CORRECTIONS

<!-- BEGIN MANUAL: overview -->
CORRECTIONS is the cross-dictionary staging area for CDSL correction evidence:
daily correction-form downloads, historical notes, dictionary-specific batches,
headword checks, n-gram probes, spreadsheets, and older one-off projects.  It is
not the canonical source text; accepted corrections eventually land in the
target dictionary repository or in `csl-orig`.

## Where to put a correction

| Path | Use |
|---|---|
| `daily/` | Correction-form downloads by date; see `daily/readme.txt`. |
| `dictionaries/` | Dictionary-specific issue preparation and batch scripts. |
| `english/`, `english_error/` | English-word and English-definition error checks. |
| `k1k2/` | Primary/secondary headword checks. |
| `ngram/` | N-gram candidate discovery for suspect spellings. |
| `sanhw1/`, `sanhw2/` | Sanskrit headword review material. |
| `spreadsheets/` | Spreadsheet-based review material. |
| `afem/` | Feminine-ending anomaly extraction; see `afem/readme.md`. |
| `nochange/`, `nonalphabet/`, `abnormending/` | Specialized review buckets. |

## Correction lifecycle

The usual path is:

```text
candidate -> correction note/form -> review -> change file or script -> target repo / csl-orig
```

Keep the evidence.  A later maintainer should be able to recover the dictionary,
line/headword, reason for the correction, and the file/script that produced the
change.

## Important files

| File | Role |
|---|---|
| `history.txt` | Chronological correction log, especially for older correction-form work. |
| `correctionform.txt` | Correction-form reference material. |
| `cfr.tsv`, `cfr.zip`, `redo_cfr.sh` | Correction-form export and refresh material. |
| `corrections_nochange.txt` | Records reviewed but intentionally not changed. |
| `redo_sanhw12.sh` | Refreshes Sanskrit headword review material. |
| `DATA_DICTIONARY.md` | Generic CDSL tag reference. |

## Do not edit blindly

This repository contains historical evidence as well as current working files.
Before moving, deleting, or normalizing a file, record why it is safe.  For new
work, prefer a small local `readme.*` in the working directory with commands,
input files, output files, and the final decision.

## Current status / open questions

- Some subdirectories are historical archives; do not assume every script still
  runs unchanged.
- `daily/` names are date-sensitive and should remain auditable.
- Dictionary-specific batches should say where the accepted change was applied:
  target dictionary repo, `csl-orig`, or no-change list.
<!-- END MANUAL: overview -->

## Issues

This repository uses the Sanskrit Lexicon unified issue taxonomy with:
- **9 type labels**: link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **3 severity levels**: minor, medium, hard
- **4 milestones**: Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

## GitHub Issue Conventions

All issues follow the unified taxonomy. See [CLAUDE.md](CLAUDE.md) for details.

---
*Updated by Cologne Issue Runbook*
