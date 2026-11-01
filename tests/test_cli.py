"""Command-line scanner tests (core engine; Presidio engine when the model exists)."""

from __future__ import annotations

import json

import pytest

from pii_detector_ca.cli import EXIT_MATCHES, EXIT_OK, EXIT_USAGE, Hit, main, redact
from pii_detector_ca.validators import luhn_check_digit

SIN = "123456782"  # Luhn-valid, leading 1
assert luhn_check_digit(SIN[:8]) == SIN[8]
NOTE = f"Patient health card 7577 752 616 AB, SIN {SIN[:3]}-{SIN[3:6]}-{SIN[6:]}.\n"


def _records(capsys) -> list[dict]:
    out = capsys.readouterr().out
    return [json.loads(line) for line in out.splitlines() if line.strip()]


class TestTextInput:
    def test_single_file(self, tmp_path, capsys):
        f = tmp_path / "a.txt"
        f.write_text(NOTE, encoding="utf-8")
        assert main(["scan", str(f)]) == EXIT_OK
        (rec,) = _records(capsys)
        assert rec["source"] == str(f) and rec["chars"] == len(NOTE)
        found = {(e["entity"], e["text"]) for e in rec["entities"]}
        assert ("CA_SIN", "123-456-782") in found
        assert ("CA_OHIP", "7577 752 616 AB") in found

    def test_directory_and_recursive(self, tmp_path, capsys):
        (tmp_path / "a.txt").write_text(NOTE, encoding="utf-8")
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "b.txt").write_text("No identifiers here.\n", encoding="utf-8")
        assert main(["scan", str(tmp_path)]) == EXIT_OK
        assert len(_records(capsys)) == 1
        assert main(["scan", "-r", str(tmp_path)]) == EXIT_OK
        recs = _records(capsys)
        assert len(recs) == 2 and recs[1]["entities"] == []

    def test_stdin(self, tmp_path, capsys, monkeypatch):
        import io

        monkeypatch.setattr("sys.stdin", io.StringIO(NOTE))
        assert main(["scan", "-"]) == EXIT_OK
        (rec,) = _records(capsys)
        assert rec["source"] == "<stdin>" and len(rec["entities"]) == 2

    def test_missing_path_is_usage_error(self, tmp_path, capsys):
        assert main(["scan", str(tmp_path / "nope.txt")]) == EXIT_USAGE
        assert "error" in capsys.readouterr().err

    def test_output_file_and_summary(self, tmp_path, capsys):
        f = tmp_path / "a.txt"
        f.write_text(NOTE, encoding="utf-8")
        out = tmp_path / "hits.jsonl"
        assert main(["scan", str(f), "-o", str(out)]) == EXIT_OK
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "identifiers=2" in captured.err and "CA_SIN 1" in captured.err
        assert len(out.read_text(encoding="utf-8").splitlines()) == 1


class TestJsonlInput:
    def test_jsonl_records(self, tmp_path, capsys):
        f = tmp_path / "notes.jsonl"
        f.write_text(
            json.dumps({"id": "n1", "text": NOTE}) + "\n"
            + json.dumps({"id": "n2", "text": "clean"}) + "\n\n",
            encoding="utf-8",
        )
        assert main(["scan", str(f)]) == EXIT_OK
        recs = _records(capsys)
        assert [r["id"] for r in recs] == ["n1", "n2"]
        assert recs[0]["source"].endswith("notes.jsonl:1")
        assert len(recs[0]["entities"]) == 2 and recs[1]["entities"] == []

    def test_custom_fields(self, tmp_path, capsys):
        f = tmp_path / "x.jsonl"
        f.write_text(json.dumps({"note_id": 7, "body": NOTE}) + "\n", encoding="utf-8")
        rc = main(["scan", str(f), "--text-field", "body", "--id-field", "note_id"])
        assert rc == EXIT_OK
        (rec,) = _records(capsys)
        assert rec["id"] == "7" and rec["entities"]

    def test_missing_text_field_is_usage_error(self, tmp_path, capsys):
        f = tmp_path / "x.jsonl"
        f.write_text(json.dumps({"id": 1}) + "\n", encoding="utf-8")
        assert main(["scan", str(f)]) == EXIT_USAGE
        assert "no 'text' field" in capsys.readouterr().err


class TestOptions:
    def test_entities_filter(self, tmp_path, capsys):
        f = tmp_path / "a.txt"
        f.write_text(NOTE, encoding="utf-8")
        assert main(["scan", str(f), "--entities", "ca_sin"]) == EXIT_OK
        (rec,) = _records(capsys)
        assert {e["entity"] for e in rec["entities"]} == {"CA_SIN"}

    def test_unknown_entity_is_usage_error(self, tmp_path, capsys):
        f = tmp_path / "a.txt"
        f.write_text(NOTE, encoding="utf-8")
        assert main(["scan", str(f), "--entities", "US_SSN"]) == EXIT_USAGE

    def test_fail_on_match(self, tmp_path, capsys):
        f = tmp_path / "a.txt"
        f.write_text(NOTE, encoding="utf-8")
        assert main(["scan", str(f), "--fail-on-match", "-q"]) == EXIT_MATCHES
        g = tmp_path / "clean.txt"
        g.write_text("Nothing to see.\n", encoding="utf-8")
        assert main(["scan", str(g), "--fail-on-match", "-q"]) == EXIT_OK

    def test_redact_dir(self, tmp_path, capsys):
        f = tmp_path / "a.txt"
        f.write_text(NOTE, encoding="utf-8")
        out = tmp_path / "redacted"
        assert main(["scan", str(f), "--redact-dir", str(out), "-q"]) == EXIT_OK
        redacted = (out / "a.txt").read_text(encoding="utf-8")
        assert "123-456-782" not in redacted and "7577 752 616 AB" not in redacted
        assert "[CA_SIN]" in redacted and "[CA_OHIP]" in redacted

    def test_redact_dir_names_jsonl_records_by_id(self, tmp_path, capsys):
        f = tmp_path / "notes.jsonl"
        f.write_text(
            json.dumps({"id": "enc/42", "text": NOTE}) + "\n" + json.dumps({"text": NOTE}) + "\n",
            encoding="utf-8",
        )
        out = tmp_path / "redacted"
        assert main(["scan", str(f), "--redact-dir", str(out), "-q"]) == EXIT_OK
        assert sorted(p.name for p in out.iterdir()) == ["doc-000001.txt", "enc_42.txt"]

    def test_redact_placeholder_and_overlaps(self):
        text = "id 123456782 end"
        hits = [Hit("CA_SIN", 3, 12, "123456782", 1.0), Hit("CA_HEALTH_CARD", 3, 12, "x", 0.4)]
        assert redact(text, hits, "<{entity}>") == "id <CA_SIN> end"
        assert redact(text, [], "<{entity}>") == text


class TestPresidioEngine:
    def test_presidio_engine_reports_context_gated_entities(self, tmp_path, capsys):
        pytest.importorskip("en_core_web_sm")
        f = tmp_path / "a.txt"
        f.write_text(
            "Patient Jane Tremblay, Alberta ULI 574839216, seen 2024-03-01.\n", encoding="utf-8"
        )
        assert main(["scan", str(f), "--engine", "presidio", "-q"]) == EXIT_OK
        (rec,) = _records(capsys)
        types = {e["entity"] for e in rec["entities"]}
        assert "CA_AB_ULI" in types
        assert not any(t in types for t in ("PERSON", "DATE_TIME"))

        assert main(["scan", str(f), "--engine", "presidio", "--include-builtins", "-q"]) == EXIT_OK
        (rec,) = _records(capsys)
        types = {e["entity"] for e in rec["entities"]}
        assert "CA_AB_ULI" in types and "DATE_TIME" in types
