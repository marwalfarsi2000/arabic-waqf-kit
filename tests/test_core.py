import unittest

from arabic_waqf_kit import count_removed_marks, strip_final_short_vowels


class WaqfTests(unittest.TestCase):
    def test_simple_damma(self):
        self.assertEqual(strip_final_short_vowels("القمرُ."), "القمر.")

    def test_sentence_multiple(self):
        self.assertEqual(strip_final_short_vowels("القمرُ. والهواءُ لطيفٌ!"), "القمر. والهواءُ لطيف!")

    def test_internal_marks_retained(self):
        self.assertEqual(strip_final_short_vowels("جَلَسَ الرجلُ."), "جَلَسَ الرجل.")

    def test_preserve_shadda(self):
        self.assertEqual(strip_final_short_vowels("مُهِمٌّ."), "مُهِمّ.")

    def test_reordered_shadda(self):
        self.assertEqual(strip_final_short_vowels("مُهِمٌّ."), "مُهِمّ.")

    def test_question_mark(self):
        self.assertEqual(strip_final_short_vowels("أينَ المنزلُ؟"), "أينَ المنزل؟")

    def test_quotes_and_space(self):
        self.assertEqual(strip_final_short_vowels('قالَ: «الليلُ هادئٌ». '), 'قالَ: «الليلُ هادئ». ')

    def test_newline(self):
        self.assertEqual(strip_final_short_vowels("طريقٌ\nبيتٍ\n"), "طريق\nبيت\n")

    def test_sukun_is_preserved(self):
        self.assertEqual(strip_final_short_vowels("قُمْ."), "قُمْ.")

    def test_no_change_to_digits(self):
        self.assertEqual(strip_final_short_vowels("النسبة ١٠٪."), "النسبة ١٠٪.")

    def test_no_change_to_latin(self):
        self.assertEqual(strip_final_short_vowels("Hello!"), "Hello!")

    def test_no_change_to_tanween_fatha_before_alif(self):
        self.assertEqual(strip_final_short_vowels("هادئًا."), "هادئًا.")

    def test_empty_string(self):
        self.assertEqual(strip_final_short_vowels(""), "")

    def test_final_without_punctuation(self):
        self.assertEqual(strip_final_short_vowels("الحديقةِ"), "الحديقة")

    def test_ending_quote_without_punctuation(self):
        self.assertEqual(strip_final_short_vowels("«العَلَمُ»"), "«العَلَم»")

    def test_do_not_strip_mid_clause(self):
        self.assertEqual(strip_final_short_vowels("البحرُ هادئٌ"), "البحرُ هادئ")

    def test_count(self):
        before = "القمرُ."
        result = strip_final_short_vowels(before)
        self.assertEqual(count_removed_marks(before, result), 1)

    def test_tanween_written_after_alif_is_removed(self):
        # Unicode texts differ in whether fathatan occurs before or after alif.
        self.assertEqual(strip_final_short_vowels("جميلاً."), "جميلا.")

    def test_multiple_lines_preserve_spacing(self):
        self.assertEqual(strip_final_short_vowels("النَّهارُ.  \nاللَّيلُ؟"), "النَّهار.  \nاللَّيل؟")

    def test_keep_nonfinal_marks_in_quote(self):
        self.assertEqual(strip_final_short_vowels('«سَمِعَ الطفلُ.»'), '«سَمِعَ الطفل.»')

    def test_repeated_processing_is_idempotent(self):
        text = "القَمَرُ. وَنَسيمٌ لَطيفٌ!"
        once = strip_final_short_vowels(text)
        self.assertEqual(once, strip_final_short_vowels(once))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            strip_final_short_vowels(None)
