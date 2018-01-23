# ChessAI

Chess AI python app

I decided to write a Chess AI program for fun. It turns out that writing a Chess program is not simple. Chess has 6 different pieces with very different moves (L-shape, diagonal, vertical, horizontal) and there are extremely large number of possible moves that can be made by player for each pieces. I first implemented this ChessAI using arrays of arrays. This is a naive way as the run time is simply too big since we will need to check for each square tiles until we found a colliding piece. I scrapped the whole thing and rewrite it using the concept of bitboards, and it works extremely well. Due to the large possible moves that can be made by player each turn, I decided to use Principal Variation Search/ Negascout, an "upgraded version of minimax with Alpha-Beta pruning" to find the best move. Principal Variation Search treats the first legal move as the best move and searches it thoroughly; for the remaning legal moves, Principal Variation Search does a quick search to ensure that it is lesser or equal (not better) to the first legal move. The AI takes an average of 5 seconds to choose the best move each turn.

Run (with Tkinter GUI):
`./chessAI.py`

![chessAI_GUI]
(https://github.com/fzy1995/ChessAI/blob/master/chessAI_GUI.png)

