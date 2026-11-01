"""Command-line scanner: run the Canadian identifier detectors over files.

Reads plain-text files, JSON Lines records, or standard input; writes one
JSON Lines record per input document with the identifiers found; optionally
writes redacted copies. The default engine is the stdlib-only ``scan()``
(no Presidio or spaCy); ``--engine presidio`` uses the Presidio integration
so that context-gated entities (CA_AB_ULI, CA_HEALTH_CARD) and, with
``--include-builtins``, Presidio's own PERSON / DATE_TIME / etc. are
reported too.

Examples::

    pii-detector-ca scan notes/*.txt
    pii-detector-ca scan --recursive notes/ --output hits.jsonl
    pii-detector-ca scan --input-format jsonl --text-field text records.jsonl
    cat note.txt | pii-detector-ca scan -
    pii-detector-ca scan --engine presidio --include-builtins --redact-dir out/ notes/

Output record (one line per document)::

    {"source": "notes/a.txt", "id": null, "chars": 812,
     "entities": [{"entity": "CA_SIN", "start": 41, "end": 52,
                   "text": "123-456-782", "score": 1.0}]}

Exit status: 0 on success, 2 on usage or input error, 3 when
``--fail-on-match`` is set and at least one identifier was found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

from .core import ENTITY_IDS, scan
from .core.scanner import DEFAULT_THRESHOLD

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_MATCHES = 3

TEXT_SUFFIXES = {".txt", ".md", ".rtf", ".csv", ".tsv", ".log", ".json", ".jsonl", ".xml", ".hl7"}


@dataclass
class Document:
    source: str
    doc_id: str | None
    text: str
    path: Path | None = None  # set for whole-file documents


@dataclass
class Hit:
    entity: str
    start: int
    end: int
    text: str
    score: float

    def as_dict(self) -> dict:
        return {
            "entity": self.entity,
            "start": self.start,
            "end": self.end,
            "text": self.text,
            "score": round(self.score, 4),
        }


# --- Input --------------------------------------------------------------------


def _expand_paths(paths: list[str], recursive: bool) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            it: Iterable[Path] = p.rglob("*") if recursive else p.iterdir()
            out.extend(sorted(f for f in it if f.is_file() and not f.name.startswith(".")))
        elif p.is_file():
            out.append(p)
        else:
            raise FileNotFoundError(raw)
    return out


def _read_documents(
    paths: list[str],
    *,
    input_format: str,
    text_field: str,
    id_field: str,
    recursive: bool,
    encoding: str,
) -> Iterator[Document]:
    if paths == ["-"]:
        data = sys.stdin.read()
        if input_format == "jsonl":
            yield from _jsonl_documents("<stdin>", data.splitlines(), text_field, id_field)
        else:
            yield Document("<stdin>", None, data)
        return
    for path in _expand_paths(paths, recursive):
        fmt = input_format
        if fmt == "auto":
            fmt = "jsonl" if path.suffix.lower() == ".jsonl" else "text"
        with open(path, encoding=encoding, errors="replace") as f:
            if fmt == "jsonl":
                yield from _jsonl_documents(str(path), f, text_field, id_field)
            else:
                yield Document(str(path), None, f.read(), path=path)


def _jsonl_documents(
    source: str, lines: Iterable[str], text_field: str, id_field: str
) -> Iterator[Document]:
    for n, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{source}:{n}: invalid JSON ({exc.msg})") from exc
        if not isinstance(record, dict) or text_field not in record:
            raise ValueError(f"{source}:{n}: no {text_field!r} field")
        doc_id = record.get(id_field)
        yield Document(
            f"{source}:{n}", None if doc_id is None else str(doc_id), str(record[text_field])
        )


# --- Engines ------------------------------------------------------------------


class CoreEngine:
    name = "core"

    def __init__(self, entities: list[str] | None, threshold: float):
        self.entities = entities
        self.threshold = threshold

    def hits(self, text: str) -> list[Hit]:
        return [
            Hit(m.entity, m.start, m.end, m.text, m.score)
            for m in scan(text, entities=self.entities, threshold=self.threshold)
        ]


class PresidioEngine:
    name = "presidio"

    def __init__(
        self,
        entities: list[str] | None,
        threshold: float,
        *,
        include_builtins: bool,
        spacy_model: str,
    ):
        try:
            from presidio_analyzer import AnalyzerEngine
            from presidio_analyzer.nlp_engine import NlpEngineProvider
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise SystemExit(
                "The presidio engine needs the optional dependency: "
                "pip install 'pii-detector-ca[presidio]' and "
                f"python -m spacy download {spacy_model}"
            ) from exc
        from . import add_recognizers

        nlp = NlpEngineProvider(
            nlp_configuration={
                "nlp_engine_name": "spacy",
                "models": [{"lang_code": "en", "model_name": spacy_model}],
            }
        ).create_engine()
        self.analyzer = AnalyzerEngine(nlp_engine=nlp, supported_languages=["en"])
        add_recognizers(self.analyzer.registry)
        self.threshold = threshold
        self.include_builtins = include_builtins
        self.entities = set(entities) if entities else None

    def hits(self, text: str) -> list[Hit]:
        results = self.analyzer.analyze(text=text, language="en", score_threshold=self.threshold)
        out = []
        for r in results:
            if self.entities is not None and r.entity_type not in self.entities:
                continue
            builtin = not r.entity_type.startswith("CA_")
            if self.entities is None and builtin and not self.include_builtins:
                continue
            out.append(Hit(r.entity_type, r.start, r.end, text[r.start : r.end], r.score))
        return sorted(out, key=lambda h: (h.start, h.end, h.entity))


# --- Output -------------------------------------------------------------------


def redact(text: str, hits: list[Hit], placeholder: str) -> str:
    """Replace each hit span with ``placeholder`` (``{entity}`` is substituted).

    Overlapping spans are merged; the placeholder names the first entity of
    the merged run.
    """
    spans = sorted(((h.start, h.end, h.entity) for h in hits), key=lambda s: (s[0], -s[1]))
    merged: list[tuple[int, int, str]] = []
    for start, end, entity in spans:
        if merged and start < merged[-1][1]:
            prev = merged[-1]
            merged[-1] = (prev[0], max(prev[1], end), prev[2])
        else:
            merged.append((start, end, entity))
    out, pos = [], 0
    for start, end, entity in merged:
        out.append(text[pos:start])
        out.append(placeholder.format(entity=entity))
        pos = end
    out.append(text[pos:])
    return "".join(out)


def _redacted_path(redact_dir: Path, doc: Document, index: int) -> Path:
    """Whole files keep their name; JSON Lines records and stdin use the id."""
    if doc.path is not None:
        return redact_dir / (doc.path.name if doc.path.suffix else doc.path.name + ".txt")
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", doc.doc_id) if doc.doc_id else f"doc-{index:06d}"
    return redact_dir / f"{stem}.txt"


# --- Main ---------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pii-detector-ca",
        description="Find Canadian government and health identifiers in text files.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser(
        "scan",
        help="scan files, directories, JSON Lines records or stdin",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("paths", nargs="+", help="files or directories; '-' reads stdin")
    p.add_argument("-r", "--recursive", action="store_true", help="descend into directories")
    p.add_argument(
        "--input-format",
        choices=["auto", "text", "jsonl"],
        default="auto",
        help="auto: *.jsonl is JSON Lines, everything else is plain text",
    )
    p.add_argument("--text-field", default="text", help="JSON Lines field holding the text")
    p.add_argument("--id-field", default="id", help="JSON Lines field used as document id")
    p.add_argument("--encoding", default="utf-8")
    p.add_argument(
        "--engine",
        choices=["core", "presidio"],
        default="core",
        help="core: stdlib regex+checksum (default); presidio: full AnalyzerEngine",
    )
    p.add_argument(
        "--entities",
        help="comma-separated entity ids to report (default: all pack entities)",
    )
    p.add_argument(
        "--include-builtins",
        action="store_true",
        help="with --engine presidio, also report Presidio's own entities (PERSON, DATE_TIME, ...)",
    )
    p.add_argument("--spacy-model", default="en_core_web_sm")
    p.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    p.add_argument("-o", "--output", help="write JSON Lines here instead of stdout")
    p.add_argument("--redact-dir", help="also write a redacted copy of every document here")
    p.add_argument(
        "--placeholder",
        default="[{entity}]",
        help="redaction placeholder; {entity} is replaced by the entity id",
    )
    p.add_argument(
        "--fail-on-match",
        action="store_true",
        help=f"exit {EXIT_MATCHES} if any identifier is found (for pipelines)",
    )
    p.add_argument("-q", "--quiet", action="store_true", help="no summary on stderr")
    return parser


def _parse_entities(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    wanted = [e.strip().upper() for e in raw.split(",") if e.strip()]
    unknown = [e for e in wanted if e not in ENTITY_IDS and not e.isupper()]
    if unknown:
        raise ValueError(f"unknown entities: {', '.join(unknown)}")
    return wanted


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        entities = _parse_entities(args.entities)
        if args.engine == "core":
            bad = [e for e in entities or [] if e not in ENTITY_IDS]
            if bad:
                raise ValueError(
                    f"core engine knows only {', '.join(ENTITY_IDS)}; got {', '.join(bad)}"
                )
            engine: CoreEngine | PresidioEngine = CoreEngine(entities, args.threshold)
        else:
            engine = PresidioEngine(
                entities,
                args.threshold,
                include_builtins=args.include_builtins,
                spacy_model=args.spacy_model,
            )
        docs = _read_documents(
            args.paths,
            input_format=args.input_format,
            text_field=args.text_field,
            id_field=args.id_field,
            recursive=args.recursive,
            encoding=args.encoding,
        )
        redact_dir = Path(args.redact_dir) if args.redact_dir else None
        if redact_dir:
            redact_dir.mkdir(parents=True, exist_ok=True)

        out = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout
        counts: Counter[str] = Counter()
        n_docs = n_docs_with_hits = 0
        try:
            for index, doc in enumerate(docs):
                hits = engine.hits(doc.text)
                n_docs += 1
                if hits:
                    n_docs_with_hits += 1
                counts.update(h.entity for h in hits)
                record = {
                    "source": doc.source,
                    "id": doc.doc_id,
                    "chars": len(doc.text),
                    "entities": [h.as_dict() for h in hits],
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                if redact_dir:
                    target = _redacted_path(redact_dir, doc, index)
                    target.write_text(redact(doc.text, hits, args.placeholder), encoding="utf-8")
        finally:
            if out is not sys.stdout:
                out.close()
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"pii-detector-ca: error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    total = sum(counts.values())
    if not args.quiet:
        summary = ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "none"
        print(
            f"pii-detector-ca: engine={engine.name} documents={n_docs} "
            f"with_identifiers={n_docs_with_hits} identifiers={total} ({summary})",
            file=sys.stderr,
        )
    if args.fail_on_match and total:
        return EXIT_MATCHES
    return EXIT_OK


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
