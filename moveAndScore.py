#!/usr/bin/env python3

"""
@author: Foo Zhi Yuan
ChessAI is being implemented using the concepts of bitboard and principal variation search
Requires Python 3 and Pillow(for GUI)
USAGE: python chessAI.py
"""

class MoveAndScore:
	move=None
	score=None

	def __init__(self,move,score):
		self.move=move
		self.score=score