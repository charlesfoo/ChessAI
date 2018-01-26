#!/usr/bin/env python3

"""
@author: Foo Zhi Yuan
ChessAI is being implemented using the concepts of bitboard and principal variation search
Requires Python 3 and Pillow(for GUI)
USAGE: python chessAI.py to play in GUI and python chessAI_console.py to play in console 
"""

from moves import Moves

class Rating:
	"""
	Positional score credits to http://chessprogramming.wikispaces.com/Simplified+evaluation+function

	"""
	currKing=None;currQueen=None;currBishop=None;currKnight=None;currRook=None;currPawn=None
	altKing=None;altQueen=None;altBishop=None;altKnight=None;altRook=None;altPawn=None
	Moves=None

	pawnBoard=[
	[ 0,  0,  0,  0,  0,  0,  0,  0],
	[50, 50, 50, 50, 50, 50, 50, 50],
	[10, 10, 20, 30, 30, 20, 10, 10],
	[ 5,  5, 10, 25, 25, 10,  5,  5],
	[ 0,  0,  0, 20, 20,  0,  0,  0],
	[ 5, -5,-10,  0,  0,-10, -5,  5],
	[ 5, 10, 10,-20,-20, 10, 10,  5],
	[ 0,  0,  0,  0,  0,  0,  0,  0]]

	rookBoard=[
	[ 0,  0,  0,  0,  0,  0,  0,  0],
	[ 5, 10, 10, 10, 10, 10, 10,  5],
	[-5,  0,  0,  0,  0,  0,  0, -5],
	[-5,  0,  0,  0,  0,  0,  0, -5],
	[-5,  0,  0,  0,  0,  0,  0, -5],
	[-5,  0,  0,  0,  0,  0,  0, -5],
	[-5,  0,  0,  0,  0,  0,  0, -5],
	[ 0,  0,  0,  5,  5,  0,  0,  0]]

	knightBoard=[
	[-50,-40,-30,-30,-30,-30,-40,-50],
	[-40,-20,  0,  0,  0,  0,-20,-40],
	[-30,  0, 10, 15, 15, 10,  0,-30],
	[-30,  5, 15, 20, 20, 15,  5,-30],
	[-30,  0, 15, 20, 20, 15,  0,-30],
	[-30,  5, 10, 15, 15, 10,  5,-30],
	[-40,-20,  0,  5,  5,  0,-20,-40],
	[-50,-40,-30,-30,-30,-30,-40,-50]]

	bishopBoard=[
	[-20,-10,-10,-10,-10,-10,-10,-20],
	[-10,  0,  0,  0,  0,  0,  0,-10],
	[-10,  0,  5, 10, 10,  5,  0,-10],
	[-10,  5,  5, 10, 10,  5,  5,-10],
	[-10,  0, 10, 10, 10, 10,  0,-10],
	[-10, 10, 10, 10, 10, 10, 10,-10],
	[-10,  5,  0,  0,  0,  0,  5,-10],
	[-20,-10,-10,-10,-10,-10,-10,-20]]

	queenBoard=[
	[-20,-10,-10, -5, -5,-10,-10,-20],
	[-10,  0,  0,  0,  0,  0,  0,-10],
	[-10,  0,  5,  5,  5,  5,  0,-10],
	[ -5,  0,  5,  5,  5,  5,  0, -5],
	[  0,  0,  5,  5,  5,  5,  0, -5],
	[-10,  5,  5,  5,  5,  5,  0,-10],
	[-10,  0,  5,  0,  0,  0,  0,-10],
	[-20,-10,-10, -5, -5,-10,-10,-20]]

	kingMidBoard=[
	[-30,-40,-40,-50,-50,-40,-40,-30],
	[-30,-40,-40,-50,-50,-40,-40,-30],
	[-30,-40,-40,-50,-50,-40,-40,-30],
	[-30,-40,-40,-50,-50,-40,-40,-30],
	[-20,-30,-30,-40,-40,-30,-30,-20],
	[-10,-20,-20,-20,-20,-20,-20,-10],
	[ 20, 20,  0,  0,  0,  0, 20, 20],
	[ 20, 30, 10,  0,  0, 10, 30, 20]]

	kingEndBoard=[
	[-50,-40,-30,-20,-20,-30,-40,-50],
	[-30,-20,-10,  0,  0,-10,-20,-30],
	[-30,-10, 20, 30, 30, 20,-10,-30],
	[-30,-10, 30, 40, 40, 30,-10,-30],
	[-30,-10, 30, 40, 40, 30,-10,-30],
	[-30,-10, 20, 30, 30, 20,-10,-30],
	[-30,-30,  0,  0,  0,  0,-30,-30],
	[-50,-30,-30,-30,-30,-30,-30,-50]]

	def __init__(self,Moves):
		self.Moves=Moves

	#type board: int
	def reverse(self,board):
		binary=format(board,"064b")
		binary=binary[::-1]
		return int(binary,2)

	def flipBoard(self):
		self.currKing=self.reverse(self.currKing)
		self.currQueen=self.reverse(self.currQueen)
		self.currBishop=self.reverse(self.currBishop)
		self.currKnight=self.reverse(self.currKnight)
		self.currRook=self.reverse(self.currRook)
		self.currPawn=self.reverse(self.currPawn)

		self.altKing=self.reverse(self.altKing)
		self.altQueen=self.reverse(self.altQueen)
		self.altBishop=self.reverse(self.altBishop)
		self.altKnight=self.reverse(self.altKnight)
		self.altRook=self.reverse(self.altRook)
		self.altPawn=self.reverse(self.altPawn)

		tempKing=self.currKing
		tempQueen=self.currQueen
		tempBishop=self.currBishop
		tempKnight=self.currKnight
		tempRook=self.currRook
		tempPawn=self.currPawn

		self.currKing=self.altKing
		self.currQueen=self.altQueen
		self.currBishop=self.altBishop
		self.currKnight=self.altKnight
		self.currRook=self.altRook
		self.currPawn=self.altPawn

		self.altKing=tempKing
		self.altQueen=tempQueen
		self.altBishop=tempBishop
		self.altKnight=tempKnight
		self.altRook=tempRook
		self.altPawn=tempPawn


	#type pieces: dictionary of bitboards
	#type numOfPossibleMoves: int
	#type depth: int
	#type playerIsWhite: True if player is white, False otherwise
	#note: Given a board, our score is only based on player's pieces.
	def evaluate(self, history, whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle,depth, playerIsWhite):		
		Moves=self.Moves
		counter=0

		self.currKing=whiteKing;self.currQueen=whiteQueen;self.currBishop=whiteBishop;self.currKnight=whiteKnight;self.currRook=whiteRook;self.currPawn=whitePawn
		self.altKing=blackKing;self.altQueen=blackQueen;self.altBishop=blackBishop;self.altKnight=blackKnight;self.altRook=blackRook;self.altPawn=blackPawn
		
		whitePossibleMoves=Moves.white_legalMoves(history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		blackPossibleMoves=Moves.black_legalMoves(history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		numOfWhitePossibleMoves=len(whitePossibleMoves.split())
		numOfBlackPossibleMoves=len(blackPossibleMoves.split())

		whiteKingMoves=Moves.whiteKing_moves(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		blackKingMoves=Moves.blackKing_moves(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		numOfWhiteKingMoves=len(whiteKingMoves.split())
		numofBlackKingMoves=len(blackKingMoves.split())

		boardFlipped=False
		if(playerIsWhite):
			pass
		elif(not playerIsWhite):
			self.flipBoard()
			boardFlipped=True
		"""
		-> Our internal board is always represented with black pieces on top, white pieces at the bottom. 
		-> Our method usually will just evaluate white pieces, add it to our counter; flip the board, evaluate white pieces again, 
			and deduct them from our counter. 
		-> If player is white and if it's white turn to move, there's no problem at all with this approach, 
			since we will add white pieces' score to our counter, and deduct black pieces' score from our counter.
		-> If player is white and if it's black turn to move, observe that there is still no problem with this approach. 
			In particular, we'll add white pieces' score to our counter, and deduct black pieces' score from our counter. This is okay, because
			we want our board evaluation to be based on white player's perspective. We want to see if when black makes a move, how does it affect white player.
		-> When player is black, we just need to flip board before computing. The rest of the procedure remains the same.

		"""
		
		#give each piece on the board a score, rate the board
		#Player's perspective
		material=self.rateMaterial(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn)
		counter=counter+self.rateAttack(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,self.altKing,self.altQueen,self.altBishop,self.altKnight,self.altRook,self.altPawn)
		counter=counter+material
		#score for white pieces (player is white)
		if(not boardFlipped):
			#rate Moveability
			counter=counter+self.rateMoveability(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,self.altKing,self.altQueen,self.altBishop,self.altKnight,self.altRook,self.altPawn,depth,material,numOfWhitePossibleMoves)
			#rate positional
			counter=counter+self.ratePositional(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,material,numOfWhiteKingMoves)
		#score for black pieces (player is black)
		elif(boardFlipped):
			#rate Moveability
			counter=counter+self.rateMoveability(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,self.altKing,self.altQueen,self.altBishop,self.altKnight,self.altRook,self.altPawn,depth,material,numOfBlackPossibleMoves)
			#rate positional
			counter=counter+self.ratePositional(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,material,numofBlackKingMoves)
		self.flipBoard()
		#we need to update our board flipped variable according to if our board is flipped now
		#if board is not flipped before, since we just do flipBoard(), our board is flipped now.
		if(boardFlipped==False):
			boardFlipped=True
		#if board is flipped before, since we just do flipBoard(), board is now back to its original state. So board is not flipped now.
		elif(boardFlipped==True):
			boardFlipped=False


		#Opponent's perspective
		material=self.rateMaterial(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn)
		counter=counter-self.rateAttack(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,self.altKing,self.altQueen,self.altBishop,self.altKnight,self.altRook,self.altPawn)
		counter=counter-material
		#score for black pieces (player is white)
		if(boardFlipped):
			counter=counter-self.rateMoveability(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,self.altKing,self.altQueen,self.altBishop,self.altKnight,self.altRook,self.altPawn,depth,material,numOfBlackPossibleMoves)
			counter=counter-self.ratePositional(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,material,numofBlackKingMoves)
		#score for white pieces (player is black)
		elif(not boardFlipped):
			counter=counter-self.rateMoveability(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,self.altKing,self.altQueen,self.altBishop,self.altKnight,self.altRook,self.altPawn,depth,material,numOfWhitePossibleMoves)
			counter=counter-self.ratePositional(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,material,numOfWhiteKingMoves)
		self.flipBoard()
		#we need to update our board flipped variable according to if our board is flipped now
		#if board is not flipped before, since we just do flipBoard(), our board is flipped now.
		if(boardFlipped==False):
			boardFlipped=True
		#if board is flipped before, since we just do flipBoard(), board is now back to its original state. So board is not flipped now.
		elif(boardFlipped==True):
			boardFlipped=False


		#restore board to original state. black pieces on top, white pieces at bottom
		if(boardFlipped):
			self.flipBoard()
			boardFlipped=False

		return (counter+depth*500)

	#Given a board, do a quick evaluation on the board. We only perform rateMaterial and rateMoveability.
	def quickEvaluate(self, history, whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle,depth, playerIsWhite):
		Moves=self.Moves
		counter=0

		self.currKing=whiteKing;self.currQueen=whiteQueen;self.currBishop=whiteBishop;self.currKnight=whiteKnight;self.currRook=whiteRook;self.currPawn=whitePawn
		self.altKing=blackKing;self.altQueen=blackQueen;self.altBishop=blackBishop;self.altKnight=blackKnight;self.altRook=blackRook;self.altPawn=blackPawn
		
		whitePossibleMoves=Moves.white_legalMoves(history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		blackPossibleMoves=Moves.black_legalMoves(history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		numOfWhitePossibleMoves=len(whitePossibleMoves.split())
		numOfBlackPossibleMoves=len(blackPossibleMoves.split())

		boardFlipped=False
		if(playerIsWhite):
			pass
		elif(not playerIsWhite):
			self.flipBoard()
			boardFlipped=True
		"""
		-> Our internal board is always represented with black pieces on top, white pieces at the bottom. 
		-> Our method usually will just evaluate white pieces, add it to our counter; flip the board, evaluate white pieces again, 
			and deduct them from our counter. 
		-> If player is white and if it's white turn to move, there's no problem at all with this approach, 
			since we will add white pieces' score to our counter, and deduct black pieces' score from our counter.
		-> If player is white and if it's black turn to move, observe that there is still no problem with this approach. 
			In particular, we'll add white pieces' score to our counter, and deduct black pieces' score from our counter. This is okay, because
			we want our board evaluation to be based on white player's perspective. We want to see if when black makes a move, how does it affect white player.
		-> When player is black, we just need to flip board before computing. The rest of the procedure remains the same.

		"""
		
		#give each piece on the board a score, rate the board
		#Player's perspective
		material=self.rateMaterial(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn)
		counter=counter+material
		#score for white pieces (player is white)
		if(not boardFlipped):
			#rate Moveability
			counter=counter+self.rateMoveability(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,self.altKing,self.altQueen,self.altBishop,self.altKnight,self.altRook,self.altPawn,depth,material,numOfWhitePossibleMoves)
		#score for black pieces (player is black)
		elif(boardFlipped):
			#rate Moveability
			counter=counter+self.rateMoveability(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,self.altKing,self.altQueen,self.altBishop,self.altKnight,self.altRook,self.altPawn,depth,material,numOfBlackPossibleMoves)
		self.flipBoard()
		#we need to update our board flipped variable according to if our board is flipped now
		#if board is not flipped before, since we just do flipBoard(), our board is flipped now.
		if(boardFlipped==False):
			boardFlipped=True
		#if board is flipped before, since we just do flipBoard(), board is now back to its original state. So board is not flipped now.
		elif(boardFlipped==True):
			boardFlipped=False


		#Opponent's perspective
		material=self.rateMaterial(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn)
		counter=counter-material
		#score for black pieces (player is white)
		if(boardFlipped):
			counter=counter-self.rateMoveability(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,self.altKing,self.altQueen,self.altBishop,self.altKnight,self.altRook,self.altPawn,depth,material,numOfBlackPossibleMoves)
		#score for white pieces (player is black)
		elif(not boardFlipped):
			counter=counter-self.rateMoveability(self.currKing,self.currQueen,self.currBishop,self.currKnight,self.currRook,self.currPawn,self.altKing,self.altQueen,self.altBishop,self.altKnight,self.altRook,self.altPawn,depth,material,numOfWhitePossibleMoves)
		self.flipBoard()
		#we need to update our board flipped variable according to if our board is flipped now
		#if board is not flipped before, since we just do flipBoard(), our board is flipped now.
		if(boardFlipped==False):
			boardFlipped=True
		#if board is flipped before, since we just do flipBoard(), board is now back to its original state. So board is not flipped now.
		elif(boardFlipped==True):
			boardFlipped=False


		#restore board to original state. black pieces on top, white pieces at bottom
		if(boardFlipped):
			self.flipBoard()
			boardFlipped=False

		return (counter+depth*500)




	def getPieceCountInBitBoard(self,bitBoard):
		binary=format(bitBoard,"064b")
		return binary.count("1")


	def rateMaterial(self,king,queen,bishop,knight,rook,pawn):   #CORRECT
		counter=0
		#white queen
		pieceCount=self.getPieceCountInBitBoard(queen)
		counter=counter+(pieceCount*900)

		#white bishop
		pieceCount=self.getPieceCountInBitBoard(bishop)
		if(pieceCount>=2):
			counter=counter+(pieceCount*300)
		else:
			counter=counter+(pieceCount*250)

		#white knight
		pieceCount=self.getPieceCountInBitBoard(knight)
		counter=counter+(pieceCount*300)

		#white rook
		pieceCount=self.getPieceCountInBitBoard(rook)
		counter=counter+(pieceCount*500)

		#white pawn
		pieceCount=self.getPieceCountInBitBoard(pawn)
		counter=counter+(pieceCount*100)
		return counter

	def ratePositional(self,king,queen,bishop,knight,rook,pawn,material,numofKingMoves):
		counter=0

		for i in range(64):
			if((pawn>>i)&1==1):
				counter=counter+self.pawnBoard[i//8][i%8]
			elif((rook>>i)&1==1):
				counter=counter+self.rookBoard[i//8][i%8]
			elif((knight>>i)&1==1):
				counter=counter+self.knightBoard[i//8][i%8]
			elif((bishop>>i)&1==1):
				counter=counter+self.bishopBoard[i//8][i%8]
			elif((queen>>i)&1==1):
				counter=counter+self.queenBoard[i//8][i%8]
			elif((king>>i)&1==1):
				#score the position of the king based on phase
				#if the score of piece on the board >=1750, this is a middle phase
				if(material>=1750):
					counter=counter+self.kingMidBoard[i//8][i%8]
					counter=counter+(numofKingMoves*10)
				#end phase
				else:
					counter=counter+self.kingEndBoard[i//8][i%8]
					counter=counter+(numofKingMoves*30)		
		return counter

	#score our ability to move
	#penalise heavily for checkmate and stalemate             #CORRECT
	def rateMoveability(self,playerKing,playerQueen,playerBishop,playerKnight,playerRook,playerPawn,opponentKing,opponentQueen,opponentBishop,opponentKnight,opponentRook,opponentPawn,depth,material,numOfPossibleMoves):
		Moves=self.Moves
		counter=0
		#5 points for each valid move
		counter=counter+(numOfPossibleMoves*5)
		#either checkmate or stalemate
		#stalemate means no square to move to, except for squares that will get king into checked
		if(numOfPossibleMoves==0):
			#if king currently in checked and no place to move to, checkmate
			if(playerKing&Moves.whiteKing_illegalMoves(playerKing,playerQueen,playerBishop,playerKnight,playerRook,playerPawn,opponentKing,opponentQueen,opponentBishop,opponentKnight,opponentRook,opponentPawn)!=0):
				counter=counter+(-200000*depth)
			#if king currently is not in checked and no place to move to, stalemate
			else:
				counter=counter+(-150000*depth)
		return counter

	#check if each of my piece is under attack. if it is, return lower score    #CORRECT
	def rateAttack(self,playerKing,playerQueen,playerBishop,playerKnight,playerRook,playerPawn,opponentKing,opponentQueen,opponentBishop,opponentKnight,opponentRook,opponentPawn):
		Moves=self.Moves
		counter=0
		kingPosition=None

		underAttack=Moves.whiteKing_illegalMoves(playerKing,playerQueen,playerBishop,playerKnight,playerRook,playerPawn,opponentKing,opponentQueen,opponentBishop,opponentKnight,opponentRook,opponentPawn)


		for i in range(64):
			#we check if our piece at this position is under attack by placing our king at this position
			#if our king is under attack, playerPawn at this position is also under attack
			if((playerPawn>>i)&1==1):
				kingPosition=(1<<i)
				if(underAttack&kingPosition!=0):
					counter=counter-64
			#if our king is under attack, playerRook at this position is also under attack
			elif((playerRook>>i)&1==1):
				kingPosition=(1<<i)
				if(underAttack&kingPosition!=0):
					counter=counter-500
			#if our king is under attack, playerKnight at this position is also under attack
			elif((playerKnight>>i)&1==1):
				kingPosition=(1<<i)
				if(underAttack&kingPosition!=0):
					counter=counter-300
			#if our king is under attack, playerBishop at this position is also under attack
			elif((playerBishop>>i)&1==1):
				kingPosition=(1<<i)
				if(underAttack&kingPosition!=0):
					counter=counter-300
			#if our king is under attack, playerQueen at this position is also under attack
			elif((playerQueen>>i)&1==1):
				kingPosition=(1<<i)
				if(underAttack&kingPosition!=0):
					counter=counter-900
		kingPosition=playerKing
		if(underAttack&kingPosition!=0):
			counter=counter-2000
		#our piece under attack is less important than our piece actually being captured by opponent, so we divide it by 2
		return counter/2
