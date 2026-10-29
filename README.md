# Arabic Waqf Kit · عُدّة الوقف العربي

**A small, openly licensed, dependency-free Python utility for conservative Arabic sentence-ending diacritic cleanup before text-to-speech (TTS).**

**أداة بايثون صغيرة ومفتوحة المصدر لتخفيف الحركات الإعرابية في نهاية الجمل قبل توليد الصوت العربي.**

> Status: **v0.1.0 — experimental**. Human listening and language review are required. This tool is not a full Arabic morphology engine, a pronunciation oracle, or a religious recitation tool.

## The problem / المشكلة

Arabic TTS engines sometimes pronounce case endings at sentence stops. In many narration styles, particularly calm, long-form audio, a pausal rendition may sound more natural. Removing all diacritics would destroy useful pronunciation information. This library therefore removes **only short-vowel and tanween marks on the last Arabic letter at sentence/line endings**, leaving interior diacritics and shadda intact.

قد تنطق بعض محركات تحويل النص إلى صوت الحركات الإعرابية في مواضع الوقف. إزالة التشكيل من النص كاملًا تضر النطق. لذلك تزيل هذه المكتبة علامات الحركات القصيرة والتنوين من **الحرف العربي الأخير عند نهاية الجملة أو السطر** فقط، وتُبقي التشكيل الداخلي والشدة.

## Quick start / بداية سريعة

Requires Python 3.10+. Use as source without installing dependencies:

```bash
PYTHONPATH=src python -m arabic_waqf_kit --input examples.txt --output output.txt
PYTHONPATH=src python -m unittest discover -s tests -v
```

Install locally if desired:

```bash
python -m pip install .
arabic-waqf --input examples.txt --output output.txt
```

Read from standard input and write to standard output:

```bash
printf 'الليلُ هادئٌ.\n' | arabic-waqf
# الليلُ هادئ.
```

Python API:

```python
from arabic_waqf_kit import strip_final_short_vowels

text = "الليلُ هادئٌ. ثمَّ ظهرَ القمرُ."
print(strip_final_short_vowels(text))
# الليلُ هادئ. ثمَّ ظهرَ القمر.
```

`--check` exits with status 1 if changes would be made, without writing output. The CLI **never overwrites** an existing output file unless `--overwrite` is set explicitly.

## Safety and scope / حدود واضحة

- Preserves internal vowel marks, shadda (ّ), sukun (ْ), Latin letters, punctuation and ordinary whitespace.
- Handles common sentence endings `.` `!` `?` `؟` `؛` `…` and newlines.
- Conservative behavior: for endings such as `هادئًا` where tanween precedes bare alif, the tool **does not attempt a morphological transformation**. For texts using the alternative encoding `جميلاً` (tanween placed after alif), it removes that trailing mark. Both spellings may occur in real-world text; review the output before TTS. This is intentional.
- Does not resolve contextual pronunciation, dialect, numbers, hamza forms, spelling, Arabic prosody, or tajweed.
- No network calls, API keys, analytics, model costs, or external runtime dependencies.
- Avoid use in Quranic or other text requiring specialized linguistic/religious accuracy without expert review.

## Contributing / المساهمة

Read [CONTRIBUTING.md](CONTRIBUTING.md). Small, well-evidenced fixes and test cases are especially welcome. Code is [MIT licensed](LICENSE).

## Roadmap / خارطة الطريق

See [ROADMAP.md](docs/ROADMAP.md). Future development is **proposed**, not a claim that any existing community or downstream project has adopted this library.

## Provenance / المصدر

The idea comes from practical challenges in creating Arabic long-form narration. This independent utility is provided as a small, experimental starting point. It does not contain private source texts, access credentials, or third-party proprietary code.
