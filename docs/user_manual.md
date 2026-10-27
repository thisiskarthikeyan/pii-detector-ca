# User Manual

**For people who want to find Canadian ID numbers in text — without needing a technical background.**

This guide explains what the software does, how to try it on your own text, and how to read the results. It avoids research and engineering jargon.

---

## Who this is for

You might use this if you:

- work with clinical notes, forms, or free-text documents from **Canada**
- need to **spot** Social Insurance Numbers, provincial health card numbers, postal codes and addresses before sharing text with others
- want to **try a few sample sentences** and see what the software flags

This manual is **not** a legal or compliance guide. It does not certify that your organization meets PIPEDA, PHIPA, or any other regulation.

---

## What this product is

This package adds **rules for Canadian ID formats** to text-scanning workflows.

Think of it as a **specialized spell-checker for ID numbers**: it looks at a block of text, finds strings that look like official identifiers, and checks whether they pass format and checksum rules where those rules are public.

It can be used in two ways:

| Way to use it | Best for | Extra software needed |
|---|---|---|
| **Simple scan** (`scan`) | Quick tests, scripts, services that only need ID detection | Python only |
| **Presidio integration** | Full clinical de-identification pipelines that also find names, dates, etc. | Presidio, spaCy, and related models |

Most of this manual focuses on the **simple scan**, because that is the easiest way to try the product.

---

## What it finds

| What it looks for | Plain name |
|---|---|
| `CA_SIN` | Social Insurance Number |
| `CA_OHIP` | Ontario health card number |
| `CA_RAMQ` | Quebec health insurance number |
| `CA_BC_PHN` | BC Personal Health Number |
| `CA_POSTAL_CODE` | Canadian postal code (e.g. K1A 0B1) |
| `CA_STREET_ADDRESS` | Full mailing/residence address ending in province + postal code |
| `CA_AB_ULI` | Alberta health card number (ULI) |
| `CA_HEALTH_CARD` | Health card number for the other provinces/territories (needs nearby words such as "health card") |

The **label in the output** (e.g. `CA_SIN`, `CA_OHIP`) is the short code the software uses. The table above is what each code means in everyday language.

---

## What it does **not** do

Please read this section carefully.

- **It is not a guarantee** that all private information has been removed from a document.
- **It does not find everything by itself** when used in simple scan mode for some ID types (see “When results depend on nearby words” below).
- **It is not a substitute for human review** of sensitive documents.
- **It does not store or send your text anywhere** — everything runs on your machine when you run it locally.
- **It does not include real patient data** in its built-in practice notes; those are synthetic (made-up) examples.
- **Person names and dates** are handled by other tools (Presidio + spaCy), not by the simple `scan` function alone.
- **Checksums are not proof.** Roughly 1 in 12 random 9-digit numbers passes the SIN check and 1 in 10 random 10-digit numbers passes the Ontario check, so order numbers and compact phone numbers are sometimes flagged.

---

## Before you start

### Install

You need Python 3.10 or newer.

The package is not on PyPI yet. Install it from the source code:

```bash
git clone https://github.com/thisiskarthikeyan/pii-detector.git
cd pii-detector
pip install -e .
```

For the full Presidio pipeline (names, dates, etc.), you also need Presidio and a spaCy English model. That setup is more involved; see the main [README](../README.md).

### Important safety rule

**Do not paste real patient or customer data into shared chat tools, tickets, or public forums.**

When testing, use:

- made-up numbers that pass the checksum rules (see examples below), or
- the synthetic practice notes included with this project, or
- redacted copies where you have replaced digits with `X`

---

## How to test with your own text (simple scan)

Open Python and run:

```python
from pii_detector_ca import scan

text = """
Referral note: Ontario health card 7577 752 616 AB on file.
SIN on intake form: 239-698-863.
"""

matches = scan(text, threshold=0.35)

for hit in matches:
    print(f"Found: {hit.text!r}")
    print(f"  Type: {hit.entity}")
    print(f"  Position: characters {hit.start} to {hit.end}")
    print(f"  Confidence: {hit.score:.2f}")
    print()
```

### Settings explained in plain language

| Setting | What it means |
|---|---|
| `text` | The paragraph or document you want checked |
| `threshold=0.35` | How confident a match must be before it is reported (0 = report everything weak or strong; 0.35 is the default; 1.0 = only very strong matches) |

---

## How to read the output

Each match is one piece of text the software thinks is an identifier.

| Field | What it tells you |
|---|---|
| **Type** (`entity`) | Which kind of ID (e.g. `CA_SIN`, `CA_OHIP`) |
| **Found text** (`text`) | The exact characters matched in your input |
| **Position** (`start`, `end`) | Where in the string the match begins and ends (counting from 0 at the first character) |
| **Confidence** (`score`) | How sure the rule is, from 0.0 to 1.0. Higher = stronger evidence. Values near **1.0** usually mean a checksum or strict structure check passed |

### Example interpretation

```
Found: '239-698-863'
  Type: CA_SIN
  Confidence: 1.00
```

**Plain reading:** “The software found something formatted like a Social Insurance Number, and the check-digit math checks out, so it is very confident.”

```
Found: '7577 752 616 AB'
  Type: CA_OHIP
  Confidence: 1.00
```

**Plain reading:** “This looks like a valid Ontario health number format with a version suffix.”

If **nothing is printed**, the software did not find any ID types strong enough to report at your chosen threshold. That might be correct (no IDs in the text) or it might mean an ID was present but not detected (see limitations below).

---

## When results depend on nearby words

Some ID types have **no public check-digit formula**. For those, the software uses a low base confidence and expects **helpful words nearby** — such as “health card”, “ULI”, “MSP”, “carte soleil” — when used through the **full Presidio pipeline**.

In **simple scan mode** (`scan`), that nearby-word boosting is **not** applied. So:

- **Works in simple scan:** SIN, OHIP, RAMQ, BC PHN, postal codes, full street addresses (checksum or strict structure applies)
- **Never reported in simple scan at the default threshold:** Alberta ULI and the generic health card — they depend entirely on nearby words

If you need those context-sensitive types in production, use the **Presidio integration** (full pipeline), not `scan` alone.

---

## How to tell if the software is “working” on a quick test

Use a **positive test** (should find something) and a **negative test** (should not find an ID).

### Positive test — Canadian SIN

A valid SIN must pass a check-digit calculation. Example that should be **found** with high confidence:

```python
from pii_detector_ca import scan

text = "Employee SIN: 239-698-863"
hits = scan(text)
assert any(h.entity == "CA_SIN" and h.score >= 0.9 for h in hits)
print("PASS: valid SIN detected")
```

### Negative test — random digits that fail the check

```python
text = "Invoice reference: 123-456-789"
hits = scan(text)
sin_hits = [h for h in hits if h.entity == "CA_SIN"]
assert len(sin_hits) == 0
print("PASS: invalid SIN correctly ignored")
```

### What “success” means for you

| Outcome | Meaning |
|---|---|
| Valid example IDs are **found** with confidence near **1.0** | The core rules are working |
| Random or invalid numbers are **not** reported as IDs | The checker is not crying wolf on every digit string |

### What “failure” looks like

| Problem | What you might see | What to do |
|---|---|---|
| Valid ID not found | Empty result list | Check if the ID type needs the Presidio full pipeline; check formatting (spaces, dashes) |
| Wrong ID type | Unexpected `entity` label | Review text context; some formats overlap (a 9-digit number can be a SIN or an Alberta ULI) |
| Innocent number flagged | Match on invoice/order numbers | Expected occasionally for checksum-only types (see the collision rates above) |
| Nothing installs | Import error | Confirm Python version and `pip install` |

---

## Built-in quality checks (for reviewers and maintainers)

The project ships with **practice documents** (synthetic clinical notes) and scripts that score how well the software performs on those notes. You do **not** need to run these for everyday use, but they answer: “Is this release still good?”

### What gets compared

1. **Stock Presidio** — generic tool without this package’s Canadian rules  
2. **Presidio + CA builtins** — generic tool with Presidio’s own (normally switched-off) SIN and postal-code rules  
3. **Presidio + this package** — generic tool **with** this package’s rules  

On the practice notes, the package is expected to find **all** injected Canadian ID numbers that the benchmark labels, while the first two miss the provincial health-card numbers.

### Running the main check (same as automated CI)

From the project folder, with dependencies installed:

```bash
python evaluation/run_eval.py --all
python evaluation/check_thresholds.py
```

### Reading the result **without jargon**

After `run_eval.py --all`, open `evaluation/results/results.md`.

You will see tables with columns like **Recall**, **Strict recall**, **FN rate**. Here is what they mean in plain language:

| Column name in the file | Plain meaning |
|---|---|
| **Gold** | How many labeled IDs of that type were in the practice notes |
| **Detected (overlap)** | How many of those the software found (at least partially) |
| **Recall** | **“Found rate”** — out of all IDs that should be there, what fraction did we catch? **1.000 = found all of them** |
| **Strict recall** | **“Fully covered rate”** — the entire labeled ID span was inside what we flagged, not just a piece of it |
| **FN rate** | **“Miss rate”** — fraction we failed to find. **0.000 = missed none** |
| **Span precision** (in the paragraph below the table) | **“Wrong alarm rate among our flags”** — when we flagged something as an ID, how often were we right? Higher is better |

Focus on rows labeled **Presidio + pack** (not “Stock Presidio”).

**Success for a release:** the last command prints something like:

```
53 checks, 0 failure(s).
Threshold gate passed.
```

That means every automatic minimum-quality bar passed.

**Failure:** you see `FAIL` lines and a non-zero failure count. Something regressed compared to the expected baseline — treat the release as **not ready** until a maintainer investigates.

### Other bundled checks (short descriptions)

| Script | Plain purpose |
|---|---|
| `run_negatives.py` | Feeds **notes with no real IDs** but lots of confusing numbers (credit cards, lab values). Measures **wrong alarms**. Lower is better. |
| `run_hard.py` | Uses **deliberately awkward** formatting (no label words, odd separators, line breaks). Shows where the rules are brittle. |
| `run_address_eval.py` | Tests **street addresses** on a separate holdout set not used to train the rules. |
| `run_core_eval.py --all` | Tests the **simple scan** path only (no Presidio). Expect lower “found rate” on context-sensitive IDs — that is expected, not a Presidio regression. |


---

## Quick reference: commands

| Goal | Command |
|---|---|
| Try in Python | `from pii_detector_ca import scan` |
| Run full quality report | `python evaluation/run_eval.py --all` |
| Pass/fail gate | `python evaluation/check_thresholds.py` |
| Simple-scan-only report | `python evaluation/run_core_eval.py --all` |

Results are written under `evaluation/results/` as markdown (human-readable) and JSON (for tools).

---

## Where to learn more

| Document | Audience |
|---|---|
| [README](../README.md) | Developers integrating the package |
| [docs/architecture/core_contract.md](architecture/core_contract.md) | Technical contract for the scanning engine |
| [docs/identifiers/](identifiers/) | Source-backed notes on each ID type’s rules |
| [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md) | Project roadmap and research milestones |

---

## Summary

- This product **finds Canadian ID numbers** in text using format and checksum rules.
- Use **`scan(text)`** for the simplest hands-on test.
- Output shows **what** was found, **where**, and **how confident** the rule is (0–1).
- **Working correctly** on a quick test means valid IDs are found and obvious fakes are ignored.
- The bundled evaluation scripts measure quality on **synthetic practice notes**; **“Threshold gate passed”** means success, **`FAIL`** means failure.
- It **does not** replace legal review, human QA, or full de-identification by itself.

If you need help interpreting a specific result from your own test, compare the **Type**, **Found text**, and **Confidence** columns against the tables in this guide.
