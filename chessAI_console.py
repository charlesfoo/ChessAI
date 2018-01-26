#!/usr/bin/env python3

"""
@author: Foo Zhi Yuan
ChessAI is being implemented using the concepts of bitboard and principal variation search
Requires Python 3 and Pillow(for GUI)
USAGE: python chessAI.py to play in GUI and python chessAI_console.py to play in console
"""

from board import Board
from rating import Rating
from moves import Moves
from principalVariation import PrincipalVariation
from PawnPromotionPieceNotDefinedError import PawnPromotionPieceNotDefinedError
import math

class chessAI_console:
	playerIsWhite=None
	maxDepth=None
	whiteTurn=None


	def start(self):
		self.maxDepth=3
		self.whiteTurn=True
		print("GAME START")
		print("Would you like to play as white or black?")
		while(True):
			playerColour=input("Player colour: ")
			if(playerColour.lower()=="white" or playerColour.lower()=="black"):
				break
			else:
				print("Please input white or black.")

		if(playerColour.lower()=="white"):
			self.playerIsWhite=True
		else:
			self.playerIsWhite=False
		print("")
		print("Input the board position to make your move.")
		print("Eg: g8a1, e3e8, a1a8, h1a8, d7d8 Queen")
		print("Input q or quit to end game.")

	#convert move entered by player to move recognised by internal board.
	#if player is black, we present black pieces at the bottom of the board and white pieces at the top of the board to player.
	#however, our internal board is built with white pieces at the bottom and black pieces at the top, with the format of 0 to 7 at y axis from top to bottom. 
	#We need to thus convert the move entered by player to match the corresponding move in internal move, as our internal board has y axis from 0 to 7 at y axis
	#from top to bottom
	def convertMoveEnteredToInternalNumericalMove(self,moveEntered):
		if(len(moveEntered)<4):
			raise ValueError("The move entered is invalid. Please input the board position to make your move. Eg: g8a1, a1a8, e3e8, d7d8 Queen")
		if(len(moveEntered)>4):
			if(moveEntered[4]!=" "):
				raise ValueError("The move entered is invalid. Please input the board position to make your move. Eg: g8a1, a1a8, e3e8. \nTo make pawn promotion move, do: d7d8 Queen, b7a8 Rook, g7h8 Knight")
			if(moveEntered[5:].lower()!="queen" and moveEntered[5:].lower()!="bishop" and moveEntered[5:].lower()!="knight" and moveEntered[5:].lower()!="rook"):
				raise ValueError("The move entered is invalid. Please input the board position to make your move. Eg: g8a1, a1a8, e3e8. \nTo make pawn promotion move, do: d7d8 Queen, b7a8 Rook, g7h8 Knight")
			
		move=""
		pawnPromotionMove=None

		moveEntered=moveEntered.lower()
		if(len(moveEntered)>4):
			pawnPromotionMove=moveEntered[5:]

		if(moveEntered[0]!="a" and moveEntered[0]!="b" and moveEntered[0]!="c" and moveEntered[0]!="d" and moveEntered[0]!="e" and moveEntered[0]!="f" and moveEntered[0]!="g" and moveEntered[0]!="h"):
			raise ValueError("The move entered is invalid. Please input the board position to make your move. Eg: g8a1, a1a8, e3e8")
		if(moveEntered[1]!="1" and moveEntered[1]!="2" and moveEntered[1]!="3" and moveEntered[1]!="4" and moveEntered[1]!="5" and moveEntered[1]!="6" and moveEntered[1]!="7" and moveEntered[1]!="8"):
			raise ValueError("The move entered is invalid. Please input the board position to make your move. Eg: g8a1, a1a8, e3e8")
		if(moveEntered[2]!="a" and moveEntered[2]!="b" and moveEntered[2]!="c" and moveEntered[2]!="d" and moveEntered[2]!="e" and moveEntered[2]!="f" and moveEntered[2]!="g" and moveEntered[2]!="h"):
			raise ValueError("The move entered is invalid. Please input the board position to make your move. Eg: g8a1, a1a8, e3e8")
		if(moveEntered[3]!="1" and moveEntered[3]!="2" and moveEntered[3]!="3" and moveEntered[3]!="4" and moveEntered[3]!="5" and moveEntered[3]!="6" and moveEntered[3]!="7" and moveEntered[3]!="8"):
			raise ValueError("The move entered is invalid. Please input the board position to make your move. Eg: g8a1, a1a8, e3e8")

		x_axisMap={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}

		originalX=x_axisMap[moveEntered[0]]
		originalY=int(moveEntered[1])-1
		newX=x_axisMap[moveEntered[2]]
		newY=int(moveEntered[3])-1


		#since the board we presented to the player has y axis from 8 to 1 at y axis from top to bottom, we need to convert it to match the internal board format
		#which is 0 to 7 at y axis from top to bottom.
		if(self.playerIsWhite):
			originalY=7-originalY
			newY=7-newY
			if(pawnPromotionMove!=None):
				pawnPromotionMap={"queen":"Q","bishop":"B","knight":"H","rook":"R"}
				pawnPromotionMove=pawnPromotionMap[pawnPromotionMove]+"P"

		#if player is black, we present black pieces at the bottom of the board and white pieces at the top of the board to player
		#however, our internal board is built with white pieces at the bottom and black pieces at the top, with the format of 0 to 7 at y axis from top to bottom.
		#we will thus need to convert move input by player when player is black to corresponding move in internal board.
		if(not self.playerIsWhite):
			originalX=7-originalX
			newX=7-newX
			if(pawnPromotionMove!=None):
				pawnPromotionMap={"queen":"q","bishop":"b","knight":"h","rook":"r"}
				pawnPromotionMove=pawnPromotionMap[pawnPromotionMove]+"P"

		temp=originalX
		originalX=originalY
		originalY=temp

		temp=newX
		newX=newY
		newY=temp

		if(pawnPromotionMove==None):
			move=str(originalX)+str(originalY)+str(newX)+str(newY)
		else:
			move=str(originalX)+str(originalY)+str(newX)+str(newY)+pawnPromotionMove

		return move

	def convertInternalNumericalMoveToBoardMove(self,move):
		originalX=int(move[0])
		originalY=int(move[1])
		newX=int(move[2])
		newY=int(move[3])

		x_axisMap={0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}

		temp=originalX
		originalX=originalY
		originalY=temp

		temp=newX
		newX=newY
		newY=temp

		if(self.playerIsWhite):
			originalX=x_axisMap[originalX]
			originalY=7-originalY+1
			newX=x_axisMap[newX]
			newY=7-newY+1
		elif(not self.playerIsWhite):
			originalX=x_axisMap[7-originalX]
			originalY=originalY+1
			newX=x_axisMap[7-newX]
			newY=newY+1

		result=str(originalX)+str(originalY)+str(newX)+str(newY)
		return result


	def main(self):
		self.start()
		moves=Moves()
		principalVariation=PrincipalVariation(moves,self.playerIsWhite,self.maxDepth)
		board=Board()
		board.initChess(moves,self.playerIsWhite)

		if(self.playerIsWhite):
			player="W"
			opponent="B"
		else:
			player="B"
			opponent="W"
		board.getAllCurrentLegalMoves(self.whiteTurn)

		while(len(board.currentAllLegalMoves)>0):
			#if it is player's turn
			if(self.playerIsWhite==self.whiteTurn):
				while(True):
					playerMove=input(player+": ")
					if(playerMove.lower()=="quit" or playerMove.lower()=="q"):
						print("Computer wins.")
						exit(0)
					try:
						playerMove=self.convertMoveEnteredToInternalNumericalMove(playerMove)
						board.updateMove(playerMove)
						break
					except ValueError as e:
						print(str(e))
				board.drawBoard(self.playerIsWhite)
				self.whiteTurn=not self.whiteTurn
				board.getAllCurrentLegalMoves(self.whiteTurn)
			#if it is opponent's turn
			else:
				print("Computer is thinking ......")
				bestScore,bestMove=principalVariation.principalVariationSearch(-math.inf,math.inf,board.history,board.whiteKing,board.whiteQueen,board.whiteBishop,board.whiteKnight,board.whiteRook,board.whitePawn,board.blackKing,board.blackQueen,board.blackBishop,board.blackKnight,board.blackRook,board.blackPawn,board.whiteQueenCastle,board.whiteKingCastle,board.blackQueenCastle,board.blackKingCastle,self.whiteTurn,0)
				if(bestMove=="No Move"):
					break
				board.updateMove(bestMove)
				print(opponent+": "+self.convertInternalNumericalMoveToBoardMove(bestMove))
				board.drawBoard(self.playerIsWhite)
				self.whiteTurn=not self.whiteTurn
				board.getAllCurrentLegalMoves(self.whiteTurn)

			##For debugging
			# if(self.whiteTurn):
			# 	currentPlayer="White"
			# else:
			# 	currentPlayer="Black"

			# print("Now it is "+currentPlayer+"'s turn")
			# print(board.currentAllLegalMoves)
		if(self.whiteTurn==self.playerIsWhite):
			print("Computer wins.")
		else:
			print("Player wins.")






chessAI_console=chessAI_console()
chessAI_console.main()
		

	