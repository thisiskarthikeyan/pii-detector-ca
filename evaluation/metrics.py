"""Span-level metrics for de-identification evaluation.

Recall views (per gold entity type):

1. Leak recall: a gold PII span counts as detected if ANY predicted span of
   ANY entity type overlaps it. This is the de-id threat model (does the
   value get masked?) and is an upper bound: incidental overlap by an
   unrelated recognizer (a DATE_TIME over a health number) counts.

2. Strict (fully-covered) recall: the gold span must be FULLY covered by
   the union of predicted spans. One-character overlaps do not count.

3. Pack-attributed recall: the gold span must overlap a prediction whose
   type is the gold type or a declared alias of it (ATTRIBUTION). This is
   the number that measures the recognizer that owns the entity; it is the
   one gated in CI for pack entities, because leak recall passes even when
   the owning recognizer is removed.

4. Typed exact recall: exact boundaries AND the mapped type.

Precision views (per predicted span):

- Pipeline precision: over every prediction the analyzer emitted. A
  prediction is a true positive if it overlaps a gold span that no earlier
  prediction already claimed; later predictions on the same gold span are
  "duplicates" and are excluded from both numerator and denominator
  (Presidio emits several types on one span by design). A prediction that
  overlaps no gold span is a false positive.
- Pack precision: the same computation restricted to predictions whose
  type is owned by the pack (PACK_PREFIX).
- Over-redaction: characters covered by predictions that lie outside every
  gold span, reported per note. Lenient overlap counting hides spans that
  extend far past the identifier; this does not.

Bootstrap confidence intervals resample notes (the unit of independence).
"""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field

# Presidio builtin -> gold label space (used for typed-exact matching).
TYPE_MAP = {
    "DATE_TIME": "DATE",
    "LOCATION": "ADDRESS",
    "CA_STREET_ADDRESS": "ADDRESS",
}

# Gold type -> predicted types that count as the owning recognizer.
# Entities absent here are attributed only by an identical predicted type.
ATTRIBUTION: dict[str, frozenset[str]] = {
    "ADDRESS": frozenset({"CA_STREET_ADDRESS"}),
    "DATE": frozenset({"DATE_TIME"}),
}

PACK_PREFIX = "CA_"


def attributed_types(gold_type: str) -> frozenset[str]:
    return ATTRIBUTION.get(gold_type, frozenset({gold_type}))


@dataclass
class Span:
    start: int
    end: int
    type: str

    def overlaps(self, other: Span) -> bool:
        return self.start < other.end and other.start < self.end


@dataclass
class EntityStats:
    gold: int = 0
    detected: int = 0          # overlap, any type (leak)
    covered: int = 0           # fully covered by union of predictions (strict)
    attributed: int = 0        # overlap by the owning recognizer's type
    exact_typed: int = 0       # exact boundaries + mapped type
    missed_values: list = field(default_factory=list)
    unattributed_values: list = field(default_factory=list)

    @property
    def recall(self) -> float:
        return self.detected / self.gold if self.gold else 0.0

    @property
    def fn_rate(self) -> float:
        return 1.0 - self.recall if self.gold else 0.0

    @property
    def strict_recall(self) -> float:
        return self.covered / self.gold if self.gold else 0.0

    @property
    def attributed_recall(self) -> float:
        return self.attributed / self.gold if self.gold else 0.0

    @property
    def typed_recall(self) -> float:
        return self.exact_typed / self.gold if self.gold else 0.0

    def as_dict(self) -> dict:
        return {
            "gold": self.gold,
            "detected": self.detected,
            "covered": self.covered,
            "attributed": self.attributed,
            "recall": self.recall,
            "strict_recall": self.strict_recall,
            "attributed_recall": self.attributed_recall,
            "typed_recall": self.typed_recall,
        }


def fully_covered(gold: Span, preds: list[Span]) -> bool:
    """True if the union of predicted spans covers every character of gold."""
    segments = sorted((p.start, p.end) for p in preds if p.overlaps(gold))
    pos = gold.start
    for start, end in segments:
        if start > pos:
            return False
        pos = max(pos, end)
        if pos >= gold.end:
            return True
    return pos >= gold.end


def _precision_counts(preds: list[Span], gold_spans: list[Span]) -> dict:
    """Deduplicated TP / duplicate / FP counts for one note's predictions."""
    claimed: set[int] = set()
    tp = dup = fp = 0
    for p in sorted(preds, key=lambda s: (s.start, s.end, s.type)):
        hits = [i for i, g in enumerate(gold_spans) if p.overlaps(g)]
        if not hits:
            fp += 1
        elif any(i not in claimed for i in hits):
            tp += 1
            claimed.update(hits)
        else:
            dup += 1
    return {"tp": tp, "dup": dup, "fp": fp, "total": len(preds)}


def _overredaction_chars(preds: list[Span], gold_spans: list[Span]) -> int:
    """Characters covered by predictions that fall outside every gold span."""
    covered: set[int] = set()
    for p in preds:
        covered.update(range(p.start, p.end))
    for g in gold_spans:
        covered.difference_update(range(g.start, g.end))
    return len(covered)


def _finalize_precision(c: dict) -> dict:
    denom = c["tp"] + c["fp"]
    return {
        **c,
        "precision": c["tp"] / denom if denom else 0.0,
    }


def evaluate_notes(notes, predictions) -> tuple[dict, dict, list[dict]]:
    """Compare gold entities against predictions.

    notes: list of corpus records with gold `entities`
    predictions: list (parallel to notes) of lists of Span
    Returns (per_entity_stats, precision, per_note_counts).

    precision carries: pipeline (all predictions), pack (PACK_PREFIX
    predictions only), pred_counts (per predicted type: {"tp", "fp"}),
    overredaction (chars outside gold, total and per note).
    per_note_counts feeds bootstrap_ci (notes are the resampling unit).
    """
    stats: dict[str, EntityStats] = defaultdict(EntityStats)
    by_form: dict[tuple[str, str], EntityStats] = defaultdict(EntityStats)
    pipeline = {"tp": 0, "dup": 0, "fp": 0, "total": 0}
    pack = {"tp": 0, "dup": 0, "fp": 0, "total": 0}
    pred_counts: dict[str, dict[str, int]] = defaultdict(lambda: {"tp": 0, "fp": 0})
    over_total = 0
    per_note: list[dict] = []

    for note, preds in zip(notes, predictions, strict=True):
        gold_spans = [Span(e["start"], e["end"], e["type"]) for e in note["entities"]]
        n_detected = n_covered = n_attributed = 0

        for gold, ent in zip(gold_spans, note["entities"], strict=True):
            overlapping = [p for p in preds if p.overlaps(gold)]
            owners = attributed_types(gold.type)
            detected = bool(overlapping)
            covered = fully_covered(gold, overlapping)
            attributed = any(p.type in owners for p in overlapping)
            exact = any(
                p.start == gold.start
                and p.end == gold.end
                and TYPE_MAP.get(p.type, p.type) == gold.type
                for p in preds
            )
            targets = [stats[gold.type]]
            form = ent.get("form")
            if form:
                targets.append(by_form[(gold.type, form)])
            for s in targets:
                s.gold += 1
                s.detected += detected
                s.covered += covered
                s.attributed += attributed
                s.exact_typed += exact
            record = {"note_id": note["id"], "value": ent["value"], "type": gold.type}
            if form:
                record["form"] = form
            if not detected:
                stats[gold.type].missed_values.append(record)
            if not attributed:
                stats[gold.type].unattributed_values.append(record)
            n_detected += detected
            n_covered += covered
            n_attributed += attributed

        note_pipe = _precision_counts(preds, gold_spans)
        pack_preds = [p for p in preds if p.type.startswith(PACK_PREFIX)]
        note_pack = _precision_counts(pack_preds, gold_spans)
        for k in pipeline:
            pipeline[k] += note_pipe[k]
            pack[k] += note_pack[k]
        for p in preds:
            key = "tp" if any(p.overlaps(g) for g in gold_spans) else "fp"
            pred_counts[p.type][key] += 1
        over = _overredaction_chars(preds, gold_spans)
        over_total += over
        per_note.append(
            {
                "gold": len(gold_spans),
                "detected": n_detected,
                "covered": n_covered,
                "attributed": n_attributed,
                "preds_tp": note_pipe["tp"],
                "preds_fp": note_pipe["fp"],
                "pack_tp": note_pack["tp"],
                "pack_fp": note_pack["fp"],
                "overredaction": over,
            }
        )

    n_notes = len(per_note)
    precision = {
        "pipeline": _finalize_precision(pipeline),
        "pack": _finalize_precision(pack),
        "pred_counts": {k: dict(v) for k, v in sorted(pred_counts.items())},
        "overredaction": {
            "chars_total": over_total,
            "chars_per_note": over_total / n_notes if n_notes else 0.0,
        },
        # Backwards-compatible aliases for the pipeline view.
        "tp": pipeline["tp"],
        "total": pipeline["total"],
        "precision": _finalize_precision(pipeline)["precision"],
    }
    if by_form:
        precision["by_form"] = {
            f"{entity}|{form}": s.as_dict() for (entity, form), s in sorted(by_form.items())
        }
    return dict(stats), precision, per_note


def overall(stats: dict) -> dict:
    gold = sum(s.gold for s in stats.values())
    detected = sum(s.detected for s in stats.values())
    covered = sum(s.covered for s in stats.values())
    attributed = sum(s.attributed for s in stats.values())
    typed = sum(s.exact_typed for s in stats.values())
    return {
        "gold": gold,
        "detected": detected,
        "covered": covered,
        "attributed": attributed,
        "recall": detected / gold if gold else 0.0,
        "fn_rate": 1 - detected / gold if gold else 0.0,
        "strict_recall": covered / gold if gold else 0.0,
        "strict_fn_rate": 1 - covered / gold if gold else 0.0,
        "attributed_recall": attributed / gold if gold else 0.0,
        "typed_recall": typed / gold if gold else 0.0,
    }


def bootstrap_ci(
    per_note: list[dict], n_boot: int = 1000, seed: int = 0, alpha: float = 0.05
) -> dict:
    """Percentile bootstrap CIs for leak, strict and attributed recall, and
    pipeline / pack precision.

    Resamples notes with replacement (notes are independent by construction;
    entities within a note are not). Deterministic given the seed.
    """
    rng = random.Random(seed)
    n = len(per_note)
    keys = ["recall", "strict_recall", "attributed_recall", "precision", "pack_precision"]
    samples: dict[str, list[float]] = {k: [] for k in keys}
    for _ in range(n_boot):
        g = d = c = a = tp = fp = ptp = pfp = 0
        for _ in range(n):
            r = per_note[rng.randrange(n)]
            g += r["gold"]
            d += r["detected"]
            c += r["covered"]
            a += r["attributed"]
            tp += r["preds_tp"]
            fp += r["preds_fp"]
            ptp += r["pack_tp"]
            pfp += r["pack_fp"]
        if g:
            samples["recall"].append(d / g)
            samples["strict_recall"].append(c / g)
            samples["attributed_recall"].append(a / g)
        if tp + fp:
            samples["precision"].append(tp / (tp + fp))
        if ptp + pfp:
            samples["pack_precision"].append(ptp / (ptp + pfp))

    def percentile_interval(values: list[float]) -> list[float]:
        values = sorted(values)
        lo = values[int(alpha / 2 * len(values))]
        hi = values[min(len(values) - 1, int((1 - alpha / 2) * len(values)))]
        return [round(lo, 4), round(hi, 4)]

    return {k: percentile_interval(v) for k, v in samples.items() if v}
