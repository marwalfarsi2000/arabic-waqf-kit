"""Small, deterministic helpers for Arabic pausal endings in TTS scripts.

This project intentionally avoids linguistic claims beyond its narrow rule:
remove only terminal short-vowel marks and tanween from the final Arabic word
of a sentence or line, while preserving internal marks and shadda.
"""

from __future__ import annotations

import unicodedata

# Arabic fathatan, dammatan, kasratan, fatha, damma, kasra.
ENDING_VOWELS = frozenset("\u064b\u064c\u064d\u064e\u064f\u0650")
# Marks are grouped by Unicode's combining property, not a hard-coded range.
TERMINATORS = frozenset(".!?؟؛…\n")
CLOSING_MARKS = frozenset('"\u201d\u2019\u00bb)]}\u300d\u300f')


def _is_arabic_letter(char: str) -> bool:
    """Avoid touching digits, Latin script, or unrelated combining marks."""
    return unicodedata.category(char).startswith("L") and "ARABIC" in unicodedata.name(char, "")


def _ending_marks_to_remove(text: str, start: int, end: int) -> set[int]:
    """Locate removable vowel marks on the last Arabic letter before *end*."""
    pos = end - 1
    while pos >= start and (text[pos].isspace() or text[pos] in CLOSING_MARKS):
        pos -= 1
    mark_end = pos + 1
    while pos >= start and unicodedata.combining(text[pos]):
        pos -= 1
    if pos < start or not _is_arabic_letter(text[pos]):
        return set()
    return {i for i in range(pos + 1, mark_end) if text[i] in ENDING_VOWELS}


def strip_final_short_vowels(text: str) -> str:
    """Remove final case/mood vowels at sentence and line boundaries.

    Example:
        >>> strip_final_short_vowels('كانَ المساءُ هادئًا. وعادَ الطائرُ.')
        'كانَ المساءُ هادئًا. وعادَ الطائر.'

    The first sentence ends with a bare alif after tanween; changing this
    correctly needs morphological knowledge, so this conservative function
    leaves it alone. It does not rewrite spelling or pronounce text.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    removed: set[int] = set()
    start = 0
    for index, char in enumerate(text):
        if char in TERMINATORS:
            removed.update(_ending_marks_to_remove(text, start, index))
            start = index + 1
    removed.update(_ending_marks_to_remove(text, start, len(text)))
    return "".join(char for index, char in enumerate(text) if index not in removed)


def count_removed_marks(before: str, after: str) -> int:
    """Return how many terminal marks were removed without exposing the text."""
    if not isinstance(before, str) or not isinstance(after, str):
        raise TypeError("before and after must be strings")
    return len(before) - len(after)
