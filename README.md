# CORRECTIONS

_Created: 16-05-2026 · Last updated: 05-07-2026_

Digitizing 40+ Sanskrit dictionaries from 19th/20th-century printed scans
produces errors — typos, misread diacritics, mis-split entries — at a scale
no single editor can catch by re-reading. The Cologne Digital Sanskrit
Dictionaries (CDSL) project runs a public **correction form** that lets any
reader flag an error against any dictionary; this repo is where every
correction ever accepted across the whole project is recorded, per
dictionary, as a durable audit trail — independent of whatever tooling
happens to render the correction form itself.

Corrections are never applied silently to source text. Each one is logged
here (who reported it, what changed, when, and whether it was actually
applied), so a scholar citing a CDSL entry can trace exactly what changed
and why — the same discipline the
[org CLAUDE.md](../CLAUDE.md) `csl-orig` workflow enforces for source edits.

## Structure

| Path | Contents |
|---|---|
| [dictionaries/](dictionaries) | One subfolder per dictionary code (e.g. [ACC](dictionaries/ACC), [MW](dictionaries/MW), [PWG](dictionaries) siblings) — each holds a `<DICT>_correctionform.txt` history file and dictionary-specific consistency checks |
| [daily/](daily) | Scripts that pull the day's correction-form submissions (`dailydown.py`, `download_cfr_ymd.py`) and push them as GitHub issues (`upload_github_issue1.py`) |
| [correction_form_app/](correction_form_app) | The PHP correction-form web app itself (form, response handler, thank-you page) |
| [history.txt](history.txt) | Chronological project-wide log of correction batches since 2018 |
| [cfr.tsv](cfr.tsv) / [cfr.zip](cfr.zip) | Consolidated correction-form-response export |
| [61267-Sanskrit-Catalan-Words-List.txt](61267-Sanskrit-Catalan-Words-List.txt) | An external contributed word list under review |

## A real correction, read from the audit trail (not invented)

From [dictionaries/ACC/ACC_correctionform.txt](dictionaries/ACC/ACC_correctionform.txt):

```
Case 23811: 09/11/2017 dict=ACC, L=37452, hw=vESvatmyarahasya, user=dhaval
old = vESvatmyarahasya
new = vESvAtmyarahasya
comment = typo
status =  Corrected 09/11/2017
```

And from [history.txt](history.txt), the scale a single logged batch can
reach:

```
July 18, 2019 Corrections of c-cedilla to Ś/ś in STC.
  see https://github.com/sanskrit-lexicon/CORRECTIONS/issues/430.
  roughly 655 changes.
```

## Data format

Standard Sanskrit lexicography markup used across correction records — see
[DATA_DICTIONARY.md](DATA_DICTIONARY.md):

| Tag | Role |
|---|---|
| `<L>NNNN` | Entry begin |
| `<k1>word` | Primary headword |
| `<lex>cat` | Category |
| `<ls>src` | Source |

## Issue taxonomy

This repo uses the Sanskrit Lexicon unified issue taxonomy:

- **9 type labels**: link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **3 severity levels**: minor, medium, hard
- **4 milestones**: Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

See [CLAUDE.md](CLAUDE.md) for full definitions and the
[org-level runbook](../CLAUDE.md). Corrections applied to source text follow
the `csl-orig` correction workflow (snapshot → apply → validate → audit
change file) documented there — this repo is the audit trail, not the
source.

---

_Dr. Mārcis Gasūns_
