from django.test import TestCase

class TicTacToeViewsTest(TestCase):

    def test_renders_start_page(self):
        response = self.client.get('/tictactoe/')
        self.assertEquals(response.templates[0].name, 'tictactoe_start.html')
        self.assertTemplateUsed(response, 'tictactoe_start.html')

    def test_POST_renders_game_page(self):
        response = self.client.post('/tictactoe/game', data={
            "textx": "Jon",
            "texto": "Dasha"
        })
        self.assertEquals(response.templates[0].name, 'tictactoe.html')
        self.assertTemplateUsed(response, 'tictactoe.html')

    
