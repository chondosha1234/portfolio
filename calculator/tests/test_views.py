from django.test import TestCase


class CalculatorViewTest(TestCase):

    def test_renders_calculator_page(self):
        response = self.client.get('/calculator/')
        self.assertEquals(response.templates[0].name, 'calculator.html')
        self.assertTemplateUsed(response, 'calculator.html')
