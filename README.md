# AI-Memory-Game-using-Knowledge-Base
## OBJECTIVE
This game is a remake of the classic Memory game, also known as matching cards game. We tried to make a 2-player game, so that the User and AI can compete against each other. Among the User and AI, the one who gets maximum number of matched cards is declared as the winner.

## ALGORITHM
The main concept of AI behind this game is the use of Knowledge Base. AI uses Knowledge Base to choose cards which increases the chances of winning for AI.

<p align="center">
  <img src="https://media.giphy.com/media/xT1XGZjmprZ5i6Q8M0/giphy.gif">
</p>

### HOW TO PLAY!

1.	Choose your grid size.
2.	A grid of cards of (nxn) dimension is created
3.	The user gets the first chance to choose cards.
4.	If the cards are matched, the user gets another chance to choose cards and the symbols of the matched cards are displayed on the grid. 
5.	Else the symbols of the chosen cards and a warning stating ‘UNMATCH’ is displayed, and chance is passed to the other player i.e., AI.
6.	The cards chosen by the players and their respective symbols are added to the explored set.
7.	Now when AI chooses two cards, it checks if the cards chosen match or else it checks if any of the chosen cards matches with any card in the explored set. 
8.	If any chosen card matches with any card in the explored set, the card is removed from the explored set and symbols of both the cards are displayed on the grid.
9.	Steps 4 to 8 are repeated until all matching pair of cards are found and the player with the most matches WINS!
