"""Span-level metrics for de-identification evaluation.

Two views:

1. Leak-oriented recall (primary): a gold PII span counts as detected if ANY
   predicted span of ANY entity type overlaps it. This matches the de-id
   threat model — what matters is whether the value gets masked, not whether
   the type label is right. The complement is the false-negative (leak) rate.

2. Type-correct exact match (secondary): predicted span must match the gold
   span boundaries exactly AND carry the expected entity type (after mapping
   builtin Presidio types, e.g. DATE_TIME -> DATE).
"""

from __future__ import annotations

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
    exact_typed: int = 0       # exact boundaries + mapped type
    missed_values: list = field(default_factory=list)

    @property
    def recall(self) -> float:
        return self.detected / self.gold if self.gold else 0.0

    @property
    def fn_rate(self) -> float:
        return 1.0 - self.recall if self.gold else 0.0

    @property
    def typed_recall(self) -> float:
        return self.exact_typed / self.gold if self.gold else 0.0


def evaluate_notes(notes, predictions) -> tuple[dict, dict]:
    """Compare gold entities against predictions.

    notes: list of corpus records with gold `entities`
    predictions: list (parallel to notes) of lists of Span
    Returns (per_entity_stats, precision_counts).
    """
    stats: dict[str, EntityStats] = defaultdict(EntityStats)
    tp_pred, total_pred = 0, 0

    for note, preds in zip(notes, predictions, strict=True):
        gold_spans = [Span(e["start"], e["end"], e["type"]) for e in note["entities"]]

        for gold, ent in zip(gold_spans, note["entities"], strict=True):
            s = stats[gold.type]
            s.gold += 1
            overlapping = [p for p in preds if p.overlaps(gold)]
            if overlapping:
                s.detected += 1
            else:
                s.missed_values.append(
                    {"note_id": note["id"], "value": ent["value"], "type": gold.type}
                )
            if any(
                p.start == gold.start
                and p.end == gold.end
                and TYPE_MAP.get(p.type, p.type) == gold.type
                for p in preds
            ):
                s.exact_typed += 1

        for p in preds:
            total_pred += 1
            if any(p.overlaps(g) for g in gold_spans):
                tp_pred += 1

    precision = {"tp": tp_pred, "total": total_pred,
                 "precision": tp_pred / total_pred if total_pred else 0.0}
    return dict(stats), precision


def overall(stats: dict) -> dict:
    gold = sum(s.gold for s in stats.values())
    detected = sum(s.detected for s in stats.values())
    typed = sum(s.exact_typed for s in stats.values())
    return {
        "gold": gold,
        "detected": detected,
        "recall": detected / gold if gold else 0.0,
        "fn_rate": 1 - detected / gold if gold else 0.0,
        "typed_recall": typed / gold if gold else 0.0,
    }
