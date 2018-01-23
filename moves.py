#!/usr/bin/env python3

"""
@author: Foo Zhi Yuan
ChessAI implemented using the concepts of bitboard and principal variation search
Requires Python 3 and Pillow(for GUI)
USAGE: python chessAI.py to play in GUI and python chessAI_console.py to play in console
"""

from presetPositions import *

class Moves:
	#(all black pieces EXCLUDING black king) and all empty spaces
	NOTPLAYERPIECES=None
	#all black pieces EXCLUDING black king
	BLACKPIECES=None
	#all white pieces EXCLUDING white king
	WHITEPIECES=None
	#positions occupied by either black or white pieces
	OCCUPIED=None
	#all empty spaces on the board
	EMPTYSPACE=None
	#castling
	whiteQueenCastle=None
	whiteKingCastle=None
	blackQueenCastle=None
	blackKingCastle=None
	#rooks
	rooks={"whiteLeftRook":56,"whiteRightRook":63,"blackLeftRook":0,"blackRightRook":7}
	
	def NOT(self,num):
		# unsigned=bin(~np.uint64(num))
		# unsigned=unsigned.replace("0b","")
		# unsigned=int(unsigned,2)
		# return unsigned
		result=~num&0xFFFFFFFFFFFFFFFF
		return result

	#type history: string
	#type pieces: dictionary
	#type castling: dictionary
	#type boardFlipped: boolean. If boardFlipped is true, we represent our black pieces as white, and are checking for the legal moves for flipped white pieces.
	#rtype: string
	#player is white, return all legal white moves
	def white_legalMoves(self,history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle):
		self.NOTPLAYERPIECES=self.NOT(whiteKing|whiteQueen|whiteBishop|whiteKnight|whiteRook|whitePawn|blackKing)
		self.BLACKPIECES=(blackQueen|blackBishop|blackKnight|blackRook|blackPawn)
		self.OCCUPIED=(whiteKing|whiteQueen|whiteBishop|whiteKnight|whiteRook|whitePawn|
			blackKing|blackQueen|blackBishop|blackKnight|blackRook|blackPawn)
		self.EMPTYSPACE=self.NOT(self.OCCUPIED)
		#castling
		self.whiteQueenCastle=whiteQueenCastle
		self.whiteKingCastle=whiteKingCastle
		self.blackQueenCastle=blackQueenCastle
		self.blackKingCastle=blackKingCastle

		li=self.whitePawn_legalMoves(history,whitePawn,blackPawn)+self.king_legalMoves(whiteKing)+self.queen_legalMoves(whiteQueen)+self.bishop_legalMoves(whiteBishop)+self.knight_legalMoves(whiteKnight)+self.rook_legalMoves(whiteRook)+self.whiteCastling(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		
		# li=self.blackKing_illegalMoves(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn)
		# z=li.split()
		# for item in z:
		# 	print(item)

		
		return li
	
	#type history: string
	#type pieces: dictionary
	#type castling: dictionary
	#rtype: string
	#player is black, return all legal black moves
	def black_legalMoves(self,history,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle):
		self.NOTPLAYERPIECES=self.NOT(blackKing|blackQueen|blackBishop|blackKnight|blackRook|blackPawn|whiteKing)
		self.WHITEPIECES=(whiteQueen|whiteBishop|whiteKnight|whiteRook|whitePawn)
		self.OCCUPIED=(whiteKing|whiteQueen|whiteBishop|whiteKnight|whiteRook|whitePawn|
			blackKing|blackQueen|blackBishop|blackKnight|blackRook|blackPawn)
		self.EMPTYSPACE=self.NOT(self.OCCUPIED)
		#castling
		self.whiteQueenCastle=whiteQueenCastle
		self.whiteKingCastle=whiteKingCastle
		self.blackQueenCastle=blackQueenCastle
		self.blackKingCastle=blackKingCastle

		li=self.blackPawn_legalMoves(history,whitePawn,blackPawn)+self.king_legalMoves(blackKing)+self.queen_legalMoves(blackQueen)+self.bishop_legalMoves(blackBishop)+self.knight_legalMoves(blackKnight)+self.rook_legalMoves(blackRook)+self.blackCastling(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		# z=li.split()
		# print(len(z))
		# for item in z:
		# 	print(item)

		# li=self.whiteKing_illegalMoves(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn)
		return li

	#type history: string
	#type pieces: dictionary
	#rtype: string
	def whitePawn_legalMoves(self,history,whitePawn,blackPawn):

		li="";li_0="";li_1="";li_2="";li_3="";li_4="";li_5="";li_6="";li_7="";li_8=""

		############################capturing or moving forward
		#white pawn captures left
		#and not(ROWZEROONE) because that is a pawn promotion
		#and not(RIGHTCOLONE) because most left column pawn cannot left capture. a shift to right 9 will moves it to most right column of same row. we don't want that
		leftCapture=(whitePawn>>9)&self.BLACKPIECES&(self.NOT(ROWZEROONE))&(self.NOT(RIGHTCOLONE))
		#white pawn captures right 
		#and not(ROWZEROONE) because that is a pawn promotion
		#and not(LEFTCOLONE) because most right column pawn cannot right capture. a shift to right 7 will moves it to most left column of same row. we don't want that
		rightCapture=(whitePawn>>7)&self.BLACKPIECES&(self.NOT(ROWZEROONE))&(self.NOT(LEFTCOLONE))
		#white pawn moves one step forward
		#and EMPTYSPACE because to move pawn one step forward, the space in front must be empty
		#and not(ROWZEROONE) because that is a pawn promotion
		oneStepForward=(whitePawn>>8)&self.EMPTYSPACE&(self.NOT(ROWZEROONE))
		#white pawn moves two step forward
		#and EMPTY SPACE because to move pawn two step forward, the space in front must be empty
		#and ROWFOURONE because we want to make sure that the white pawn we moved two step forward is from default chessboard white pawn position
		twoStepForward=(whitePawn>>16)&self.EMPTYSPACE&ROWFOURONE
		if(leftCapture==0 and rightCapture==0 and oneStepForward==0 and twoStepForward==0):
			pass
		else:
			for i in range(64):
				if( ( (leftCapture>>i)&1 )==1):
					#original X, original Y, destination X, destination Y
					li_0=li_0+str(i//8+1)+str(i%8+1)+str(i//8)+str(i%8)+" "
				if( ( (rightCapture>>i)&1 )==1):
					li_1=li_1+str(i//8+1)+str(i%8-1)+str(i//8)+str(i%8)+" "
				if( ( (oneStepForward>>i)&1 )==1):
					li_2=li_2+str(i//8+1)+str(i%8)+str(i//8)+str(i%8)+" "
				if( ( (twoStepForward>>i)&1)==1):
					li_3=li_3+str(i//8+2)+str(i%8)+str(i//8)+str(i%8)+" "

		############################pawn promotion
		promotionByLeftCapture=(whitePawn>>9)&self.BLACKPIECES&ROWZEROONE&(self.NOT(RIGHTCOLONE))
		promotionByRightCapture=(whitePawn>>7)&self.BLACKPIECES&ROWZEROONE&(self.NOT(LEFTCOLONE))
		promotionByForwardMove=(whitePawn>>8)&self.EMPTYSPACE&ROWZEROONE
		if(promotionByLeftCapture==0 and promotionByRightCapture==0 and promotionByForwardMove==0):
			pass
		else:
			for i in range(64):
				if( ( (promotionByLeftCapture>>i)&1 )==1):
					#original X, original Y, destination X, destination Y, move type (QP=Queen Promotion, BP=Bishop Promotion, HP=Knight[horse] Promotion, RP=Rook Promotion)
					li_4=li_4+str(i//8+1)+str(i%8+1)+str(i//8)+str(i%8)+"QP"+" "+str(i//8+1)+str(i%8+1)+str(i//8)+str(i%8)+"BP"+" "+str(i//8+1)+str(i%8+1)+str(i//8)+str(i%8)+"HP"+" "+str(i//8+1)+str(i%8+1)+str(i//8)+str(i%8)+"RP"+" "
				if( ( (promotionByRightCapture>>i)&1 )==1):
					li_5=li_5+str(i//8+1)+str(i%8-1)+str(i//8)+str(i%8)+"QP"+" "+str(i//8+1)+str(i%8-1)+str(i//8)+str(i%8)+"BP"+" "+str(i//8+1)+str(i%8-1)+str(i//8)+str(i%8)+"HP"+" "+str(i//8+1)+str(i%8-1)+str(i//8)+str(i%8)+"RP"+" "
					
				if( ( (promotionByForwardMove>>i)&1 )==1):
					li_6=li_6+str(i//8+1)+str(i%8)+str(i//8)+str(i%8)+"QP"+" "+str(i//8+1)+str(i%8)+str(i//8)+str(i%8)+"BP"+" "+str(i//8+1)+str(i%8)+str(i//8)+str(i%8)+"HP"+" "+str(i//8+1)+str(i%8)+str(i//8)+str(i%8)+"RP"+" "

		############################en passant
		if(len(history)==4):
			#if our last move is pawn promotion, cannot enpeassant
			try:
				int(history)
			except(ValueError):
				raise ValueError("Error in whitePawn_legalMove: History of length 4 should only contain 4 digits of number.")
			oldX=int(history[0])
			oldY=int(history[1])
			newX=int(history[2])
			newY=int(history[3])
			if(oldY==newY and (abs(newX-oldX)==2) and oldX==1 and newX==3):
				columnToEnPassant=newY
				#left en passant
				#and ROWTHREEONE because that's the row of EnPassant piece
				#and ALLCOLONE[columnToEnPassant] to ensure that we only make a enpassant move to opponent last move of pawn
				leftEnPassant=(whitePawn>>1)&blackPawn&ROWTHREEONE&(self.NOT(RIGHTCOLONE))&COLALLONE[columnToEnPassant]
				#right en passant
				rightEnPassant=(whitePawn<<1)&blackPawn&ROWTHREEONE&(self.NOT(LEFTCOLONE))&COLALLONE[columnToEnPassant]
				if(leftEnPassant==0 and rightEnPassant==0):
					pass
				else:
					for i in range(64):
						if( ( (leftEnPassant>>i)&1)==1):
							#original X, original Y, destination X, destination Y, move type (WE: white enpassant)
							li_7=li_7+str(i//8)+str(i%8+1)+str(i//8-1)+str(i%8)+"WE"+" "
						if( ( (rightEnPassant>>i)&1)==1):
							#original X, original Y, destination X, destination Y, move type
							li_8=li_8+str(i//8)+str(i%8-1)+str(i//8-1)+str(i%8)+"WE"+" "


		li=li_0+li_1+li_2+li_3+li_4+li_5+li_6+li_7+li_8

		return li

	#type history: string
	#type pieces: dictionary
	#rtype: string
	def blackPawn_legalMoves(self,history,whitePawn,blackPawn):

		li="";li_0="";li_1="";li_2="";li_3="";li_4="";li_5="";li_6="";li_7="";li_8=""

		############################capturing or moving forward
		#black pawn captures left
		#and not(ROWSEVENONE) because that is a pawn promotion
		#and not(LEFT) because most right column pawn cannot left capture. a shift to left 9 will moves it to most left column of same row. we don't want that
		leftCapture=(blackPawn<<9)&self.WHITEPIECES&(self.NOT(ROWSEVENONE))&(self.NOT(LEFTCOLONE))
		#black pawn captures right 
		#and not(ROWSEVENONE) because that is a pawn promotion
		#and not(LEFTCOLONE) because most left column pawn cannot right capture. a shift to left 7 will moves it to most right column of same row. we don't want that
		rightCapture=(blackPawn<<7)&self.WHITEPIECES&(self.NOT(ROWSEVENONE))&(self.NOT(RIGHTCOLONE))
		#black pawn moves one step forward
		#and EMPTYSPACE because to move pawn one step forward, the space in front must be empty
		#and not(ROWSEVENONE) because that is a pawn promotion
		oneStepForward=(blackPawn<<8)&self.EMPTYSPACE&(self.NOT(ROWSEVENONE))
		#black pawn moves two step forward
		#and EMPTY SPACE because to move pawn two step forward, the space in front must be empty
		#and ROWTHREEONE because we want to make sure that the black pawn we moved two step forward is from default chessboard black pawn position
		twoStepForward=(blackPawn<<16)&self.EMPTYSPACE&ROWTHREEONE
		if(leftCapture==0 and rightCapture==0 and oneStepForward==0 and twoStepForward==0):
			pass
		else:
			for i in range(64):
				if( ( (leftCapture>>i)&1 )==1):
					#original X, original Y, destination X, destination Y
					li_0=li_0+str(i//8-1)+str(i%8-1)+str(i//8)+str(i%8)+" "
				if( ( (rightCapture>>i)&1 )==1):
					li_1=li_1+str(i//8-1)+str(i%8+1)+str(i//8)+str(i%8)+" "
				if( ( (oneStepForward>>i)&1 )==1):
					li_2=li_2+str(i//8-1)+str(i%8)+str(i//8)+str(i%8)+" "
				if( ( (twoStepForward>>i)&1)==1):
					li_3=li_3+str(i//8-2)+str(i%8)+str(i//8)+str(i%8)+" "

		############################pawn promotion
		promotionByLeftCapture=(blackPawn<<9)&self.WHITEPIECES&ROWSEVENONE&(self.NOT(LEFTCOLONE))
		promotionByRightCapture=(blackPawn<<7)&self.WHITEPIECES&ROWSEVENONE&(self.NOT(RIGHTCOLONE))
		promotionByForwardMove=(blackPawn<<8)&self.EMPTYSPACE&ROWSEVENONE
		if(promotionByLeftCapture==0 and promotionByRightCapture==0 and promotionByForwardMove==0):
			pass
		else:
			for i in range(64):
				if( ( (promotionByLeftCapture>>i)&1 )==1):
					#original X, original Y, destination X, destination Y, move type (QP=Queen Promotion, BP=Bishop Promotion, HP=Knight[horse] Promotion, RP=Rook Promotion)
					li_4=li_4+str(i//8-1)+str(i%8-1)+str(i//8)+str(i%8)+"qP"+" "+str(i//8-1)+str(i%8-1)+str(i//8)+str(i%8)+"bP"+" "+str(i//8-1)+str(i%8-1)+str(i//8)+str(i%8)+"hP"+" "+str(i//8-1)+str(i%8-1)+str(i//8)+str(i%8)+"rP"+" "
				if( ( (promotionByRightCapture>>i)&1 )==1):
					li_5=li_5+str(i//8-1)+str(i%8+1)+str(i//8)+str(i%8)+"qP"+" "+str(i//8-1)+str(i%8+1)+str(i//8)+str(i%8)+"bP"+" "+str(i//8-1)+str(i%8+1)+str(i//8)+str(i%8)+"hP"+" "+str(i//8-1)+str(i%8+1)+str(i//8)+str(i%8)+"rP"+" "
					
				if( ( (promotionByForwardMove>>i)&1 )==1):
					li_6=li_6+str(i//8-1)+str(i%8)+str(i//8)+str(i%8)+"qP"+" "+str(i//8-1)+str(i%8)+str(i//8)+str(i%8)+"bP"+" "+str(i//8-1)+str(i%8)+str(i//8)+str(i%8)+"hP"+" "+str(i//8-1)+str(i%8)+str(i//8)+str(i%8)+"rP"+" "

		############################en passant
		if(len(history)==4):
			#if our last move is pawn promotion, cannot enpeassant
			try:
				int(history)
			except(ValueError):
				raise ValueError("Error in blackPawn_legalMove: History of length 4 should only contain 4 digits of number.")
			oldX=int(history[0])
			oldY=int(history[1])
			newX=int(history[2])
			newY=int(history[3])
			if(oldY==newY and (abs(newX-oldX)==2) and oldX==6 and newX==4):
				columnToEnPassant=newY
				#left en passant
				#and ROWFOURONE because that's the row of EnPassant piece
				#and ALLCOLONE[columnToEnPassant] to ensure that we only make a enpassant move to opponent last move of pawn
				leftEnPassant=(blackPawn<<1)&whitePawn&ROWFOURONE&(self.NOT(LEFTCOLONE))&COLALLONE[columnToEnPassant]
				#right en passant
				rightEnPassant=(blackPawn>>1)&whitePawn&ROWFOURONE&(self.NOT(RIGHTCOLONE))&COLALLONE[columnToEnPassant]
				if(leftEnPassant==0 and rightEnPassant==0):
					pass
				else:
					for i in range(64):
						if( ( (leftEnPassant>>i)&1)==1):
							#original X, original Y, destination X, destination Y, move type (BE: black enpassant)
							li_7=li_7+str(i//8)+str(i%8-1)+str(i//8+1)+str(i%8)+"BE"+" "
						if( ( (rightEnPassant>>i)&1)==1):
							#original X, original Y, destination X, destination Y, move type
							li_8=li_8+str(i//8)+str(i%8+1)+str(i//8+1)+str(i%8)+"BE"+" "


		li=li_0+li_1+li_2+li_3+li_4+li_5+li_6+li_7+li_8

		return li



	#for debugging
	#type bitBoard: int
	def drawBoard(self,bitBoard,sliderPiece=None):
		board=[[" " for i in range(8)] for j in range(8)]
		if(sliderPiece is not None):
			for i in range(64):
				if( ( (bitBoard>>i)&1 )==1):
					board[i//8][i%8]="p"
				elif(i==sliderPiece):
					board[i//8][i%8]="S"
		else:
			for i in range(64):
				if( ( (bitBoard>>i)&1 )==1):
					board[i//8][i%8]="p"
		for i in range(8):
			print("[",end="")
			for j in range(8):
				if(j!=7):
					print(board[i][j],",",end="")
				else:
					print(board[i][j],end="")
			print("]",end="")
			print("")
		print("")
	
	#Given an integer this method takes the binary of this integer and reverse it, then revert the reverse binary back to int and return
	#type number: int
	#rtype: int
	def reverseBinary(self,number):
		#if number<0, we need to represent it in 2's complement before reversing it.
		if(number<0):
			#convert number to 2's complement
			"""
			Idea:
			3 -> 011
			-3 -> ?
			 1000
			- 011
			------
			  101  <- (-3)
			------
			"""
			two_complement=(1<<64)+number
			two_complement=format(two_complement,"064b")
			rev_binary64=two_complement[::-1]
			num=int(rev_binary64,2)
			return num
		else:
			binary64=format(number,"064b")
			rev_binary64=binary64[::-1]
			num=int(rev_binary64,2)
			return num

	"""
	Given a board like below:
	00000000
	00000000
	00000000
	pp000R0p
	00000000
	00000000
	00000000
	00000000
	How do I obtain all LEFT legal moves by the rook R?
	
	occupied=11000101
	slider=  00000100
	result=  01111000 (result we're seeking, eg: all left legal moves by R. doesn't include R current position since that's not a move)
	occupied-slider=11000001 (remove slider from our occupied piece)
	occupied-2*slider=10111101 (MAGIC: turn the first left piece that R is going to collide to into 0)
	left_legal_moves= occupied^(occupied-2*slider)=01111000
	unsimplified_right_legal_moves=( occupied'^(occupied'-2*slider') )'
									=00000011 (idea: reverse occupied, reverse 2*slider, treat them as left legal moves and compute the legal moves, then reverse
													the legal moves computed since we're finding right legal)
	reverse(a^b)=reverse(a)^reverse(b)
	right_legal_moves=occupied^(occupied'-2*slider')'
	lineAttack=left_legal_moves^right_legal_moves
			=(occupied-2*slider)^(occcupied'-2*slider')'

	Algorithm to obtain valid vertical, horizontal and diagonal moves:
	lineAttack= [ ((occupied&mask)-2*slider) ^ ((occcupied&mask)'-2*slider')' ]& mask 

	"""

	#type sliderPiece: int (int position of the slider piece on the board)
	#rtype: int (when converted to bitboard, this shows all positions that can be reached by slider piece vertically and horizontally)
	def verticalAndHorizontalMoves(self,sliderPiece):
		sliderPieceBinary=1<<sliderPiece
		horizontal=( (self.OCCUPIED-2*sliderPieceBinary)^(self.reverseBinary(self.reverseBinary(self.OCCUPIED)-2*self.reverseBinary(sliderPieceBinary))) )&ROWALLONE[sliderPiece//8]
		vertical=( ((self.OCCUPIED&COLALLONE[sliderPiece%8])-2*sliderPieceBinary)^(self.reverseBinary(self.reverseBinary(self.OCCUPIED&COLALLONE[sliderPiece%8])-2*self.reverseBinary(sliderPieceBinary))) ) & COLALLONE[sliderPiece%8] 
		result=horizontal|vertical
		return result

	#type sliderPiece: int (int position of the slider piece on the board)
	#rtype: int (when converted to bitboard, this shows all positions that can be reached by slider piece vertically and horizontally)
	def leftDiagonalAndRightDiagonalMoves(self,sliderPiece):
		sliderPieceBinary=1<<sliderPiece
		leftDiagonal=( ((self.OCCUPIED&LEFTDIAGONAL[ (sliderPiece//8)+7-(sliderPiece%8) ])-2*sliderPieceBinary)^(self.reverseBinary(self.reverseBinary(self.OCCUPIED&LEFTDIAGONAL[ (sliderPiece//8)+7-(sliderPiece%8) ])-2*self.reverseBinary(sliderPieceBinary))) ) & LEFTDIAGONAL[ (sliderPiece//8)+7-(sliderPiece%8) ]
		rightDiagonal=( ((self.OCCUPIED&RIGHTDIAGONAL[ (sliderPiece//8)+(sliderPiece%8) ])-2*sliderPieceBinary)^(self.reverseBinary(self.reverseBinary(self.OCCUPIED&RIGHTDIAGONAL[ (sliderPiece//8)+(sliderPiece%8) ])-2*self.reverseBinary(sliderPieceBinary))) ) & RIGHTDIAGONAL[ (sliderPiece//8)+(sliderPiece%8) ]
		result=leftDiagonal|rightDiagonal
		return result

	#type bishop: int
	#rtype: string
	def bishop_legalMoves(self,bishop,captureOpponentKing=False,returnBitBoard=False):
		positionOfBishop=[]
		li=""
		if(bishop==0):
			pass
		else:
			for i in range(64):
				if((bishop>>i)&1==1):
					positionOfBishop.append(i)

		legalMovesOnBitBoard=0

		for item in positionOfBishop:
			#all valid left and right diagonal moves cannot include positions where there's white pieces
			move=self.leftDiagonalAndRightDiagonalMoves(item)

			if(captureOpponentKing==False):
				move=move&self.NOTPLAYERPIECES
			else:
				pass

			legalMovesOnBitBoard=legalMovesOnBitBoard|move

			if(move==0):
				pass
			else:
				for i in range(64):
					if((move>>i)&1==1):
						#original X, original Y, destination X, destination Y
						li=li+str(item//8)+str(item%8)+str(i//8)+str(i%8)+" "
		if(returnBitBoard==False):
			return li
		else:
			return legalMovesOnBitBoard

	#type queen: int
	#rtype: string
	def queen_legalMoves(self,queen,captureOpponentKing=False,returnBitBoard=False):
		positionOfQueen=[]
		li=""
		if(queen==0):
			pass
		else:
			for i in range(64):
				if((queen>>i)&1==1):
					positionOfQueen.append(i)

		legalMovesOnBitBoard=0
		for item in positionOfQueen:
			#all valid vertical, horizontal and diagonal moves cannot include positions where there's white pieces
			move=(self.verticalAndHorizontalMoves(item)|self.leftDiagonalAndRightDiagonalMoves(item))

			if(captureOpponentKing==False):
				move=move&self.NOTPLAYERPIECES
			else:
				pass

			legalMovesOnBitBoard=legalMovesOnBitBoard|move

			if(move==0):
				pass
			else:
				for i in range(64):
					if((move>>i)&1==1):
						#original X, original Y, destination X, destination Y
						li=li+str(item//8)+str(item%8)+str(i//8)+str(i%8)+" "
		if(returnBitBoard==False):
			return li
		else:
			return legalMovesOnBitBoard

	#type rook: int
	#rtype: string
	def rook_legalMoves(self,rook,captureOpponentKing=False,returnBitBoard=False):
		positionOfRook=[]
		li=""
		if(rook==0):
			pass
		else:
			for i in range(64):
				if((rook>>i)&1==1):
					positionOfRook.append(i)

		legalMovesOnBitBoard=0
		for item in positionOfRook:
			#all valid vertical and horizontal moves cannot include positions where there's white pieces
			move=self.verticalAndHorizontalMoves(item)
			

			if(captureOpponentKing==False):
				move=move&self.NOTPLAYERPIECES
			else:
				pass

			legalMovesOnBitBoard=legalMovesOnBitBoard|move

			if(move==0):
				pass
			else:
				for i in range(64):
					if((move>>i)&1==1):
						#original X, original Y, destination X, destination Y
						li=li+str(item//8)+str(item%8)+str(i//8)+str(i%8)+" "
		if(returnBitBoard==False):
			return li
		else:
			return legalMovesOnBitBoard

	"""
	Algorithm to find all legal horse moves:
	01010000
	10001000
	00H00000
	10001000
	01010000
	00000000
	00000000
	00000000
	1. We will shift this hardcoded board with presetPositions to find the legal horse moves.     18
	2. In this hardcoded board, the position of the Horse is 18.                                  ^
	                                                                                              |
	3. The representation of this board in binary is 000000000000000000000000000010100001000100000H000001000100001010
	4. If the position of our knight is <18, we'll need to shift right by >>(18-knight_position)
	5. Else if the position of our knight is >18, we'll need to shift left by <<(knight_position-18)
	6. However, there's some edge case that we'll need to take care of.
		i. When our knight is at position 17, we right shift by 1. 
			10100001
			00010000
			0H000001
			00010000
			10100000
			00000000
			00000000
			00000000
			However, this is WRONG. Our horse at column 1 can't reach column 7! We will need to do answer & ~(rightTwoColumnOne)
		ii. The same applies when knight is at position 22. We will need to do answer & ~(leftTwoColumnOne)
	"""
	def knight_legalMoves(self,knight,captureOpponentKing=False,returnBitBoard=False):
		positionOfKnight=[]
		li=""
		if(knight==0):
			pass
		else:
			for i in range(64):
				if((knight>>i)&1==1):
					positionOfKnight.append(i)

		legalMovesOnBitBoard=0
		#note that item is location
		for item in positionOfKnight:
			#shift the board with presetPosition to the hose position
			if(item>18):
				move=KNIGHT_2_2<<(item-18)
			else:
				move=KNIGHT_2_2>>(18-item)
			#prevent out of range or illegal move (edge case as stated in our algorithm)
			if((item%8)<4):
				move=move&self.NOT(RIGHTTWOCOLONE)
			else:
				move=move&self.NOT(LEFTTWOCOLONE)


			if(captureOpponentKing==False):
				move=move&self.NOTPLAYERPIECES
			else:
				pass


			legalMovesOnBitBoard=legalMovesOnBitBoard|move

			if(move==0):
				pass
			else:
				for i in range(64):
					if((move>>i)&1==1):
						#original X, original Y, destination X, destination Y
						li=li+str(item//8)+str(item%8)+str(i//8)+str(i%8)+" "

		if(returnBitBoard==False):
			return li
		else:
			return legalMovesOnBitBoard

	"""
	Algorithm to find all legal king moves:
	11100000
	1K100000
	11100000
	00000000
	00000000
	00000000
	00000000
	00000000
	1. We will shift this hardcoded board with presetPositions to find the legal king moves.               9
	2. In this hardcoded board, the position of the King is 9.                                             ^
	                                                                                                       |
	3. The representation of this board in binary is 000000000000000000000000000000000000000000000111000001K100000111
	4. If the position of our king is <9, we'll need to shift right by >>(9-king_position)
	5. Else if the position of our king is >9, we'll need to shift left by <<(king_position-9)
	6. However, there's some edge case that we'll need to take care of.
		i. When our king is at position 8, we right shift by 1. 
		           1
			11000000
			K1000001
			11000000
			00000000
			00000000
			00000000
			00000000
			00000000
			However, this is WRONG. Our king at column 0 can't reach column 7! We will need to do answer & ~(rightTwoColumnOne)
		ii. The same applies when king is at position 15. We will need to do answer & ~(leftTwoColumnOne)
	"""
	#VVVVVVVVVVVVVVVVVVIP: king_legalMoves DOES NOT check for illegal king moves, eg: moves that will place the king in checked or being captured.
	def king_legalMoves(self,king,captureOpponentKing=False,returnBitBoard=False):
		li=""
		kingPosition=-1
		if(king==0):
			raise ValueError("Error in king_legalMoves: There must be one player king on the board.")
		else:
			for i in range(64):
				if((king>>i)&1==1):
					#note that there can only be one player King
					kingPosition=i
					break


		if(kingPosition>9):
			move=KING_1_1<<(kingPosition-9)
		else:
			move=KING_1_1>>(9-kingPosition)
		#prevent out of range or illegal move (edge case as stated in our algorithm)
		if((kingPosition%8)<4):
			move=move&self.NOT(RIGHTTWOCOLONE)
		else:
			move=move&self.NOT(LEFTTWOCOLONE)


		if(captureOpponentKing==False):
			move=move&self.NOTPLAYERPIECES
		else:
			pass

		#if return bitBoard is True. return the move on bitBoard
		if(returnBitBoard==True):
			return move

		#else, return it in legal moves form
		if(move==0):
			pass
		else:
			for i in range(64):
				if((move>>i)&1==1):
					#original X, original Y, destination X, destination Y
					li=li+str(kingPosition//8)+str(kingPosition%8)+str(i//8)+str(i%8)+" "
		
		return li

	#type pos: string of format (original X, orinal Y, destination X, destination Y)
	#rtype: int
	#converts destination X and destination Y to bitboard representation
	def convertRowAndColumnToPositionOnBoard(self,pos):
		x=int(pos[2])
		y=int(pos[3])
		position=(x*8)+y
		binary="0"*64
		binary=binary[position+1:]+"1"+binary[0:position]
		return int(binary,2)


	#type pieces: dictionary
	#rtype: int
	#return a bitboard of moves that will cause white king to be in checked
	def whiteKing_illegalMoves(self,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn):
		self.OCCUPIED=(whiteKing|whiteQueen|whiteBishop|whiteKnight|whiteRook|whitePawn|
			blackKing|blackQueen|blackBishop|blackKnight|blackRook|blackPawn)

		illegalMoves=0
		#########black pawn moves

		#left capture
		blackPawnLeftCapture=(blackPawn<<9)&self.NOT(LEFTCOLONE)
		#right capture
		blackPawnRightCapture=(blackPawn<<7)&self.NOT(RIGHTCOLONE)
		illegalMoves=illegalMoves|(blackPawnLeftCapture|blackPawnRightCapture)

		########black bishop moves
		illegalMoves=illegalMoves|self.bishop_legalMoves(blackBishop,captureOpponentKing=True,returnBitBoard=True)

		########black queen moves
		illegalMoves=illegalMoves|self.queen_legalMoves(blackQueen,captureOpponentKing=True,returnBitBoard=True)

		########black rook moves
		illegalMoves=illegalMoves|self.rook_legalMoves(blackRook,captureOpponentKing=True,returnBitBoard=True)

		########black knight moves
		illegalMoves=illegalMoves|self.knight_legalMoves(blackKnight,captureOpponentKing=True,returnBitBoard=True)

		########black king moves
		illegalMoves=illegalMoves|self.king_legalMoves(blackKing,captureOpponentKing=True,returnBitBoard=True)

		return illegalMoves


	#type pieces: dictionary
	#rtype: int
	#return a bitboard of moves that will cause black king to be in checked
	def blackKing_illegalMoves(self,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn):
		self.OCCUPIED=(whiteKing|whiteQueen|whiteBishop|whiteKnight|whiteRook|whitePawn|
			blackKing|blackQueen|blackBishop|blackKnight|blackRook|blackPawn)

		illegalMoves=0
		#########white pawn moves
		
		#left capture
		whitePawnLeftCapture=(whitePawn>>9)&self.NOT(RIGHTCOLONE)
		#right capture
		whitePawnRightCapture=(whitePawn>>7)&self.NOT(LEFTCOLONE)
		illegalMoves=illegalMoves|(whitePawnLeftCapture|whitePawnRightCapture)

		########white bishop moves
		illegalMoves=illegalMoves|self.bishop_legalMoves(whiteBishop,captureOpponentKing=True,returnBitBoard=True)

		########white queen moves
		illegalMoves=illegalMoves|self.queen_legalMoves(whiteQueen,captureOpponentKing=True,returnBitBoard=True)

		########white rook moves
		illegalMoves=illegalMoves|self.rook_legalMoves(whiteRook,captureOpponentKing=True,returnBitBoard=True)

		########white knight moves
		illegalMoves=illegalMoves|self.knight_legalMoves(whiteKnight,captureOpponentKing=True,returnBitBoard=True)

		########white king moves
		illegalMoves=illegalMoves|self.king_legalMoves(whiteKing,captureOpponentKing=True,returnBitBoard=True)
		
		return illegalMoves

	#NOTE: 
	# -> Corresponding white castle variable is being set to false when white king, white left rook or white right rook is moved.
	# -> Observe that our board is set up with black pieces up, white pieces down. 
	#    If board is flipped, we essentially are representing our black pieces as white pieces, and white pieces as black pieces. However, this also means that
	#    our arrangement for white king, white queen, black king, black queen is flipped in compared to the original board with black pieces up, white pieces down.
	#    We want our method to be able to reflect that.
	#Rules for castling. 
	#	i. No piece of either colour in between the king and the rook
	#	ii. Cannot castle "through" check
	#	iii. Cannot castle when being checked
	#	iv. Cannot castle to the side if rook of the side has been moved. Cannot castle anymore to both sides once king has been moved
	#rtype: list of position for white king castling moves
	def whiteCastling(self,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle):
		li=""
		whiteLeftRook=1<<self.rooks["whiteLeftRook"]
		whiteRightRook=1<<self.rooks["whiteRightRook"]

		#check if there's white left rook
		whiteLeft_hasRook=whiteLeftRook&whiteRook
		#check if there's white right rook
		whiteRight_hasRook=whiteRightRook&whiteRook

		illegalMovesForWhiteKing=self.whiteKing_illegalMoves(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn)

		#if white king is not being checked
		if(illegalMovesForWhiteKing&whiteKing==0):
			#if the king has not been moved and the rook of the side has not been moved
			if(whiteQueenCastle and whiteLeft_hasRook):
				#check if the path from king to left rook is empty, and check if we are castling through check
				#to prevent king from castling through check, we only need to check (7,2) and (7,3), not including (7,1), thus we & it with NOT(1<<57)
				if( ( self.OCCUPIED|(illegalMovesForWhiteKing&self.NOT(1<<57)) ) & (WHITE_QUEENSIDEMOVES)==0):
					#original X, original Y, destination X, destination Y, move type (WL=white left castling)
					li=li+"7472"+"WL"+" "
			if(whiteKingCastle and whiteRight_hasRook):
				#check if the path from king to right rook is empty, and check if we are castling through check
				#to prevent king from castling through check, we only need to check (7,5) and (7,6)
				if((self.OCCUPIED|illegalMovesForWhiteKing)&WHITE_KINGSIDEMOVES==0):
					#original X, original Y, destination X, destination Y, move type (WR=white right castling)
					li=li+"7476"+"WR"+" "
		return li


	#rtype: list of position for black king castling moves
	def blackCastling(self,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle):
		li=""
		blackLeftRook=1<<self.rooks["blackLeftRook"]
		blackRightRook=1<<self.rooks["blackRightRook"]

		#check if there's black left rook
		blackLeft_hasRook=blackLeftRook&blackRook
		#check if there's black right rook
		blackRight_hasRook=blackRightRook&blackRook

		illegalMovesForBlackKing=self.blackKing_illegalMoves(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn)

		#if black king is not being checked
		if(illegalMovesForBlackKing&blackKing==0):
			#if the king has not been moved and the rook of the side has not been moved
			if(blackQueenCastle and blackLeft_hasRook):
				#check if the path from king to left rook is empty, and check if we are castling through check
				#to prevent king from castling through check, we only need to check (0,2) and (0,3), not including (0,1), thus we & it with NOT(1<1)
				if( ( self.OCCUPIED|(illegalMovesForBlackKing&self.NOT(1<<1)) ) & (BLACK_QUEENSIDEMOVES)==0):
					#original X, original Y, destination X, destination Y, move type (BL=black left castling)
					li=li+"0402"+"BL"+" "
			if(blackKingCastle and blackRight_hasRook):
				#check if the path from king to right rook is empty, and check if we are castling through check
				#to prevent king from castling through check, we only need to check (0,5) and (0,6)
				if((self.OCCUPIED|illegalMovesForBlackKing)&BLACK_KINGSIDEMOVES==0):
					#original X, original Y, destination X, destination Y, move type (BR=black right castling)
					li=li+"0406"+"BR"+" "
		return li



	#NOTE: For used by rating.py only.
	#all valid moves for white king, including castling. The move needs to be legal and cannot be illegal. No flipped board allowed.
	def whiteKing_moves(self,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle):
		moves_whiteKing=""
		li=""

		self.NOTPLAYERPIECES=self.NOT(whiteKing|whiteQueen|whiteBishop|whiteKnight|whiteRook|whitePawn|blackKing)
		self.OCCUPIED=(whiteKing|whiteQueen|whiteBishop|whiteKnight|whiteRook|whitePawn|
			blackKing|blackQueen|blackBishop|blackKnight|blackRook|blackPawn)
		self.whiteQueenCastle=whiteQueenCastle
		self.whiteKingCastle=whiteKingCastle
		self.blackQueenCastle=blackQueenCastle
		self.blackKingCastle=blackKingCastle
		moves=self.king_legalMoves(whiteKing,returnBitBoard=True)&self.NOT(self.whiteKing_illegalMoves(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn))
		
		#find the position of white King
		for i in range(64):
			if((whiteKing>>i)&1==1):
				#note that there can only be one player King
				kingPosition=i
				break

		if(moves==0):
			pass
		else:
			for i in range(64):
				if((moves>>i)&1==1):
					moves_whiteKing=moves_whiteKing+str(kingPosition//8)+str(kingPosition%8)+str(i//8)+str(i%8)+" "
		li=moves_whiteKing+self.whiteCastling(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		return li

	#NOTE: For used by rating.py only.
	#all valid moves for black king, including castling. The move needs to be legal and cannot be illegal. No flipped board allowed.
	def blackKing_moves(self,whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle):
		moves_blackKing=""
		li=""

		self.NOTPLAYERPIECES=self.NOT(blackKing|blackQueen|blackBishop|blackKnight|blackRook|blackPawn|whiteKing)
		self.OCCUPIED=(whiteKing|whiteQueen|whiteBishop|whiteKnight|whiteRook|whitePawn|
			blackKing|blackQueen|blackBishop|blackKnight|blackRook|blackPawn)
		self.whiteQueenCastle=whiteQueenCastle
		self.whiteKingCastle=whiteKingCastle
		self.blackQueenCastle=blackQueenCastle
		self.blackKingCastle=blackKingCastle
		moves=self.king_legalMoves(blackKing,returnBitBoard=True)&self.NOT(self.blackKing_illegalMoves(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn))
		
		#find the position of white King
		for i in range(64):
			if((blackKing>>i)&1==1):
				#note that there can only be one player King
				kingPosition=i
				break

		if(moves==0):
			pass
		else:
			for i in range(64):
				if((moves>>i)&1==1):
					moves_blackKing=moves_blackKing+str(kingPosition//8)+str(kingPosition%8)+str(i//8)+str(i%8)+" "
		li=moves_blackKing+self.blackCastling(whiteKing,whiteQueen,whiteBishop,whiteKnight,whiteRook,whitePawn,blackKing,blackQueen,blackBishop,blackKnight,blackRook,blackPawn,whiteQueenCastle,whiteKingCastle,blackQueenCastle,blackKingCastle)
		return li


	#type board: int
	#type move: string
	#type pieceType: string
	#note, our move can be 1213qP
	def makeMove(self,board,move,pieceType):
		try:
			originalX=int(move[0])
			originalY=int(move[1])
			newX=int(move[2])
			newY=int(move[3])
		except(ValueError):
			raise ValueError("Error in makeMove: the first four character of move string must be integer")
		#normal reqular move. NOT castling, enpassant or pawn promotion
		if(len(move)==4):
			start=(originalX*8)+originalY
			end=(newX*8)+newY
			#we will be looping makeMove method for all 12 bitBoards.
			#if this is the board in which we want to move the piece of, then there must be a piece on this board at the start position
			if((board>>start)&1==1):
				#remove the original piece from the board, place it at the destination
				board=board&self.NOT(1<<start)
				board=board|(1<<end)
			#if this is not the board in which we want to move the piece of, there should be nothing at the end position of this board.
			else:
				board=board&self.NOT(1<<end)
		#we know that this is not regular move. This move involves castling, enpassant or pawn promotion
		else:
			#pawn promotion
			if(move[5]=="P"):
				start=ROWALLONE[originalX]&COLALLONE[originalY]
				end=ROWALLONE[newX]&COLALLONE[newY]
				#if this is the board where we do pawn promotion
				#note that our pawn promotion allows us to exchange pawn for queen, bishop, knight and rook
				if(pieceType==move[4]):
					board=board|(end)
				#if this is not the board that we want to do pawn promotion, there shouldn't be any piece at the start and end position of this board
				else:
					##For debugging
					# print("WATCH HERE: Board="+str(board)+"  start="+str(start))
					board=board&self.NOT(start)
					board=board&self.NOT(end)
			#en passant
			elif(move[5]=="E"):
				startPos=(originalX*8)+originalY
				endPos=(newX*8)+newY
				start=ROWALLONE[originalX]&COLALLONE[originalY]
				end=ROWALLONE[newX]&COLALLONE[newY]
				#remove the piece captured by en passant from the board
				if(move[4]=="W"):
					board=board&self.NOT(ROWALLONE[3]&COLALLONE[newY])
				elif(move[4]=="B"):
					board=board&self.NOT(ROWALLONE[4]&COLALLONE[newY])
				#if this is the pawn bitboard in which we are going to perform the en passant move, we are going to update the new position of the piece
				if((board>>startPos)&1==1):
					board=board&self.NOT(start)
					board=board|(end)
			#castling
			elif(move[5]=="L" or move[5]=="R"):
				#castling
				pass
			else:
				raise ValueError("Error in makeMove: Invalid argument for pieceType")
		return board

	#NOTE: IMPORTANT! kingBoard and rookBoard must have the same colour
	#this method moves the rook (ROOK ONLY. NO MOVE KING!) to the corresponding position if the castling move is valid.
	#rtype: int. return kingBoard,rookBoard
	def makeCastlingMove(self,kingBoard,rookBoard,move):
		if(not(move[5]=="L" or move[5]=="R")):
			raise ValueError("Error in makeCastlingMove: Argument move must be a castling move.")
		try:
			originalX=int(move[0])
			originalY=int(move[1])
			newX=int(move[2])
			newY=int(move[3])
		except(ValueError):
			raise ValueError("Error in makeCastlingMove: the first four character of move string must be integer")

		moveIndex=move[0:4]
		validCastlingMove=["0402","0406","7472","7476"]
		start=(originalX*8)+originalY
		end=(newX*8)+newY

		validCastling=False

		if( ((kingBoard>>start)&1==1) and (moveIndex in validCastlingMove) ):
			#move for rook board
			##if white king castling
			if(move[4]=="W"):
				if(moveIndex=="7472"):
					#remove white left rook from rook bitBoard
					rookBoard=rookBoard&self.NOT(1<<self.rooks["whiteLeftRook"])
					#put white left rook at position (7,3)
					rookBoard=rookBoard|( 1<<(self.rooks["whiteLeftRook"]+3) )
					validCastling=True
				elif(moveIndex=="7476"):
					#remove white right rook from rook butBoard
					rookBoard=rookBoard&self.NOT(1<<self.rooks["whiteRightRook"])
					#put white right rook at position (7,5)
					rookBoard=rookBoard|( 1<<(self.rooks["whiteRightRook"]-2) )
					validCastling=True
				else:
					raise ValueError("Error in makeCastlingMove: Invalid argument for move. Not a castling move.")
			##if black king castling
			elif(move[4]=="B"):
				if(moveIndex=="0402"):
					#remove black left rook from rook bitBoard
					rookBoard=rookBoard&self.NOT(1<<self.rooks["blackLeftRook"])
					#put black left rook at position (0,3)
					rookBoard=rookBoard|( 1<<(self.rooks["blackLeftRook"]+3) )
					validCastling=True
				elif(moveIndex=="0406"):
					#remove black right rook from rook butBoard
					rookBoard=rookBoard&self.NOT(1<<self.rooks["blackRightRook"])
					#put black right rook at position (0,5)
					rookBoard=rookBoard|( 1<<(self.rooks["blackRightRook"]-2) )
					validCastling=True
				else:
					raise ValueError("Error in makeCastlingMove: Invalid argument for move. Not a castling move.")
			else:
				raise ValueError("Error in makeCastlingMove: Invalid argument for move. Not a castling move.")

			#move for king board
			if(validCastling):
				kingBoard=kingBoard&self.NOT(1<<start)
				kingBoard=kingBoard|(1<<end)
				validCastling=False

		return kingBoard,rookBoard





"""
TODO:
Note to self
Problems
1. King moves does not check for illegal king moves (SOLVED)
2. If king is checked, we CAN'T MOVE other pieces that won't prevent king from being checked. In other words, we need to move a piece in which king will not be
   be checked. (SOLVED)
3. Update castling variable when king or rook is moved. (SOLVED)
4. makeCastlingMove only move rooks to corresponding position. It didn't move our king.   (SOLVED)
"""
