import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class CliTests(unittest.TestCase):
    def invoke(self, *args, stdin=""):
        env = dict(os.environ, PYTHONPATH=str(SRC))
        return subprocess.run([sys.executable, "-m", "arabic_waqf_kit", *args],
                              input=stdin, text=True, capture_output=True, env=env, check=False)

    def test_stdin_stdout(self):
        result = self.invoke(stdin="مساءٌ جميلٌ.")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "مساءٌ جميل.")

    def test_check_mode(self):
        self.assertEqual(self.invoke("--check", stdin="القمرُ.").returncode, 1)
        self.assertEqual(self.invoke("--check", stdin="القمر.").returncode, 0)

    def test_refuses_implicit_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "text.txt"
            inp.write_text("القمرُ.", encoding="utf-8")
            result = self.invoke("--input", str(inp), "--output", str(inp))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(inp.read_text(encoding="utf-8"), "القمرُ.")

    def test_writes_new_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "in.txt"
            out = Path(tmp) / "out.txt"
            inp.write_text("القمرُ.", encoding="utf-8")
            result = self.invoke("-i", str(inp), "-o", str(out))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(out.read_text(encoding="utf-8"), "القمر.")
