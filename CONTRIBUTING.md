# Contributing / المساهمة

Thank you for contributing. This is an early-stage, focused text-processing project.

1. Open an issue with a minimal **synthetic** example and expected result; do not post private texts or credentials.
2. Submit a pull request that includes a regression test; do not silently broaden removal rules.
3. Run `PYTHONPATH=src python -m unittest discover -s tests -v` before submission.
4. Document linguistic assumptions and known exceptions. Prefer conservative behavior over guesses.
5. Avoid heavy, paid, or network-dependent packages without explicit maintainer discussion.

Contributors agree their submitted code is made available under this repository's MIT License.
