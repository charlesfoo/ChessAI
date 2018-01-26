#!/usr/bin/env python3

"""
@author: Foo Zhi Yuan
ChessAI is being implemented using the concepts of bitboard and principal variation search
Requires Python 3 and Pillow(for GUI)
USAGE: python chessAI.py to play in GUI and python chessAI_console.py to play in console
"""

import math
from rating import Rating
from moves import Moves
from moveAndScore import MoveAndScore

class PrincipalVariation:
	"""
	Principal Variation/ NegaScout algorithm credits to https://webdocs.cs.ualberta.ca/~mmueller/courses/2014-AAAI-games-tutorial/slides/AAAI-14-Tutorial-Games-3-AlphaBeta.pdf
	"""
	Moves=None
	Rating=None
	playerIsWhite=None
	maxDepth=None

	def __init__(self,Moves,playerIsWhite,maxDepth):
		self.Moves=Moves
		self.Rating=Rating(Moves)
		self.playerIsWhite=playerIsWhite
		self.maxDepth=maxDepth

	def max(self,value1,value2):
		max=value1
		if(value2>max):
			max=value2
		return max

	
	#type moves: list
	#sanitizeMove filters out invalid move in moves. eg: moves that will place current king in checked or being captured. 
	def sanitizeMove(self,moves,history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle,whiteTurn):
		Moves=self.Moves

		moves=moves.split()
		li=[]
		for i in range(len(moves)):
			currentMove=moves[i]
			#white pieces
			tempWhiteKing=Moves.makeMove(whiteKing,currentMove,"K")
			tempWhiteQueen=Moves.makeMove(whiteQueen,currentMove,"Q")
			tempWhiteBishop=Moves.makeMove(whiteBishop,currentMove,"B")
			tempWhiteKnight=Moves.makeMove(whiteKnight,currentMove,"H")
			tempWhiteRook=Moves.makeMove(whiteRook,currentMove,"R")
			tempWhitePawn=Moves.makeMove(whitePawn,currentMove,"P")
			#if castling, make castling move
			if("WL" in currentMove or "WR" in currentMove):
				tempWhiteKing,tempWhiteRook=Moves.makeCastlingMove(whiteKing,whiteRook,currentMove)
			#black pieces
			tempBlackKing=Moves.makeMove(blackKing,currentMove,"k")
			tempBlackQueen=Moves.makeMove(blackQueen,currentMove,"q")
			tempBlackBishop=Moves.makeMove(blackBishop,currentMove,"b")
			tempBlackKnight=Moves.makeMove(blackKnight,currentMove,"h")
			tempBlackRook=Moves.makeMove(blackRook,currentMove,"r")
			tempBlackPawn=Moves.makeMove(blackPawn,currentMove,"p")
			if("BL" in currentMove or "BR" in currentMove):
				tempBlackKing,tempBlackRook=Moves.makeCastlingMove(blackKing,blackRook,currentMove)
			tempHistory=currentMove

			if(whiteTurn):
				if((tempWhiteKing&Moves.whiteKing_illegalMoves(tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn))==0):
					li.append(currentMove)
			elif(not whiteTurn):
				if((tempBlackKing&Moves.blackKing_illegalMoves(tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn))==0):
					li.append(currentMove)
		return li

	def getScore(self,moveAndScore):
		return moveAndScore.score

	def sortMoves(self,moves,history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle,whiteTurn,depth):
		Moves=self.Moves
		Rating=self.Rating

		MoveAndScoreList=[]
		li=[]
		for i in range(len(moves)):
			currentMove=moves[i]

			try:
				originalX=int(currentMove[0])
				originalY=int(currentMove[1])
				newX=int(currentMove[2])
				newY=int(currentMove[3])
			except(ValueError):
				raise ValueError("Error in sortMoves: the first four character of currentMove string must be integer.")

			start=(originalX*8)+originalY
			end=(newX*8)+newY

			##make currentMove
			#white pieces
			tempWhiteKing=Moves.makeMove(whiteKing,currentMove,"K")
			tempWhiteQueen=Moves.makeMove(whiteQueen,currentMove,"Q")
			tempWhiteBishop=Moves.makeMove(whiteBishop,currentMove,"B")
			tempWhiteKnight=Moves.makeMove(whiteKnight,currentMove,"H")
			tempWhiteRook=Moves.makeMove(whiteRook,currentMove,"R")
			tempWhitePawn=Moves.makeMove(whitePawn,currentMove,"P")
			#if castling, make castling move
			if("WL" in currentMove or "WR" in currentMove):
				tempWhiteKing,tempWhiteRook=Moves.makeCastlingMove(whiteKing,whiteRook,currentMove)
			#black pieces
			tempBlackKing=Moves.makeMove(blackKing,currentMove,"k")
			tempBlackQueen=Moves.makeMove(blackQueen,currentMove,"q")
			tempBlackBishop=Moves.makeMove(blackBishop,currentMove,"b")
			tempBlackKnight=Moves.makeMove(blackKnight,currentMove,"h")
			tempBlackRook=Moves.makeMove(blackRook,currentMove,"r")
			tempBlackPawn=Moves.makeMove(blackPawn,currentMove,"p")
			if("BL" in currentMove or "BR" in currentMove):
				tempBlackKing,tempBlackRook=Moves.makeCastlingMove(blackKing,blackRook,currentMove)
			tempHistory=currentMove

			###update castling variables
			#copy castling variables from previous
			tempWhiteQueenCastle=whiteQueenCastle
			tempWhiteKingCastle=whiteKingCastle
			tempBlackQueenCastle=blackQueenCastle
			tempBlackKingCastle=blackKingCastle

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
				if(((1<<start)&whiteKing)!=0):
					tempWhiteQueenCastle=False
					tempWhiteKingCastle=False
				#if currentMove is moving blackKing, black queen and king side castle become False
				elif(((1<<start)&blackKing)!=0):
					tempBlackQueenCastle=False
					tempBlackKingCastle=False
				#if currentMove is moving white left rook, white queenside castling become False
				elif(((1<<start)&whiteRook&(1<<56))!=0):
					tempWhiteQueenCastle=False
				#if currentMove is moving white right rook, white kingside castling become False
				elif(((1<<start)&whiteRook&(1<<63))!=0):
					tempWhiteKingCastle=False
				elif(((1<<start)&blackRook&(1<<0))!=0):
					tempBlackQueenCastle=False
				elif(((1<<start)&blackRook&(1<<7))!=0):
					tempBlackKingCastle=False

			currentScore=Rating.quickEvaluate(tempHistory,tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn,tempWhiteQueenCastle,tempWhiteKingCastle,tempBlackQueenCastle,tempBlackKingCastle,depth+1,self.playerIsWhite)
			
			moveAndScore=MoveAndScore(currentMove,currentScore)
			MoveAndScoreList.append(moveAndScore)

		#Idea:
		#if this is player's turn, we need to return list sorted in descending order. Because player want to choose the most maximum score move.
		#If this is opponent's turn, we need to return list sorted in ascending order. Because opponent want to choose the most minimum score move.
		#if this is player's turn, sort in descending order
		if(self.playerIsWhite==whiteTurn):
			MoveAndScoreList.sort(key=self.getScore,reverse=True)
		#if this is opponent's turn, sort in ascending order
		else:
			MoveAndScoreList.sort(key=self.getScore,reverse=False)

		for i in range(len(MoveAndScoreList)):
			li.append(MoveAndScoreList[i].move)
		return li
		

	#given current board, return the best score this board can achieves.
	#player will always choose largest score as best score, opponent will always choose lowest score as best score
	#Given a state of chessBoard, return the best score this state of chessBoard can achieve for current player, and the best move that can be made for current player
	#rtype: int(score), string(best move) 
	def principalVariationSearch(self,alpha,beta,history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle,whiteTurn,depth):
		Moves=self.Moves
		Rating=self.Rating

		#if we reach our max search depth, return the best score for the board at that level
		if(depth==self.maxDepth):
			bestScore=Rating.evaluate(history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle,depth, self.playerIsWhite)
			return bestScore,"No Move"

		if(whiteTurn):
			moves=Moves.white_legalMoves(history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		else:
			moves=Moves.black_legalMoves(history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		

		#get the first legal move for the current player. After the moves have been sorted, we assume that the first move is always the best move.
		moves=self.sanitizeMove(moves,history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle,whiteTurn)
		
		#if no legal move for current player, then it must be checkmate or stalemate
		#if this is player's turn, this is really bad. return -5000
		#if this is opponent's turn, this is good. we want this. return 5000
		#TODO: Check this AND FIX THIS!
		if(len(moves)==0):
			if(self.playerIsWhite==whiteTurn):
				return -5000,"No Move"
			else:
				return 5000,"No Move"

		moves=self.sortMoves(moves,history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle,whiteTurn,depth)

		firstLegalMoveIndex=0
		b=beta
		bestScore=-math.inf

		####################################### throughroughly search firstLegalMove
		firstLegalMove=moves[firstLegalMoveIndex]

		try:
			originalX=int(firstLegalMove[0])
			originalY=int(firstLegalMove[1])
			newX=int(firstLegalMove[2])
			newY=int(firstLegalMove[3])
		except(ValueError):
			raise ValueError("Error in principalVariationSearch: the first four character of firstLegalMove string must be integer.")

		start=(originalX*8)+originalY
		end=(newX*8)+newY

		#white pieces
		tempWhiteKing=Moves.makeMove(whiteKing,firstLegalMove,"K")
		tempWhiteQueen=Moves.makeMove(whiteQueen,firstLegalMove,"Q")
		tempWhiteBishop=Moves.makeMove(whiteBishop,firstLegalMove,"B")
		tempWhiteKnight=Moves.makeMove(whiteKnight,firstLegalMove,"H")
		tempWhiteRook=Moves.makeMove(whiteRook,firstLegalMove,"R")
		tempWhitePawn=Moves.makeMove(whitePawn,firstLegalMove,"P")
		#if castling, make castling move
		if("WL" in firstLegalMove or "WR" in firstLegalMove):
			tempWhiteKing,tempWhiteRook=Moves.makeCastlingMove(whiteKing,whiteRook,firstLegalMove)
		#black pieces
		tempBlackKing=Moves.makeMove(blackKing,firstLegalMove,"k")
		tempBlackQueen=Moves.makeMove(blackQueen,firstLegalMove,"q")
		tempBlackBishop=Moves.makeMove(blackBishop,firstLegalMove,"b")
		tempBlackKnight=Moves.makeMove(blackKnight,firstLegalMove,"h")
		tempBlackRook=Moves.makeMove(blackRook,firstLegalMove,"r")
		tempBlackPawn=Moves.makeMove(blackPawn,firstLegalMove,"p")
		if("BL" in firstLegalMove or "BR" in firstLegalMove):
			tempBlackKing,tempBlackRook=Moves.makeCastlingMove(blackKing,blackRook,firstLegalMove)
		tempHistory=firstLegalMove

		###update castling variables
		#copy castling variables from previous
		tempWhiteQueenCastle=whiteQueenCastle
		tempWhiteKingCastle=whiteKingCastle
		tempBlackQueenCastle=blackQueenCastle
		tempBlackKingCastle=blackKingCastle

		#update castling variable based on the firstLegalMove we made
		#if firstLegalMove is making white castling move, we can no longer castle again for white
		if("WL" in firstLegalMove or "WR" in firstLegalMove):
			tempWhiteQueenCastle=False
			tempWhiteKingCastle=False
		#if firstLegalMove is making black castling move, we can no longer castle again for black
		elif("BL" in firstLegalMove or "BR" in firstLegalMove):
			tempBlackQueenCastle=False
			tempBlackKingCastle=False
		else:
			#if firstLegalMove is moving whiteKing, white queen and king side castle become False
			if(((1<<start)&whiteKing)!=0):
				tempWhiteQueenCastle=False
				tempWhiteKingCastle=False
			#if firstLegalMove is moving blackKing, black queen and king side castle become False
			elif(((1<<start)&blackKing)!=0):
				tempBlackQueenCastle=False
				tempBlackKingCastle=False
			#if firstLegalMove is moving white left rook, white queenside castling become False
			elif(((1<<start)&whiteRook&(1<<56))!=0):
				tempWhiteQueenCastle=False
			#if firstLegalMove is moving white right rook, white kingside castling become False
			elif(((1<<start)&whiteRook&(1<<63))!=0):
				tempWhiteKingCastle=False
			elif(((1<<start)&blackRook&(1<<0))!=0):
				tempBlackQueenCastle=False
			elif(((1<<start)&blackRook&(1<<7))!=0):
				tempBlackKingCastle=False
		"""
		# original algorithm
		score,bestMove=-self.principalVariationSearch(-b,-alpha,tempHistory,tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn,tempWhiteQueenCastle,tempWhiteKingCastle,tempBlackQueenCastle,tempBlackKingCastle,not whiteTurn,depth+1)
		"""
		#Alternate way of writing to original algorithm
		score,bestMove=self.principalVariationSearch(-b,-alpha,tempHistory,tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn,tempWhiteQueenCastle,tempWhiteKingCastle,tempBlackQueenCastle,tempBlackKingCastle,not whiteTurn,depth+1)
		score=-score
		#In principal variation search, we assume that our first move is the best move, and thus yield the best score.
		bestScore=self.max(bestScore,score)   #can also write bestScore=score
		alpha=self.max(alpha,score)
		bestMoveIndex=firstLegalMoveIndex
		if(alpha>=beta):
			return alpha, moves[bestMoveIndex]

		b=alpha+1

		####################################### simply and quickly search through remaining move to confirm our assumption that firstLegalMove is the best move
		for i in range(len(moves)):
			#if current iteration is firstLegalMoveIndex, skip, since we already thoroughly searched this move.
			if(i==firstLegalMoveIndex):
				continue
			#if current iteration is not firstLegalMoveIndex, simply and quickly search through current move.
			currentMove=moves[i]
			try:
				originalX=int(currentMove[0])
				originalY=int(currentMove[1])
				newX=int(currentMove[2])
				newY=int(currentMove[3])
			except(ValueError):
				raise ValueError("Error in principalVariationSearch: the first four character of currentMove string must be integer.")

			start=(originalX*8)+originalY
			end=(newX*8)+newY

			#white pieces
			tempWhiteKing=Moves.makeMove(whiteKing,currentMove,"K")
			tempWhiteQueen=Moves.makeMove(whiteQueen,currentMove,"Q")
			tempWhiteBishop=Moves.makeMove(whiteBishop,currentMove,"B")
			tempWhiteKnight=Moves.makeMove(whiteKnight,currentMove,"H")
			tempWhiteRook=Moves.makeMove(whiteRook,currentMove,"R")
			tempWhitePawn=Moves.makeMove(whitePawn,currentMove,"P")
			#if castling, make castling move
			if("WL" in currentMove or "WR" in currentMove):
				tempWhiteKing,tempWhiteRook=Moves.makeCastlingMove(whiteKing,whiteRook,currentMove)
			#black pieces
			tempBlackKing=Moves.makeMove(blackKing,currentMove,"k")
			tempBlackQueen=Moves.makeMove(blackQueen,currentMove,"q")
			tempBlackBishop=Moves.makeMove(blackBishop,currentMove,"b")
			tempBlackKnight=Moves.makeMove(blackKnight,currentMove,"h")
			tempBlackRook=Moves.makeMove(blackRook,currentMove,"r")
			tempBlackPawn=Moves.makeMove(blackPawn,currentMove,"p")
			if("BL" in currentMove or "BR" in currentMove):
				tempBlackKing,tempBlackRook=Moves.makeCastlingMove(blackKing,blackRook,currentMove)
			tempHistory=currentMove

			###update castling variables
			#copy castling variables from previous
			tempWhiteQueenCastle=whiteQueenCastle
			tempWhiteKingCastle=whiteKingCastle
			tempBlackQueenCastle=blackQueenCastle
			tempBlackKingCastle=blackKingCastle

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
				if(((1<<start)&whiteKing)!=0):
					tempWhiteQueenCastle=False
					tempWhiteKingCastle=False
				#if currentMove is moving blackKing, black queen and king side castle become False
				elif(((1<<start)&blackKing)!=0):
					tempBlackQueenCastle=False
					tempBlackKingCastle=False
				#if currentMove is moving white left rook, white queenside castling become False
				elif(((1<<start)&whiteRook&(1<<56))!=0):
					tempWhiteQueenCastle=False
				#if currentMove is moving white right rook, white kingside castling become False
				elif(((1<<start)&whiteRook&(1<<63))!=0):
					tempWhiteKingCastle=False
				elif(((1<<start)&blackRook&(1<<0))!=0):
					tempBlackQueenCastle=False
				elif(((1<<start)&blackRook&(1<<7))!=0):
					tempBlackKingCastle=False

			#TODO: check this!
			"""
			# original algorithm
			score,bestMove=-self.principalVariationSearch(-b,-alpha,tempHistory,tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn,tempWhiteQueenCastle,tempWhiteKingCastle,tempBlackQueenCastle,tempBlackKingCastle,not whiteTurn,depth+1)
			"""
			#Alternate way of writing to original algorithm
			score,bestMove=self.principalVariationSearch(-b,-alpha,tempHistory,tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn,tempWhiteQueenCastle,tempWhiteKingCastle,tempBlackQueenCastle,tempBlackKingCastle,not whiteTurn,depth+1)
			score=-score
			if(score>alpha and score<beta):
				"""
				# original algorithm
				score,bestMove=-self.principalVariationSearch(-beta,-score,tempHistory,tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn,tempWhiteQueenCastle,tempWhiteKingCastle,tempBlackQueenCastle,tempBlackKingCastle,not whiteTurn,depth+1)
				"""
				#alternate way of writing to original algorithm
				score,bestMove=self.principalVariationSearch(-beta,-score,tempHistory,tempWhiteKing,tempWhiteQueen,tempWhiteBishop,tempWhiteKnight,tempWhiteRook,tempWhitePawn,tempBlackKing,tempBlackQueen,tempBlackBishop,tempBlackKnight,tempBlackRook,tempBlackPawn,tempWhiteQueenCastle,tempWhiteKingCastle,tempBlackQueenCastle,tempBlackKingCastle,not whiteTurn,depth+1)
				score=-score
				##For debugging
				# print("researched")
			if(score>bestScore):
				bestMoveIndex=i
				bestScore=score
			alpha=self.max(alpha,score)
			if(alpha>=beta):
				return alpha, moves[bestMoveIndex]
			b=alpha+1

		return bestScore, moves[bestMoveIndex]

