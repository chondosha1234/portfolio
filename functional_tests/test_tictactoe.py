from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class TicTacToeTest(FunctionalTest):

    def test_tic_tac_toe_game(self):

        # user goes to home page and sees tic tac toe game link
        # user clicks link and is taken to tic tac toe page

        # user sees a page with text input for 2 player names
        # there is a button that says start game

        # user enters player 1 and player 2 names
        # user presses start game button

        # user is taken to game board
        # it says tic tac toe at top

        # it says it is {player1}'s turn

        # user clicks a box for player one and an X appears

        # at bottom of board it now says it is {player2}'s turn

        # user clicks a different box and an O appears

        # user alternates player turns until player1 (X) wins 

        # now it says Player {player1} has won!

        # user sees button that says 'restart' and presses it

        # board is cleared and it is a fresh game with the same players

        # user sees button that says 'new game' and clicks it

        # user is returned to player name entry page
        pass
