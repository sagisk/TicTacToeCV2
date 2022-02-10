#!/usr/bin/env python3
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

imgCanvas = np.zeros((480, 640, 3), np.uint8)
detector = HandDetector(detectionCon=0.8)

class Board:
	def __init__(self, state, img):
		self.state=state
		self.img=img
		self.board = np.zeros(9)


	def drawHands(self):
		"""
        Tests if a specific player wins.
        :param player: a human or a computer
        :return: True if the player wins
        """
		self.img = detector.findHands(self.img)
		lmList, bboxInfo = detector.findPosition(self.img)
		return lmList, bboxInfo


	def drawBoard(self):
		"""
        Draws the grid-box of the game.
        :return: the box image
        """
		h, w, _ = self.img.shape
		cv2.line(self.img, (w//3, 0), (w//3, h), (0,255,0), 3)
		cv2.line(self.img, (2*w//3, 0), (2*w//3, h), (0,255,0), 3)

		cv2.line(self.img, (0, h//3), (w, h//3), (0,255,0), 3)
		cv2.line(self.img, (0, 2*h//3), (w, 2*h//3), (0,255,0), 3)
		return self.img


	def drawO(self, imgCanvas, xMin, xMax, yMin, yMax):
		"""
        Draws the "O" of the tic-tac-toe game.
        :param imgCanvas: the image on which we should draw
		:param xMin: minimum x coordinate of the box
		:param xMax: maximum x coordinate of the box
		:param yMin: minimum y coordinate of the box
		:param yMax: maximum x coordinate of the box
        """
		h, _, _ = detector.findDistance(8, 12, self.img) 
		if h < 30: # draw O
			cv2.circle(imgCanvas, ((xMin+xMax)//2, (yMin+yMax)//2),
					   25, (0,0,255))


	def drawX(self, imgCanvas, xMin, xMax, yMin, yMax):
		"""
        Draws the "X" of the tic-tac-toe game.
        :param imgCanvas: the image on which we should draw
		:param xMin: minimum x coordinate of the box
		:param xMax: maximum x coordinate of the box
		:param yMin: minimum y coordinate of the box
		:param yMax: maximum x coordinate of the box
        """
		t,_,_ =  detector.findDistance(8, 4, self.img)
		if t < 30: # draw x
			cv2.line(imgCanvas, (xMin, yMin), (xMax, yMax), (0,0,255), 5)
			cv2.line(imgCanvas, (xMax, yMin), (xMin, yMax), (0,0,255), 5)


	def detectCell(self, imgCanvas, lmList):
		"""
        Draws the "O" of the tic-tac-toe game.
        :param imgCanvas: the image on which we should draw
		:param lmList: the list of landmarks for the detected hand
        :return: the image on which X is drawn, with the 
        		 corresponding grid value on the board.
        """
		if lmList:  # to check if the hand is detected.
			for i in range(len(self.state)):
				key = self.state[i]
				xMin, xMax, yMin, yMax = key
				if xMin < lmList[8][0] <= xMax and yMin < lmList[8][1] <= yMax:
					cv2.rectangle(self.img, (xMin, yMin), (xMax, yMax),
							 (0,255,0), cv2.FILLED)
					#self.drawO(imgCanvas, xMin, xMax, yMin, yMax)
					if self.board[i] == 0:
						self.drawX(imgCanvas, xMin, xMax, yMin, yMax)
						self.board[i] = 1
					return imgCanvas, i, self.board[i]