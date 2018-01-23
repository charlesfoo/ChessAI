#!/usr/bin/env python3

"""
@author: Foo Zhi Yuan
ChessAI implemented using the concepts of bitboard and principal variation search
Requires Python 3 and Pillow(for GUI)
USAGE: python chessAI.py to play in GUI and python chessAI_console.py to play in console
"""

"""
encoding utf-8
chess pieces unicode credits to https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode
"""

from moves import Moves
from PawnPromotionPieceNotDefinedError import PawnPromotionPieceNotDefinedError

class Board:
	#white pieces bitboard
	whiteKing=0 #white king
	whiteQueen=0 #white queen
	whiteBishop=0 #white bishop
	whiteKnight=0 #white horse
	whiteRook=0 #white rook
	whitePawn=0 #white pawn
	#black pieces bitboard
	blackKing=0 #black king
	blackQueen=0 #black queen
	blackBishop=0 #black bishop
	blackKnight=0 #black horse
	blackRook=0 #black rook
	blackPawn=0 #black pawn
	#castling
	whiteQueenCastle=True
	whiteKingCastle=True
	blackQueenCastle=True
	blackKingCastle=True

	history=None
	currentAllLegalMoves=None
	Moves=None
	playerIsWhite=None
	chessBoard=None

	#initChess reset chessBoard to its original state
	def initChess(self,Moves,playerIsWhite,gui=False):
		self.history=""
		#white pieces bitboard
		self.whiteKing=0;self.whiteQueen=0;self.whiteBishop=0;self.whiteKnight=0;self.whiteRook=0;self.whitePawn=0
		#black pieces bitboard
		self.blackKing=0;self.blackQueen=0;self.blackBishop=0;self.blackKnight=0;self.blackRook=0;self.blackPawn=0
		#castling
		self.whiteQueenCastle=True;self.whiteKingCastle=True;self.blackQueenCastle=True;self.blackKingCastle=True
		self.currentAllLegalMoves=[]
		self.Moves=Moves
		self.playerIsWhite=playerIsWhite

		chessBoard=[
		["r","h","b","q","k","b","h","r"], #0
		["p","p","p","p","p","p","p","p"], #1
		[" "," "," "," "," "," "," "," "], #2
		[" "," "," "," "," "," "," "," "], #3
		[" "," "," "," "," "," "," "," "], #4
		[" "," "," "," "," "," "," "," "], #5
		["P","P","P","P","P","P","P","P"], #6
		["R","H","B","Q","K","B","H","R"]] #7
		# 0   1   2   3   4   5   6   7
		
		##For debugging
		# chessBoard=[
		# ["r","h","b","q","k"," "," "," "], #0
		# ["p","p","p","p","p"," ","Q"," "], #1
		# [" "," "," "," "," "," "," "," "], #2
		# [" "," "," "," "," "," "," "," "], #3
		# [" "," "," "," "," "," "," ","Q"], #4
		# [" "," "," "," "," "," "," "," "], #5
		# ["P","P","P","P","P","P","P","P"], #6
		# ["R","H","B","Q","K","B","H","R"]] #7
		# # 0   1   2   3   4   5   6   7

		# chessBoard=[
		# ["r","h","b","q","k","b"," ","r"], #0
		# ["p","p","p","p","p","p","P","p"], #1
		# [" "," "," "," "," "," "," "," "], #2
		# [" "," "," "," "," "," "," "," "], #3
		# [" "," "," "," "," "," "," "," "], #4
		# [" "," "," "," "," "," "," "," "], #5
		# ["P","P","P","P","P","P","P","P"], #6
		# ["R","H","B","Q","K","B","H","R"]] #7
		# # 0   1   2   3   4   5   6   7
		self.convertArrayOfChessToBitBoards(chessBoard,gui)
		##For debugging
		# move=Moves()
		# move.white_legalMoves("1636",self.whiteKing,self.whiteQueen,self.whiteBishop,self.whiteKnight,self.whiteRook,self.whitePawn,self.blackKing,self.blackQueen,self.blackBishop,self.blackKnight,self.blackRook,self.blackPawn,self.whiteQueenCastle,self.whiteKingCastle,self.blackQueenCastle,self.blackKingCastle)
		# self.flipBoard()
		# self.flipBoard()
		# self.drawBoard()

	#type chessBoard: array of array
	#note:
	#A board of
	#10000000
	#00000000
	#00000000
	#00000000
	#00000000
	#00000000
	#00000000
	#00000000 
	#corresponds to 0000000000000000000000000000000000000000000000000000000000000001
	def convertArrayOfChessToBitBoards(self,chessBoard,gui):
		pieceMap={"K":"whiteKing","Q":"whiteQueen","B":"whiteBishop","H":"whiteKnight","R":"whiteRook","P":"whitePawn",
		"k":"blackKing","q":"blackQueen","b":"blackBishop","h":"blackKnight","r":"blackRook","p":"blackPawn"}
		for i in range(64):
			binary="0"*64
			#if pawn piece is at (0,0), the idea is that after I right shift by a, eg: >> a, chessBoard[a/8][a%8] is the pawn piece
			binary=binary[i+1:]+"1"+binary[0:i]
			pieceAbbr=chessBoard[i//8][i%8]

			#white bitboards
			if(pieceAbbr=="K"): self.whiteKing=self.whiteKing+int(binary,2)
			elif(pieceAbbr=="Q"): self.whiteQueen=self.whiteQueen+int(binary,2)
			elif(pieceAbbr=="B"): self.whiteBishop=self.whiteBishop+int(binary,2)
			elif(pieceAbbr=="H"): self.whiteKnight=self.whiteKnight+int(binary,2)
			elif(pieceAbbr=="R"): self.whiteRook=self.whiteRook+int(binary,2)
			elif(pieceAbbr=="P"): self.whitePawn=self.whitePawn+int(binary,2)
			#black bitboards
			elif(pieceAbbr=="k"): self.blackKing=self.blackKing+int(binary,2)
			elif(pieceAbbr=="q"): self.blackQueen=self.blackQueen+int(binary,2)
			elif(pieceAbbr=="b"): self.blackBishop=self.blackBishop+int(binary,2)
			elif(pieceAbbr=="h"): self.blackKnight=self.blackKnight+int(binary,2)
			elif(pieceAbbr=="r"): self.blackRook=self.blackRook+int(binary,2)
			elif(pieceAbbr=="p"): self.blackPawn=self.blackPawn+int(binary,2)

		#if this is for console, we will need to draw the initial board to present to player
		if(gui==False):
			self.drawBoard(self.playerIsWhite)
		#if this is for GUI, 
		else:
			self.updateChessBoard()



	#type bitBoards: dictionary
	def drawBoard(self,playerIsWhite):
		#if player is black, we need to present black pieces at bottom, white pieces on top
		boardFlipped=False
		if(not playerIsWhite):
			self.flipBoard()
			boardFlipped=True

		board=[[" " for i in range(8)] for j in range(8)]

		for i in range(64):
			#white pieces
			if( ((self.whiteKing>>i)&1)==1 ): board[i//8][i%8]=u'♔'
			elif( ((self.whiteQueen>>i)&1)==1 ): board[i//8][i%8]=u'♕'
			elif( ((self.whiteBishop>>i)&1)==1 ): board[i//8][i%8]=u'♗'
			elif( ((self.whiteKnight>>i)&1)==1 ): board[i//8][i%8]=u'♘'	
			elif( ((self.whiteRook>>i)&1)==1 ): board[i//8][i%8]=u'♖'
			elif( ((self.whitePawn>>i)&1)==1 ): board[i//8][i%8]=u'♙'	
			#black pieces
			elif( ((self.blackKing>>i)&1)==1 ): board[i//8][i%8]=u'♚'
			elif( ((self.blackQueen>>i)&1)==1 ): board[i//8][i%8]=u'♛'
			elif( ((self.blackBishop>>i)&1)==1 ): board[i//8][i%8]=u'♝'
			elif( ((self.blackKnight>>i)&1)==1 ): board[i//8][i%8]=u'♞'
			elif( ((self.blackRook>>i)&1)==1 ): board[i//8][i%8]=u'♜'
			elif( ((self.blackPawn>>i)&1)==1 ): board[i//8][i%8]=u'♟'

		print("")
		for i in range(8):
			print("  "+str(7-i+1)+"   ",end="")
			# print("[",end="")
			for j in range(8):
				if(j!=7):
					# print(board[i][j],",",end="")
					print(board[i][j],",",end="")
				else:
					print(board[i][j],end="")
			# print("]",end="")
			print("")
		print("      -----------------------")
		print("       a  b  c  d  e  f  g  h")
		print("")

		#if player is black, we need to convert our chessBoard back to its internal format of white at bottom, black on top
		if(boardFlipped==True):
			self.flipBoard()
			boardFlipped=False

	#update arrays of arrays chessBoard to represent current state of 12 bit boards.
	#Used only by GUI.
	#note: DO NOT MODIFY self.chessBoard
	def updateChessBoard(self):
		boardFlipped=False
		if(not self.playerIsWhite):
			self.flipBoard()
			boardFlipped=True

		board=[[" " for i in range(8)] for j in range(8)]

		for i in range(64):
			#white pieces
			if( ((self.whiteKing>>i)&1)==1 ): board[i//8][i%8]="K"
			elif( ((self.whiteQueen>>i)&1)==1 ): board[i//8][i%8]="Q"
			elif( ((self.whiteBishop>>i)&1)==1 ): board[i//8][i%8]="B"
			elif( ((self.whiteKnight>>i)&1)==1 ): board[i//8][i%8]="H"
			elif( ((self.whiteRook>>i)&1)==1 ): board[i//8][i%8]="R"
			elif( ((self.whitePawn>>i)&1)==1 ): board[i//8][i%8]="P"	
			#black pieces
			elif( ((self.blackKing>>i)&1)==1 ): board[i//8][i%8]="k"
			elif( ((self.blackQueen>>i)&1)==1 ): board[i//8][i%8]="q"
			elif( ((self.blackBishop>>i)&1)==1 ): board[i//8][i%8]="b"
			elif( ((self.blackKnight>>i)&1)==1 ): board[i//8][i%8]="h"
			elif( ((self.blackRook>>i)&1)==1 ): board[i//8][i%8]="r"
			elif( ((self.blackPawn>>i)&1)==1 ): board[i//8][i%8]="p"

		#if player is black, we need to convert our chessBoard back to its internal format of white at bottom, black on top
		if(boardFlipped==True):
			self.flipBoard()
			boardFlipped=False

		self.chessBoard=board

	#type board: int
	def reverse(self,board):
		binary=format(board,"064b")
		binary=binary[::-1]
		return int(binary,2)

	#Given current state of chessBoard, update the global variable currentAllLegalMoves with all legal moves that can be performed by current player.
	def getAllCurrentLegalMoves(self,whiteTurn):
		Moves=self.Moves

		if(whiteTurn):
			moves=Moves.white_legalMoves(self.history,self.whiteKing,self.whiteQueen,self.whiteBishop,self.whiteKnight,self.whiteRook,self.whitePawn,self.blackKing,self.blackQueen,self.blackBishop,self.blackKnight,self.blackRook,self.blackPawn,self.whiteQueenCastle,self.whiteKingCastle,self.blackQueenCastle,self.blackKingCastle)
		else:
			moves=Moves.black_legalMoves(self.history,self.whiteKing,self.whiteQueen,self.whiteBishop,self.whiteKnight,self.whiteRook,self.whitePawn,self.blackKing,self.blackQueen,self.blackBishop,self.blackKnight,self.blackRook,self.blackPawn,self.whiteQueenCastle,self.whiteKingCastle,self.blackQueenCastle,self.blackKingCastle)

		moves=moves.split()
		li=[]
		for i in range(len(moves)):
			currentMove=moves[i]
			#white pieces
			tempWhiteKing=Moves.makeMove(self.whiteKing,currentMove,"K")
			tempWhiteQueen=Moves.makeMove(self.whiteQueen,currentMove,"Q")
			tempWhiteBishop=Moves.makeMove(self.whiteBishop,currentMove,"B")
			tempWhiteKnight=Moves.makeMove(self.whiteKnight,currentMove,"H")
			tempWhiteRook=Moves.makeMove(self.whiteRook,currentMove,"R")
			tempWhitePawn=Moves.makeMove(self.whitePawn,currentMove,"P")
			#if castling, make castling move
			if("WL" in currentMove or "WR" in currentMove):
				tempWhiteKing,tempWhiteRook=Moves.makeCastlingMove(self.whiteKing,self.whiteRook,currentMove)
			#black pieces
			tempBlackKing=Moves.makeMove(self.blackKing,currentMove,"k")
			tempBlackQueen=Moves.makeMove(self.blackQueen,currentMove,"q")
			tempBlackBishop=Moves.makeMove(self.blackBishop,currentMove,"b")
			tempBlackKnight=Moves.makeMove(self.blackKnight,currentMove,"h")
			tempBlackRook=Moves.makeMove(self.blackRook,currentMove,"r")
			tempBlackPawn=Moves.makeMove(self.blackPawn,currentMove,"p")
			if("BL" in currentMove or "BR" in currentMove):
				tempBlackKing,tempBlackRook=Moves.makeCastlingMove(self.blackKing,self.blackRook,currentMove)
			tempHistory=currentMove

			if(whiteTurn):
				if((tempWhiteKing&Moves.whiteKing_illegalMoves(tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn))==0):
					li.append(currentMove)
			elif(not whiteTurn):
				if((tempBlackKing&Moves.blackKing_illegalMoves(tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn))==0):
					li.append(currentMove)
		
		self.currentAllLegalMoves=li


	#update the move on the chessBoard.
	#IMPORTANT: Need to call getAllCurrentLegalMoves BEFORE calling updateMove
	def updateMove(self,move,gui=False):
		Moves=self.Moves
		##For debugging
		# print("The move you entered is "+move)
		if(len(move)<4):
			raise ValueError("Error in updateMove: the move entered is not a valid move.")

		currentMove=None
		for i in range(len(self.currentAllLegalMoves)):
			#if player input a move of length 4, this move CANNOT automatically fulfill pawn promotion moves as player needs to choose the piece for promotion
			if(move in self.currentAllLegalMoves[i]):
				if(len(move)==4):
					if(len(self.currentAllLegalMoves[i])>4):
						#if this is not a pawn promotion move, and is just castling or en passant move, assign the golden standard move to current move
						if(self.currentAllLegalMoves[i][5]!="P"):
							currentMove=self.currentAllLegalMoves[i]
						#if THIS IS A PAWN PROMOTION MOVE, raise Error since pawn promotion piece is not specified
						else:
							if(gui==True):
								raise PawnPromotionPieceNotDefinedError("Error in updateMove: pawn promotion piece is not defined.")
							else:
								pass
					#if this is not a pawn promotion move, and is just normal move, assign the golden standard move to current move
					else:
						currentMove=self.currentAllLegalMoves[i]
				elif(len(move)>4):
					currentMove=self.currentAllLegalMoves[i]
		if(currentMove==None):
			raise ValueError("Error in updateMove; the move entered is not a valid move.")

		try:
			originalX=int(currentMove[0])
			originalY=int(currentMove[1])
			newX=int(currentMove[2])
			newY=int(currentMove[3])
		except(ValueError):
			raise ValueError("Error in updateMove: the first four character of move string must be integer.")

		start=(originalX*8)+originalY
		end=(newX*8)+newY

		#white pieces
		tempWhiteKing=Moves.makeMove(self.whiteKing,currentMove,"K")
		tempWhiteQueen=Moves.makeMove(self.whiteQueen,currentMove,"Q")
		tempWhiteBishop=Moves.makeMove(self.whiteBishop,currentMove,"B")
		tempWhiteKnight=Moves.makeMove(self.whiteKnight,currentMove,"H")
		tempWhiteRook=Moves.makeMove(self.whiteRook,currentMove,"R")
		tempWhitePawn=Moves.makeMove(self.whitePawn,currentMove,"P")
		#if castling, make castling move
		if("WL" in currentMove or "WR" in currentMove):
			tempWhiteKing,tempWhiteRook=Moves.makeCastlingMove(self.whiteKing,self.whiteRook,currentMove)
		#black pieces
		tempBlackKing=Moves.makeMove(self.blackKing,currentMove,"k")
		tempBlackQueen=Moves.makeMove(self.blackQueen,currentMove,"q")
		tempBlackBishop=Moves.makeMove(self.blackBishop,currentMove,"b")
		tempBlackKnight=Moves.makeMove(self.blackKnight,currentMove,"h")
		tempBlackRook=Moves.makeMove(self.blackRook,currentMove,"r")
		tempBlackPawn=Moves.makeMove(self.blackPawn,currentMove,"p")
		if("BL" in currentMove or "BR" in currentMove):
			tempBlackKing,tempBlackRook=Moves.makeCastlingMove(self.blackKing,self.blackRook,currentMove)
		tempHistory=currentMove

		###update castling variables
		#copy castling variables from previous
		tempWhiteQueenCastle=self.whiteQueenCastle
		tempWhiteKingCastle=self.whiteKingCastle
		tempBlackQueenCastle=self.blackQueenCastle
		tempBlackKingCastle=self.blackKingCastle

		#update castling variable based on the currentMove we made
		#if currentMove is making white castling move, we can no longer castle again for white
		if("WL" in currentMove or "WR" in currentMove):
			tempWhiteQueenCastle=False
			tempWhiteKingCastle=False
		#if currentMove is making black castling move, we can no longer castle again for black
		elif("BL" in currentMove or "BR" in currentMove):
			tempBlackQueenCastle=False
			tempBlackKingCastle=False
		else:
			#if currentMove is moving whiteKing, white queen and king side castle become False
			if(((1<<start)&self.whiteKing)!=0):
				tempWhiteQueenCastle=False
				tempWhiteKingCastle=False
			#if currentMove is moving blackKing, black queen and king side castle become False
			elif(((1<<start)&self.blackKing)!=0):
				tempBlackQueenCastle=False
				tempBlackKingCastle=False
			#if currentMove is moving white left rook, white queenside castling become False
			elif(((1<<start)&self.whiteRook&(1<<56))!=0):
				tempWhiteQueenCastle=False
			#if currentMove is moving white right rook, white kingside castling become False
			elif(((1<<start)&self.whiteRook&(1<<63))!=0):
				tempWhiteKingCastle=False
			elif(((1<<start)&self.blackRook&(1<<0))!=0):
				tempBlackQueenCastle=False
			elif(((1<<start)&self.blackRook&(1<<7))!=0):
				tempBlackKingCastle=False

		#update history
		self.history=tempHistory
		#update white pieces
		self.whiteKing=tempWhiteKing
		self.whiteQueen=tempWhiteQueen
		self.whiteBishop=tempWhiteBishop
		self.whiteKnight=tempWhiteKnight
		self.whiteRook=tempWhiteRook
		self.whitePawn=tempWhitePawn
		#update black pieces
		self.blackKing=tempBlackKing
		self.blackQueen=tempBlackQueen
		self.blackBishop=tempBlackBishop
		self.blackKnight=tempBlackKnight
		self.blackRook=tempBlackRook
		self.blackPawn=tempBlackPawn
		#update castling variables
		self.whiteQueenCastle=tempWhiteQueenCastle
		self.whiteKingCastle=tempWhiteKingCastle
		self.blackQueenCastle=tempBlackQueenCastle
		self.blackKingCastle=tempBlackKingCastle

		#if gui is True, we also need to update our chessBoard (arrays of arrays)
		if(gui==True):
			self.updateChessBoard()
		#if gui is False, we don't need to update our chessBoard (arrays of arrays) since we will call the drawBoard method in chessAI_console
		else:
			pass


	#flip the board
	#note: white pieces at the top of the board, black pieces at the bottom of the board. 
	#This method is being used to present to player if player plays as black.
	#IMPORTANT: Need to call getAllCurrentLegalMoves BEFORE calling flipBoard.
	def flipBoard(self):
		self.whiteKing=self.reverse(self.whiteKing)
		self.whiteQueen=self.reverse(self.whiteQueen)
		self.whiteBishop=self.reverse(self.whiteBishop)
		self.whiteKnight=self.reverse(self.whiteKnight)
		self.whiteRook=self.reverse(self.whiteRook)
		self.whitePawn=self.reverse(self.whitePawn)

		self.blackKing=self.reverse(self.blackKing)
		self.blackQueen=self.reverse(self.blackQueen)
		self.blackBishop=self.reverse(self.blackBishop)
		self.blackKnight=self.reverse(self.blackKnight)
		self.blackRook=self.reverse(self.blackRook)
		self.blackPawn=self.reverse(self.blackPawn)

		# tempKing=self.whiteKing
		# tempQueen=self.whiteQueen
		# tempBishop=self.whiteBishop
		# tempKnight=self.whiteKnight
		# tempRook=self.whiteRook
		# tempPawn=self.whitePawn

		# self.whiteKing=self.blackKing
		# self.whiteQueen=self.blackQueen
		# self.whiteBishop=self.blackBishop
		# self.whiteKnight=self.blackKnight
		# self.whiteRook=self.blackRook
		# self.whitePawn=self.blackPawn

		# self.blackKing=tempKing
		# self.blackQueen=tempQueen
		# self.blackBishop=tempBishop
		# self.blackKnight=tempKnight
		# self.blackRook=tempRook
		# self.blackPawn=tempPawn

