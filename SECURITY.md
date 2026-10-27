# Security policy

This package sits on a privacy boundary: a missed identifier is a data leak. Please report such findings privately so they can be fixed before they are public.

## What to report privately

- **Leaks (false negatives):** a real-world identifier format that the recognizers fail to detect, especially a *class* of misses (a formatting variant, a province's card layout, a separator style).
- **Validation bypasses:** inputs that defeat a checksum or context gate in a way that hides identifiers.
- **Unsafe handling:** any code path that logs, persists, or transmits input text.

Ordinary false positives, documentation errors, and feature requests are fine as public GitHub issues.

## How to report

Use GitHub's private vulnerability reporting: open the repository's **Security** tab, then click **Report a vulnerability**.

**Never include real personal or patient data in a report.** Reproduce the issue with a synthetic value of the same shape (`benchmark/pii_generators.py` generates checksum-valid ones), or describe the format with digits replaced by `X`.

You can expect an acknowledgement within 7 days. Confirmed leaks get a fix, a regression test, and a CHANGELOG entry crediting you (unless you prefer otherwise).

## Supported versions

| Version | Supported |
|---|---|
| 0.1.x | Yes |

## Scope reminder

This project is a detection aid, not a compliance guarantee. See *What this is not* in the [README](README.md).
