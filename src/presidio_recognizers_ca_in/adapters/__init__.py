"""Presidio adapter entry point."""

from .presidio import SpecRecognizer, recognizer_from_spec, recognizers_from_specs

__all__ = ["SpecRecognizer", "recognizer_from_spec", "recognizers_from_specs"]
