"""Span-level metrics for de-identification evaluation.

Three views:

1. Leak-oriented recall (primary): a gold PII span counts as detected if ANY
   predicted span of ANY entity type overlaps it. This matches the de-id
   threat model — what matters is whether the value gets masked, not whether
   the type label is right. The complement is the false-negative (leak) rate.

2. Strict (fully-covered) recall: a gold span counts only if it is FULLY
   covered by the union of predicted spans. One-character overlaps that would
   leave most of an identifier unmasked do not count. This is the honest
   version of the masking threat model; leak recall is an upper bound on it.

3. Type-correct exact match (secondary): predicted span must match the gold
   span boundaries exactly AND carry the expected entity type (after mapping
   builtin Presidio types, e.g. DATE_TIME -> DATE).

Bootstrap confidence intervals are computed by resampling notes (the unit of
independence in the corpus), not individual entities.
"""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field

# Presidio builtin -> gold label space.
TYPE_MAP = {
    "DATE_TIME": "DATE",
    "LOCATION": "ADDRESS",
    "PHONE_NUMBER": "IN_MOBILE",
}


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
    detected: int = 0          # overlap, any type
    covered: int = 0           # fully covered by union of predictions (strict)
    exact_typed: int = 0       # exact boundaries + mapped type
    missed_values: list = field(default_factory=list)

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
    def typed_recall(self) -> float:
        return self.exact_typed / self.gold if self.gold else 0.0


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


def evaluate_notes(notes, predictions) -> tuple[dict, dict, list[dict]]:
    """Compare gold entities against predictions.

    notes: list of corpus records with gold `entities`
    predictions: list (parallel to notes) of lists of Span
    Returns (per_entity_stats, precision_counts, per_note_counts).
    per_note_counts feeds bootstrap_ci (notes are the resampling unit).
    """
    stats: dict[str, EntityStats] = defaultdict(EntityStats)
    tp_pred, total_pred = 0, 0
    per_note: list[dict] = []

    for note, preds in zip(notes, predictions, strict=True):
        gold_spans = [Span(e["start"], e["end"], e["type"]) for e in note["entities"]]
        n_detected = n_covered = 0

        for gold, ent in zip(gold_spans, note["entities"], strict=True):
            s = stats[gold.type]
            s.gold += 1
            overlapping = [p for p in preds if p.overlaps(gold)]
            if overlapping:
                s.detected += 1
                n_detected += 1
            else:
                s.missed_values.append(
                    {"note_id": note["id"], "value": ent["value"], "type": gold.type}
                )
            if fully_covered(gold, overlapping):
                s.covered += 1
                n_covered += 1
            if any(
                p.start == gold.start
                and p.end == gold.end
                and TYPE_MAP.get(p.type, p.type) == gold.type
                for p in preds
            ):
                s.exact_typed += 1

        note_tp = sum(1 for p in preds if any(p.overlaps(g) for g in gold_spans))
        tp_pred += note_tp
        total_pred += len(preds)
        per_note.append(
            {
                "gold": len(gold_spans),
                "detected": n_detected,
                "covered": n_covered,
                "preds": len(preds),
                "tp_preds": note_tp,
            }
        )

    precision = {"tp": tp_pred, "total": total_pred,
                 "precision": tp_pred / total_pred if total_pred else 0.0}
    return dict(stats), precision, per_note


def overall(stats: dict) -> dict:
    gold = sum(s.gold for s in stats.values())
    detected = sum(s.detected for s in stats.values())
    covered = sum(s.covered for s in stats.values())
    typed = sum(s.exact_typed for s in stats.values())
    return {
        "gold": gold,
        "detected": detected,
        "covered": covered,
        "recall": detected / gold if gold else 0.0,
        "fn_rate": 1 - detected / gold if gold else 0.0,
        "strict_recall": covered / gold if gold else 0.0,
        "strict_fn_rate": 1 - covered / gold if gold else 0.0,
        "typed_recall": typed / gold if gold else 0.0,
    }


def bootstrap_ci(
    per_note: list[dict], n_boot: int = 1000, seed: int = 0, alpha: float = 0.05
) -> dict:
    """Percentile bootstrap CIs for leak recall, strict recall, and precision.

    Resamples notes with replacement (notes are independent by construction;
    entities within a note are not). Deterministic given the seed.
    """
    rng = random.Random(seed)
    n = len(per_note)
    samples: dict[str, list[float]] = {"recall": [], "strict_recall": [], "precision": []}
    for _ in range(n_boot):
        g = d = c = p = tp = 0
        for _ in range(n):
            r = per_note[rng.randrange(n)]
            g += r["gold"]
            d += r["detected"]
            c += r["covered"]
            p += r["preds"]
            tp += r["tp_preds"]
        if g:
            samples["recall"].append(d / g)
            samples["strict_recall"].append(c / g)
        if p:
            samples["precision"].append(tp / p)

    def percentile_interval(values: list[float]) -> list[float]:
        values = sorted(values)
        lo = values[int(alpha / 2 * len(values))]
        hi = values[min(len(values) - 1, int((1 - alpha / 2) * len(values)))]
        return [round(lo, 4), round(hi, 4)]

    return {k: percentile_interval(v) for k, v in samples.items() if v}
