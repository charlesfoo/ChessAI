# ChessAI

##### *Implemented in Python 3*

#### Author: **Foo Zhi Yuan**

Being a Chess enthusiast, I decided to write a Chess playing bot program for fun. It turns out that writing a Chess program is not a trivial task. Chess has 6 different pieces with very different moves (L-shape, diagonal, vertical, horizontal) and there are extremely large number of possible moves that can be made by player for each pieces. In addition to that, Chess has a lot of rules like en passant, castling and pawn promotion.

I first implemented this ChessAI using arrays of arrays. This is a naive way as the run time is simply too big. This is because for every piece, we will need to loop through all the square tiles along its moving path until we found a colliding piece. This is extremely inefficient and for a game with such huge number of possible moves, this will severely limit the number of levels we can search. 

I scrapped the whole thing and rewrite it using the concept of ***bitboards***, and it works extremely well. Due to the large possible moves that can be made by player each turn, I decided to use ***Principal Variation Search/ Negascout***, an "upgraded version of minimax with Alpha-Beta pruning" to find the best move. Unlike minimax with Alpha Beta pruning, Principal Variation Search always treat the first legal move as the best move and searches it thoroughly; as for the remaning legal moves, Principal Variation Search does a quick search using zero/null window search to ensure that it is lesser or equal (not better) to the first legal move. In order to reduce the number of researching the branches of the game tree, a good sorting function is extremely important. 

The AI takes an average of 5 seconds to choose the best move each turn.

### Dependencies
1. Python 3

2. Tkinter

3. Pillow

*Note: (For Ubuntu/ Debian machines) If you encounter "ImportError: cannot import name ImageTk" when running the program*

  *Trying doing:*

  `sudo apt-get install python-imaging python-imaging-tk`

  *For Python 3, do:*

  `sudo apt-get install python3-pil python3-pil.imagetk`


### Run (with Tkinter GUI):

`./chessAI.py`

![chessAI_GUI](https://github.com/fzy1995/ChessAI/blob/master/chessAI_GUI.png)


### Run (on Console):
`./chessAI_console.py`
![chessAI_console](https://github.com/fzy1995/ChessAI/blob/master/chessAI_console.png)

**Select player colour:** Type "white" or "black"

**Make normal move:** <old X, old Y, new X, new Y>. For example: a1a8,a6a3

**Make pawn promotion move:** <old X, old Y, newX, new Y, space, piece to promote>. For example: a7a8 Queen
