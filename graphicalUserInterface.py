#!/usr/bin/env python3

"""
@author: Foo Zhi Yuan
ChessAI is being implemented using the concepts of bitboard and principal variation search
Requires Python 3 and Pillow(for GUI)
USAGE: python chessAI.py to play in GUI and python chessAI_console.py to play in console
"""

import tkinter as tk
from PIL import Image, ImageTk
from board import Board
from moves import Moves
from principalVariation import PrincipalVariation
from PawnPromotionPieceNotDefinedError import PawnPromotionPieceNotDefinedError
import math


class GraphicalUserInterface:
	#root
	master=None
	#chessBoard data fields
	playerIsWhite=None
	whiteTurn=None
	squareTileSize=None
	selectedPiece=None
	highlightedPosition=None
	allLegalMoves=None
	canvas=None
	leftFrame=None
	rightFrame=None
	statusBox=None
	chessBoard=None
	#mapping dictionary
	x_axisMap={}
	pieceImage={}
	#chess mode. One of this NEEDS to be True
	player_vs_player=False
	player_vs_AI=False
	#cache
	#stores information needed for pawn promotion before update_idletasks wipes it out
	pawnPromotionCache=None
	#
	moves=None
	board=None
	principalVariation=None
	maxDepth=None

	def initGUI(self):
		self.whiteTurn=True
		self.maxDepth=3
		self.moves=Moves()
		self.board=Board()
		self.principalVariation=PrincipalVariation(self.moves,self.playerIsWhite,self.maxDepth)
		self.board.initChess(self.moves,self.playerIsWhite,gui=True)
		self.x_axisMap={0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H"}
		self.highlightedPosition=[]

		#restore GUI data field to its initial state
		self.selectedPiece=None
		self.allLegalMoves=None
		self.canvas=None
		self.chessBoard=None
		#uncomment this
		# self.player_vs_player=False
		# self.player_vs_AI=False


		self.master.title("ChessAI")
		##Initalise pieces' images
		#initialise white pieces' images
		self.pieceImage["whiteKing"]=ImageTk.PhotoImage(file="pieceImage/whiteKing.png",width=32,height=32)
		self.pieceImage["whiteQueen"]=ImageTk.PhotoImage(file="pieceImage/whiteQueen.png",width=32,height=32)
		self.pieceImage["whiteBishop"]=ImageTk.PhotoImage(file="pieceImage/whiteBishop.png",width=32,height=32)
		self.pieceImage["whiteKnight"]=ImageTk.PhotoImage(file="pieceImage/whiteKnight.png",width=32,height=32)
		self.pieceImage["whiteRook"]=ImageTk.PhotoImage(file="pieceImage/whiteRook.png",width=32,height=32)
		self.pieceImage["whitePawn"]=ImageTk.PhotoImage(file="pieceImage/whitePawn.png",width=32,height=32)
		#initialise black pieces' images
		self.pieceImage["blackKing"]=ImageTk.PhotoImage(file="pieceImage/blackKing.png",width=32,height=32)
		self.pieceImage["blackQueen"]=ImageTk.PhotoImage(file="pieceImage/blackQueen.png",width=32,height=32)
		self.pieceImage["blackBishop"]=ImageTk.PhotoImage(file="pieceImage/blackBishop.png",width=32,height=32)
		self.pieceImage["blackKnight"]=ImageTk.PhotoImage(file="pieceImage/blackKnight.png",width=32,height=32)
		self.pieceImage["blackRook"]=ImageTk.PhotoImage(file="pieceImage/blackRook.png",width=32,height=32)
		self.pieceImage["blackPawn"]=ImageTk.PhotoImage(file="pieceImage/blackPawn.png",width=32,height=32)

	"""
	called by parent method promptPlayerColour()
	set the data field(class variable) playerIsWhite based on the option that player chose.
	"""
	def setPlayerIsWhite(self,playerIsWhite,promptPopUp):
		self.playerIsWhite=playerIsWhite
		promptPopUp.destroy()
		self.initGUI()
		self.master.deiconify()
		self.initCanvas()
		


	"""
	called by parent method getPieceToPromote()
	makes the pawn promotion move and set the piece which player chose to promote on board
	"""
	def setPieceToPromote(self,pieceToPromote,prompt):
		Board=self.board
		prompt.destroy()
		Board.updateMove(self.pawnPromotionCache+pieceToPromote,gui=True)
		#update status box
		boardMove=self.convertInternalNumericalMoveToBoardMove(self.pawnPromotionCache)
		if(self.player_vs_player):
			if(self.whiteTurn):
				self.setStatusBox("White makes move "+boardMove+".\nPawn Promotion!\nBlack's turn.")
			else:
				self.setStatusBox("Black makes move "+boardMove+".\nPawn Promotion!\nWhite's turn.")
		elif(self.player_vs_AI):
			self.setStatusBox("Player makes move "+boardMove+".\nPawn Promotion!\nComputer's turn.\nComputer is thinking .....")

		self.chessBoard=Board.chessBoard
		self.whiteTurn=not self.whiteTurn
		Board.getAllCurrentLegalMoves(self.whiteTurn)
		self.allLegalMoves=Board.currentAllLegalMoves

		#reset the variables for the board since we already made our move
		self.pawnPromotionCache=None
		self.selectedPiece=None
		self.highlightedPosition=None
		self.refreshBoard(refreshAllPieces=False)
		self.redrawAllPieces()

		self.checkForCheckmate()

		self.master.update_idletasks()
		#if this is a player vs AI game, AI needs to make move
		if(self.player_vs_AI):
			self.AI_makesMove()

	"""
	called by parent method initCanvas()
	set the game mode for the chess game based on the radio button that player selects
	"""
	def setGameMode(self,gameMode):
		if(gameMode.get()==1):
			self.player_vs_AI=True
			self.player_vs_player=False
		elif(gameMode.get()==2):
			self.player_vs_player=True
			self.player_vs_AI=False

		#only after player has chose the game mode that we read their mouse click input	
		self.master.update_idletasks()
		#detect left click button
		self.canvas.bind("<Button-1>",self.leftSingleMouseClick)

		#if this is player vs AI game and it is not player's turn, AI makes move
		if(self.player_vs_AI):
			if(self.playerIsWhite!=self.whiteTurn):
				self.setStatusBox("Computer is thinking .....")
				self.AI_makesMove()



	"""
	A pop up that prompts player for player colour
	"""
	def promptPlayerColour(self):
		promptPopUp=tk.Toplevel()
		promptPopUp.title("ChessAI")
		#A frame is rectangular region on the screen. The frame widget is mainly used as a geometry master for other widgets, or to provide padding between other widgets.
		frame1=tk.Frame(promptPopUp)
		frame1.pack()
		question=tk.Label(frame1,text="Please select your piece colour.",fg="black",font=("Times",18))
		question.pack(padx=30,pady=15)

		#create a one beautiful line separator to separate between question and the 2 buttons
		separator=tk.Frame(frame1,height=2,bd=1,relief=tk.SUNKEN)
		separator.pack(fill=tk.X,padx=5,pady=5)

		frame2=tk.Frame(promptPopUp)
		frame2.pack(side=tk.BOTTOM)

		#VVVVVVIP
		#command takes in a callable python *OBJECT*
		#hello() is not an object. The name of the method hello is an object.
		#if hello() is passed to command, it will call the method first before creating the button. This is NOT what we want. So we use lambda.
		whiteButton=tk.Button(frame1,text="White",font="Times 15",fg="black",command=lambda: self.setPlayerIsWhite(True,promptPopUp),width=20)
		whiteButton.pack(side=tk.LEFT,padx=15,pady=10)

		blackButton=tk.Button(frame1,text="Black",font="Times 15",fg="black",command=lambda: self.setPlayerIsWhite(False,promptPopUp),width=20)
		blackButton.pack(side=tk.RIGHT,padx=15,pady=10)

		watermark=tk.Label(frame2,text="A product of Foo Zhi Yuan",fg="black",font=("Verdana",10,"bold","italic"))
		watermark.pack(side=tk.BOTTOM,pady=10)

		self.master.update_idletasks()

	"""
	A pop up that prompts player to choose the piece to promote when his pawn reached the end of the board
	"""
	def getPieceToPromote(self):
		prompt=tk.Toplevel()
		prompt.title("ChessAI")
		frame1=tk.Frame(prompt)
		frame1.pack()
		question=tk.Label(frame1,text="Please select a piece to promote",fg="black",font=("Verdana",18,"bold"))
		question.pack(padx=30,pady=15)

		separator=tk.Frame(frame1,height=2,bd=1,relief=tk.SUNKEN)
		separator.pack(fill=tk.X,padx=5,pady=5)

		frame2=tk.Frame(prompt)
		frame2.pack(side=tk.BOTTOM)

		if(self.playerIsWhite):
			whiteQueenButton=tk.Button(frame1,text="White Queen",font="Times 15",fg="black",command=lambda: self.setPieceToPromote("QP",prompt),width=20)
			whiteQueenButton.pack(side=tk.LEFT,padx=10,pady=10)
			whiteBishopButton=tk.Button(frame1,text="White Bishop",font="Times 15",fg="black",command=lambda: self.setPieceToPromote("BP",prompt),width=20)
			whiteBishopButton.pack(side=tk.LEFT,padx=10,pady=10)
			whiteKnightButton=tk.Button(frame1,text="White Knight",font="Times 15",fg="black",command=lambda: self.setPieceToPromote("HP",prompt),width=20)
			whiteKnightButton.pack(side=tk.LEFT,padx=10,pady=10)
			whiteRookButton=tk.Button(frame1,text="White Rook",font="Times 15",fg="black",command=lambda: self.setPieceToPromote("RP",prompt),width=20)
			whiteRookButton.pack(side=tk.LEFT,padx=10,pady=10)
		elif(not self.playerIsWhite):
			blackQueenButton=tk.Button(frame1,text="Black Queen",font="Times 15",fg="black",command=lambda: self.setPieceToPromote("qP",prompt),width=20)
			blackQueenButton.pack(side=tk.LEFT,padx=10,pady=10)
			blackBishopButton=tk.Button(frame1,text="Black Bishop",font="Times 15",fg="black",command=lambda: self.setPieceToPromote("bP",prompt),width=20)
			blackBishopButton.pack(side=tk.LEFT,padx=10,pady=10)
			blackKnightButton=tk.Button(frame1,text="Black Knight",font="Times 15",fg="black",command=lambda: self.setPieceToPromote("hP",prompt),width=20)
			blackKnightButton.pack(side=tk.LEFT,padx=10,pady=10)
			blackRookButton=tk.Button(frame1,text="Black Rook",font="Times 15",fg="black",command=lambda: self.setPieceToPromote("rP",prompt),width=20)
			blackRookButton.pack(side=tk.LEFT,padx=10,pady=10)


		watermark=tk.Label(frame2,text="A product of Foo Zhi Yuan",fg="black",font=("Verdana",10,"bold","italic"))
		watermark.pack(side=tk.BOTTOM,pady=10)

		self.master.update_idletasks()

	def setStatusBox(self,text):
		self.statusBox.delete("1.0",tk.END)
		self.statusBox.insert(tk.END,text)


	def outOfRange(self,x,y):
		if(x<0 or x>7 or y<0 or y>7):
			return True
		else:
			return False

	"""
	sanitize mouse click by player to match the internal chessBoard implementation of black on top and white at bottom
	"""
	def sanitizeMouseClickPosition(self,x,y):
		if(not self.outOfRange(x,y)):
			if(not self.playerIsWhite):
				x=7-x
				y=7-y
			return x,y
		else:
			return -1,-1	

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

	def restartGame(self,root=None):
		if(root!=None):
			root.destroy()
		self.master.withdraw()
		self.canvas.destroy()
		self.leftFrame.destroy()
		self.rightFrame.destroy()
		self.promptPlayerColour()


	def exitGame(self,root):
		root.destroy()
		self.master.destroy()

	def checkForCheckmate(self):
		if(len(self.allLegalMoves)==0):
			self.displayGameEnds()
		else:
			pass
		
	"""
	A pop up that displays the side that win the game.
	"""
	def displayGameEnds(self):
		gameEndsPopUp=tk.Toplevel()
		gameEndsPopUp.title("ChessAI")
		frame1=tk.Frame(gameEndsPopUp)
		frame1.pack()
		#if this is player vs player mode
		if(self.player_vs_player):
			#if this is white turn and white has no place to move, black wins
			if(self.whiteTurn):
				statement=tk.Label(frame1,text="Black wins! Better luck next time White.",fg="black",font=("Verdana",20))
			#if this is black turn and black has no place to move, white wins
			elif(not self.whiteTurn):
				statement=tk.Label(frame1,text="White wins! Better luck next time Black.",fg="black",font=("Verdana",20))
		elif(self.player_vs_AI):
			#if this is player's turn and player has no place to move, computer wins
			if(self.playerIsWhite==self.whiteTurn):
				statement=tk.Label(frame1,text="Computer wins. Better luck next time!",fg="black",font=("Verdana",20))
			#if this is computer's turn and computer has no place to move, player wins
			else:
				statement=tk.Label(frame1,text="Winner winner chicken dinner! You win!",fg="black",font=("Verdana",20))
		statement.pack(padx=40,pady=20)

		separator=tk.Frame(frame1,height=2,bd=1,relief=tk.SUNKEN)
		separator.pack(fill=tk.X,padx=5,pady=5)

		frame2=tk.Frame(gameEndsPopUp)
		frame2.pack()
		newGameButton=tk.Button(frame1,text="New Game",font="Times 15",fg="black",command=lambda: self.restartGame(gameEndsPopUp),width=30)
		newGameButton.pack(side=tk.LEFT,padx=15,pady=10)
		exitGameButton=tk.Button(frame1,text="Exit Game",font="Times 15",fg="black",command=lambda: self.exitGame(gameEndsPopUp),width=30)
		exitGameButton.pack(side=tk.RIGHT,padx=15,pady=10)

		watermark=tk.Label(frame2,text="A product of Foo Zhi Yuan",fg="black",font=("Verdana",10,"bold","italic"))
		watermark.pack(side=tk.BOTTOM,pady=10)

		self.master.update_idletasks()



	def leftSingleMouseClick(self,event):
		if(self.player_vs_player==True):
			self.leftSingleMouseClick_player_vs_player(event)
		elif(self.player_vs_AI==True):
			self.leftSingleMouseClick_player_vs_AI(event)
		elif(self.player_vs_player==False and self.player_vs_AI==False):
			#TODO: do something
			pass

	def leftSingleMouseClick_player_vs_player(self,event):
		Board=self.board

		#detect which square the player has clicked on
		#One square tile
		#  _             
		# |_|64		   
		# 64
		squareTileWidth=self.squareTileSize
		squareTileHeight=self.squareTileSize

		currentX=event.y//squareTileHeight
		#currentY needs to minus the space for y axis bar at left side of the canvas
		currentY=(event.x-(self.squareTileSize//2))//squareTileWidth

		positionX,positionY=self.sanitizeMouseClickPosition(currentX,currentY)
		#if user clicked on the area that is out of range of the board, ignore.
		if(positionX==-1 and positionY==-1):
			return
		"""
		Idea: 
		1.
		if we have selected a piece, the piece can only move to highlighted position. 
		If we choose to move to an invalid (not highlighted position), we want the highlight to disappear. 
		However, if the non highlighted position is a valid old X, old Y, we want to highlight all the possible move from the old X, old Y
		If we choose to move to a valid position (highlighted position), we want the highlight to disappear.
		2.
		if we haven't select a piece, we pass the piece to highlight method to highlight all the position that can be moved by the piece and select the piece.
		"""
		if(self.selectedPiece!=None):
			try:
				Board.updateMove(str(self.selectedPiece[0])+str(self.selectedPiece[1])+str(positionX)+str(positionY),gui=True)
				#update statusBox
				boardMove=self.convertInternalNumericalMoveToBoardMove(str(self.selectedPiece[0])+str(self.selectedPiece[1])+str(positionX)+str(positionY))
				if(self.whiteTurn):
					self.setStatusBox("White makes move "+boardMove+".\nBlack's turn.")
				else:
					self.setStatusBox("Black makes move "+boardMove+".\nWhite's turn.")


				self.chessBoard=Board.chessBoard

				self.whiteTurn=not self.whiteTurn
				Board.getAllCurrentLegalMoves(self.whiteTurn)
				self.allLegalMoves=Board.currentAllLegalMoves

				self.checkForCheckmate()
			except(ValueError):
				pass
			except(PawnPromotionPieceNotDefinedError):
				self.pawnPromotionCache=self.selectedPiece+str(positionX)+str(positionY)
				self.getPieceToPromote()
				
			self.selectedPiece=None
			self.highlightedPosition=None
			self.refreshBoard(refreshAllPieces=False)
			self.redrawAllPieces()

		self.highlightPossibleMoves(positionX,positionY)
		self.refreshBoard(refreshAllPieces=True)
	

	def leftSingleMouseClick_player_vs_AI(self,event):
		if(not (self.playerIsWhite==self.whiteTurn)):
			return

		Board=self.board
		#detect which square the player has clicked on
		#One square tile
		#  _             
		# |_|64		   
		# 64
		squareTileWidth=self.squareTileSize
		squareTileHeight=self.squareTileSize

		currentX=event.y//squareTileHeight
		#currentY needs to minus the space for y axis bar at left side of the canvas
		currentY=(event.x-(self.squareTileSize//2))//squareTileWidth

		positionX,positionY=self.sanitizeMouseClickPosition(currentX,currentY)
		#if user clicked on the area that is out of range of the board, ignore.
		if(positionX==-1 and positionY==-1):
			return
		"""
		Idea: 
		1.
		if we have selected a piece, the piece can only move to highlighted position. 
		If we choose to move to an invalid (not highlighted position), we want the highlight to disappear. 
		However, if the non highlighted position is a valid old X, old Y, we want to highlight all the possible move from the old X, old Y
		If we choose to move to a valid position (highlighted position), we want the highlight to disappear.
		2.
		if we haven't select a piece, we pass the piece to highlight method to highlight all the position that can be moved by the piece and select the piece.
		"""
		if(self.selectedPiece!=None):
			try:
				Board.updateMove(str(self.selectedPiece[0])+str(self.selectedPiece[1])+str(positionX)+str(positionY),gui=True)
				#update statusBox
				boardMove=self.convertInternalNumericalMoveToBoardMove(str(self.selectedPiece[0])+str(self.selectedPiece[1])+str(positionX)+str(positionY))
				self.setStatusBox("Player makes move "+boardMove+".\nComputer's turn.\nComputer is thinking .....")

				self.chessBoard=Board.chessBoard

				self.whiteTurn=not self.whiteTurn
				Board.getAllCurrentLegalMoves(self.whiteTurn)
				self.allLegalMoves=Board.currentAllLegalMoves

			except(ValueError):
				pass
			except(PawnPromotionPieceNotDefinedError):
				self.pawnPromotionCache=self.selectedPiece+str(positionX)+str(positionY)
				self.getPieceToPromote()
				
			self.selectedPiece=None
			self.highlightedPosition=None
			self.refreshBoard(refreshAllPieces=False)
			self.redrawAllPieces()

		self.highlightPossibleMoves(positionX,positionY)
		self.refreshBoard(refreshAllPieces=True)

		self.master.update_idletasks()

		if(self.playerIsWhite!=self.whiteTurn):
			self.checkForCheckmate()
			self.AI_makesMove()

	def AI_makesMove(self):
		#if it's player's turn and not computer's turn
		if(self.playerIsWhite==self.whiteTurn):
			return

		Board=self.board

		bestScore,bestMove=self.principalVariation.principalVariationSearch(-math.inf,math.inf,Board.history,Board.whiteKing,Board.whiteQueen,Board.whiteBishop,Board.whiteKnight,Board.whiteRook,Board.whitePawn,Board.blackKing,Board.blackQueen,Board.blackBishop,Board.blackKnight,Board.blackRook,Board.blackPawn,Board.whiteQueenCastle,Board.whiteKingCastle,Board.blackQueenCastle,Board.blackKingCastle,self.whiteTurn,0)
		if(bestMove=="No Move"):
			return
		Board.updateMove(bestMove,gui=True)
		#update statusBox
		boardMove=self.convertInternalNumericalMoveToBoardMove(str(bestMove))
		self.setStatusBox("Computer makes move "+boardMove+".\nPlayer's turn.")

		self.chessBoard=Board.chessBoard

		self.selectedPiece=None
		self.highlightedPosition=None
		self.refreshBoard(refreshAllPieces=False)
		self.redrawAllPieces()

		self.whiteTurn=not self.whiteTurn
		Board.getAllCurrentLegalMoves(self.whiteTurn)
		self.allLegalMoves=Board.currentAllLegalMoves
		self.checkForCheckmate()

	#when user clicked on a valid selected piece, highlight all the possible moves that can be made by the piece
	def highlightPossibleMoves(self,x,y):
		validPieceSelected=False
		self.highlightedPosition=[]

		for i in range(len(self.allLegalMoves)):
			possMove=self.allLegalMoves[i]
			if(int(possMove[0])==x and int(possMove[1])==y):
				if(self.playerIsWhite):
					self.highlightedPosition.append(str(possMove[2])+str(possMove[3]))
				elif(not self.playerIsWhite):
					possMoveX=7-int(possMove[2])
					possMoveY=7-int(possMove[3])
					self.highlightedPosition.append(str(possMoveX)+str(possMoveY))
				validPieceSelected=True

		if(validPieceSelected):
			self.selectedPiece=str(x)+str(y)

	def refreshBoard(self,event={},refreshAllPieces=True):
		if(event):
			squareTileWidth=(event.width)//9
			squareTileHeight=(event.height)//9
			self.squareTileSize=min(squareTileWidth,squareTileHeight)
			self.canvas.delete("axisLabel")

		self.canvas.delete("squareTile")

		currentColour="white"

		#row
		for i in range(8):
			#column
			for j in range(8):
				#top left corner coordinate of square tile
				originalX=j*self.squareTileSize+self.squareTileSize//2
				originalY=i*self.squareTileSize
				#bottom right corner coordinate of square tile
				newX=originalX+self.squareTileSize
				newY=originalY+self.squareTileSize
				if(self.highlightedPosition!=None):
					#if current tile is in highlighted position, highlight it!
					if((str(i)+str(j)) in self.highlightedPosition):
													#top left X,Y       #bottom right X,Y  
						self.canvas.create_rectangle(originalX,originalY,newX,newY,outline="black",fill="spring green",tags="squareTile")
					else: 
												#top left X,Y        #bottom right X,Y
						self.canvas.create_rectangle(originalX,originalY,newX,newY,outline="black",fill=currentColour,tags="squareTile")
				else: 
											#top left X,Y        #bottom right X,Y
					self.canvas.create_rectangle(originalX,originalY,newX,newY,outline="black",fill=currentColour,tags="squareTile")
				if(currentColour=="white"):
					currentColour="gray52"
				elif(currentColour=="gray52"):
					currentColour="white"
			if(currentColour=="white"):
				currentColour="gray52"
			elif(currentColour=="gray52"):
				currentColour="white"

		##Coordinates label for x axis and y axis.
		labelBarSize=self.squareTileSize//2
		#label for x axis (bottom)
		y=8*self.squareTileSize+labelBarSize//2
		for j in range(8):
			x=j*self.squareTileSize+self.squareTileSize
			self.canvas.create_text(x,y,text=self.x_axisMap[j],font=("Verdana",15,"bold"),fill="white",tags="axisLabel")

		x=labelBarSize//2
		#label for y axis (side)
		for i in range(8):
			y=i*self.squareTileSize+self.squareTileSize//2
			self.canvas.create_text(x,y,text=str(7-i+1),font=("Verdana",15,"bold"),fill="white",tags="axisLabel")

		if(refreshAllPieces==True):
			self.refreshAllPieces()

	#create new piece and place it at position x,y. Used by method redrawAllPieces
	def createAndPlaceNewPiece(self,newPieceName,newPieceImage,x,y):
		temp=x
		x=y
		y=temp
			#skips y axis label at side      #place new piece at the center of coordinate          
		x=self.squareTileSize//2         +    x*self.squareTileSize+self.squareTileSize//2
		    #place new piece at the center of coordinate
		y=y*self.squareTileSize+self.squareTileSize//2
		self.canvas.create_image(x,y,image=newPieceImage,anchor="c",tags=(newPieceName,"piece"))

	#move current pieces to position x,y WITHOUT creating new piece. Used by method refreshAllPieces
	def movePiece(self,newPieceName,x,y):
		temp=x
		x=y
		y=temp
			#skips y axis label at side      #place new piece at the center of coordinate          
		x=self.squareTileSize//2          +   x*self.squareTileSize+self.squareTileSize//2
		    #place new piece at the center of coordinate
		y=y*self.squareTileSize+self.squareTileSize//2
		self.canvas.coords(newPieceName,x,y)


	#redraw all pieces on an empty board by moving their coordinates to new position, WITHOUT introducing new pieces
	def refreshAllPieces(self):
		if(self.chessBoard==None):
			raise ValueError("Error in redrawAllPieces: chessBoard is None.")

		for i in range(8):
			for j in range(8):
				#white pieces
				if(self.chessBoard[i][j]=="K"):
					self.movePiece("whiteKing "+str(i)+str(j),i,j)
				elif(self.chessBoard[i][j]=="Q"):
					self.movePiece("whiteQueen "+str(i)+str(j),i,j)
				elif(self.chessBoard[i][j]=="B"):
					self.movePiece("whiteBishop "+str(i)+str(j),i,j)
				elif(self.chessBoard[i][j]=="H"):
					self.movePiece("whiteKnight "+str(i)+str(j),i,j)
				elif(self.chessBoard[i][j]=="R"):
					self.movePiece("whiteRook "+str(i)+str(j),i,j)
				elif(self.chessBoard[i][j]=="P"):
					self.movePiece("whitePawn "+str(i)+str(j),i,j)
				#black pieces
				elif(self.chessBoard[i][j]=="k"):
					self.movePiece("blackKing "+str(i)+str(j),i,j)
				elif(self.chessBoard[i][j]=="q"):
					self.movePiece("blackQueen "+str(i)+str(j),i,j)
				elif(self.chessBoard[i][j]=="b"):
					self.movePiece("blackBishop "+str(i)+str(j),i,j)
				elif(self.chessBoard[i][j]=="h"):
					self.movePiece("blackKnight "+str(i)+str(j),i,j)
				elif(self.chessBoard[i][j]=="r"):
					self.movePiece("blackRook "+str(i)+str(j),i,j)
				elif(self.chessBoard[i][j]=="p"):
					self.movePiece("blackPawn "+str(i)+str(j),i,j)
		self.canvas.tag_raise("piece")
		self.canvas.tag_lower("squareTile")



	def redrawAllPieces(self):
		if(self.chessBoard==None):
			raise ValueError("Error in redrawAllPieces: chessBoard is None.")

		self.canvas.delete("piece")

		for i in range(8):
			for j in range(8):
				#white pieces
				if(self.chessBoard[i][j]=="K"):
					self.createAndPlaceNewPiece("whiteKing "+str(i)+str(j),self.pieceImage["whiteKing"],i,j)
				elif(self.chessBoard[i][j]=="Q"):
					self.createAndPlaceNewPiece("whiteQueen "+str(i)+str(j),self.pieceImage["whiteQueen"],i,j)
				elif(self.chessBoard[i][j]=="B"):
					self.createAndPlaceNewPiece("whiteBishop "+str(i)+str(j),self.pieceImage["whiteBishop"],i,j)
				elif(self.chessBoard[i][j]=="H"):
					self.createAndPlaceNewPiece("whiteKnight "+str(i)+str(j),self.pieceImage["whiteKnight"],i,j)
				elif(self.chessBoard[i][j]=="R"):
					self.createAndPlaceNewPiece("whiteRook "+str(i)+str(j),self.pieceImage["whiteRook"],i,j)
				elif(self.chessBoard[i][j]=="P"):
					self.createAndPlaceNewPiece("whitePawn "+str(i)+str(j),self.pieceImage["whitePawn"],i,j)
				#black pieces
				elif(self.chessBoard[i][j]=="k"):
					self.createAndPlaceNewPiece("blackKing "+str(i)+str(j),self.pieceImage["blackKing"],i,j)
				elif(self.chessBoard[i][j]=="q"):
					self.createAndPlaceNewPiece("blackQueen "+str(i)+str(j),self.pieceImage["blackQueen"],i,j)
				elif(self.chessBoard[i][j]=="b"):
					self.createAndPlaceNewPiece("blackBishop "+str(i)+str(j),self.pieceImage["blackBishop"],i,j)
				elif(self.chessBoard[i][j]=="h"):
					self.createAndPlaceNewPiece("blackKnight "+str(i)+str(j),self.pieceImage["blackKnight"],i,j)
				elif(self.chessBoard[i][j]=="r"):
					self.createAndPlaceNewPiece("blackRook "+str(i)+str(j),self.pieceImage["blackRook"],i,j)
				elif(self.chessBoard[i][j]=="p"):
					self.createAndPlaceNewPiece("blackPawn "+str(i)+str(j),self.pieceImage["blackPawn"],i,j)
		self.canvas.tag_raise("piece")
		self.canvas.tag_lower("squareTile")
	


	#we define the size of one square tile as 64. We need 8x8 this square tile.
	def initCanvas(self):
		Board=self.board
		self.squareTileSize=64
		                                     #for x axis bar
		canvasHeight=8*self.squareTileSize+self.squareTileSize//2
		                                     #for y axis bar
		canvasWidth=8*self.squareTileSize+self.squareTileSize//2
		self.leftFrame=tk.Frame(self.master)
		self.leftFrame.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
		self.canvas=tk.Canvas(self.leftFrame,width=canvasWidth,height=canvasHeight,background="gray27")
		self.canvas.pack(side="top",fill="both",anchor="center",expand=True)

		#get the initial state of chessBoard and all legal moves that can be made by white at the beginning of game.
		self.chessBoard=Board.chessBoard
		Board.getAllCurrentLegalMoves(self.whiteTurn)
		self.allLegalMoves=Board.currentAllLegalMoves

		#draw the initial state of chessBoard on canvas
		self.refreshBoard()
		self.redrawAllPieces()
		
		#detect enlargement or minimization of windows
		self.canvas.bind("<Configure>",self.refreshBoard)
		#radio button to choose the game mode
		self.rightFrame=tk.Frame(self.master)
		self.rightFrame.pack(side=tk.LEFT)
		mode=tk.IntVar()
		player_vs_AI_button=tk.Radiobutton(self.rightFrame,text="Player vs AI",font=("Verdana",18,"bold"),pady=0,variable=mode,value=1)
		player_vs_AI_button.pack(side=tk.TOP,anchor=tk.W)

		player_vs_player_button=tk.Radiobutton(self.rightFrame,text="Player vs Player",font=("Verdana",18,"bold"),pady=10,variable=mode,value=2)
		player_vs_player_button.pack(side=tk.TOP,anchor=tk.W)

		start_button=tk.Button(self.rightFrame,text="Start",font=("Verdana",18,"bold"),fg="black",command=lambda: self.setGameMode(mode),width=15)
		start_button.pack(side=tk.TOP,padx=10,pady=10)

		restart_button=tk.Button(self.rightFrame,text="New Game",font=("Verdana",18,"bold"),fg="black",command=lambda: self.restartGame(),width=15)
		restart_button.pack(side=tk.TOP,padx=10,pady=10)

		self.statusBox=tk.Text(self.rightFrame,fg="black",bg="LightSkyBlue1",width=26,height=5)
		self.statusBox.pack(side=tk.TOP,fill=tk.X,padx=10,pady=10)
		self.statusBox.config(font=("Times",15))
		self.statusBox.insert(tk.END,"Welcome to ChessAI!\nTo play a game, select a\ngame mode and press Start.")

		watermark=tk.Label(self.rightFrame,text="A product of Foo Zhi Yuan",fg="black",font=("Verdana",10,"bold","italic"))
		watermark.pack(side=tk.BOTTOM,anchor=tk.S,pady=10)

		self.master.update_idletasks()

	def main(self):
		self.master=tk.Tk()
		self.master.withdraw()
		self.promptPlayerColour()
		self.master.mainloop()
		




























	