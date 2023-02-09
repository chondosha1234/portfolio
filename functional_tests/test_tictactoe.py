from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse

from .base import FunctionalTest


class TicTacToeTest(FunctionalTest):

    def test_tic_tac_toe_game(self):

        # user goes to home page and sees tic tac toe game link
        # user clicks link and is taken to tic tac toe page
        self.browser.get(self.live_server_url + reverse('home'))
        self.browser.find_element(By.LINK_TEXT, 'Tic Tac Toe').click()
        self.assertRegex(self.browser.current_url, '/tictactoe/')

        # user sees a page with text input for 2 player names
        player1 = self.browser.find_element(By.ID, 'textx')
        player2 = self.browser.find_element(By.ID, 'texto')
        # there is a button that says start game
        start_btn = self.browser.find_element(By.CLASS_NAME, 'newgame-btn')

        # user enters player 1 and player 2 names
        player1.send_keys("Jon")
        player2.send_keys("Dasha")
        # user presses start game button
        start_btn.click()

        # user is taken to game board
        self.assertRegex(self.browser.current_url, '/tictactoe/game')
        # it says tic tac toe at top
        title = self.browser.find_element(By.CLASS_NAME, 'game-title').text
        self.assertEqual(title, 'Tic Tac Toe')

        # it says it is {player1}'s turn
        turn = self.browser.find_element(By.CLASS_NAME, 'game-status').text
        self.assertEqual(turn, "It is Jon's turn!")

        # user clicks a box for player one and an X appears
        self.browser.find_elements(By.CLASS_NAME, 'cell')[0].click() # top left
        box = self.browser.find_elements(By.CLASS_NAME, 'cell')[0].text
        self.assertEqual(box, 'X')

        # at bottom of board it now says it is {player2}'s turn
        turn = self.browser.find_element(By.CLASS_NAME, 'game-status').text
        self.assertEqual(turn, "It is Dasha's turn!")

        # user clicks a different box and an O appears
        self.browser.find_elements(By.CLASS_NAME, 'cell')[1].click() # top middle
        box = self.browser.find_elements(By.CLASS_NAME, 'cell')[1].text
        self.assertEqual(box, 'O')

        # user alternates player turns until player1 (X) wins
        self.browser.find_elements(By.CLASS_NAME, 'cell')[3].click() # left middle
        self.browser.find_elements(By.CLASS_NAME, 'cell')[2].click() # right top
        self.browser.find_elements(By.CLASS_NAME, 'cell')[6].click() # left bottom

        # now it says Player {player1} has won!
        status = self.browser.find_element(By.CLASS_NAME, 'game-status').text
        self.assertEqual(status, 'Player Jon has won!')

        # user sees button that says 'restart' and presses it
        self.browser.find_element(By.CLASS_NAME, 'restart-btn').click()

        # board is cleared and it is a fresh game with the same players
        box = self.browser.find_elements(By.CLASS_NAME, 'cell')[0].text
        self.assertEqual(box, '')
        turn = self.browser.find_element(By.CLASS_NAME, 'game-status').text
        self.assertEqual(turn, "It is Jon's turn!")

        # user goes through game with no winner
        self.browser.find_elements(By.CLASS_NAME, 'cell')[0].click()
        self.browser.find_elements(By.CLASS_NAME, 'cell')[2].click()
        self.browser.find_elements(By.CLASS_NAME, 'cell')[6].click()
        self.browser.find_elements(By.CLASS_NAME, 'cell')[3].click()
        self.browser.find_elements(By.CLASS_NAME, 'cell')[1].click()
        self.browser.find_elements(By.CLASS_NAME, 'cell')[8].click()
        self.browser.find_elements(By.CLASS_NAME, 'cell')[5].click()
        self.browser.find_elements(By.CLASS_NAME, 'cell')[7].click()
        self.browser.find_elements(By.CLASS_NAME, 'cell')[4].click()

        # at bottom it says game ends in draw
        status = self.browser.find_element(By.CLASS_NAME, 'game-status').text
        self.assertEqual(status, 'Game ended in a draw!')

        # user sees button that says 'new game' and clicks it
        self.browser.find_element(By.CLASS_NAME, 'newgame-btn').click()

        # user is returned to player name entry page
        self.assertRegex(self.browser.current_url, '/tictactoe/')
        player1 = self.browser.find_element(By.ID, 'textx')
        player2 = self.browser.find_element(By.ID, 'texto')
