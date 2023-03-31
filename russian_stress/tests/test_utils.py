from django.test import TestCase
from russian_stress.utils import add_stress

class AddStressTest(TestCase):

    def test_add_stress_returns_string_of_words(self):
        text = "В Москве состоялись переговоры."
        result = add_stress(text)
        self.assertIsInstance(result, str)

    def test_adds_stress_to_words(self):
        text = "В Москве состоялись переговоры между лидерами России и Китая."
        result = add_stress(text)
        self.assertEqual("В Москве́ состоя́лись перегово́ры ме́жду ли́дерами Росси́и и Китая.", result)

    def test_func_keeps_punctuation(self):
        text = "В Москве состоялись переговоры."
        result = add_stress(text)
        self.assertIn('.', result)

    def test_multiple_options_returns_without_stress(self):
        word = "стороны"  # there are 2 possible stress locations if you search this word
        result = add_stress(word)
        self.assertEqual("стороны", result)

    def test_capitalized_word_can_be_found_and_stressed(self):
        word = "Второй"
        result = add_stress(word)
        self.assertEqual("Второ́й", result)
