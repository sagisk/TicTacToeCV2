#!/usr/bin/env python3
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time

from GameBoard import Board
from TicTacToeGame import TicTacToe


HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

cap = cv2.VideoCapture(0)
imgCanvas = np.zeros((480,640,3), np.uint8)
detector = HandDetector(detectionCon=0.8)

def main():
    """
    Main function that calls all functions
    """
    # Setting computer's choice
    hooman=True

    comp_choice = 'O'

    # Main loop of this game
    while True:
        success, img = cap.read()
        h, w, _ = img.shape
        imgBoard = [(0, w//3, 0, h//3), (w//3, 2*w//3, 0, h // 3), (2*w//3, w, 0, h//3),
                    (0, w//3, h//3, 2*h//3), (w//3, 2*w//3, h//3, 2*h//3), (2*w//3, w, h//3, 2*h//3),
                    (0, w//3, 2*h//3, h), (w//3, 2*w//3, 2*h//3, h), (2*w//3, w, 2*h//3, h)]
        b = Board(imgBoard, img)
        lmList, _ = b.drawHands()
        img = b.drawBoard()
        t = TicTacToe(board, b)
        
        if lmList:
            t.human_turn(imgCanvas, lmList, b)
            hooman=False
            print(board)
        else:
            if hooman==False:
                t.ai_turn(imgCanvas, imgBoard, comp_choice)
                hooman=True
                print(board)
        if t.wins(HUMAN):
            print("You won")
            break
        elif t.wins(COMP):
            print("You lose")
            break

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        cv2.imshow('Image', img)
        # cv2.imshow('Canvas', imgCanvas)  # don't show unless 
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()