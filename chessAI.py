#!/usr/bin/env python3

"""
@author: Foo Zhi Yuan
ChessAI implemented using the concepts of bitboard and principal variation search
Requires Python 3 and Pillow(for GUI)
USAGE: python chessAI.py to play in GUI and python chessAI_console.py to play in console
"""

from graphicalUserInterface import GraphicalUserInterface

class chessAI:
	gui=GraphicalUserInterface()
	gui.main()