"""Arabic Waqf Kit: conservative, dependency-free TTS text cleanup."""
from .core import count_removed_marks, strip_final_short_vowels

__version__ = "0.1.0"
__all__ = ["strip_final_short_vowels", "count_removed_marks"]
