# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 13:23:43 2024

@author: PV
"""
import cv2 
import numpy as np 
from random import choice 

def getColor(): 
    lstColor = [[255,64,64],[255,165,0],[255,244,79],[102,255,0],[172,229,238],[148,87,235],[148,87,235],[241,156,187]]
    return choice(lstColor)

def getInfo(piece): 
    if piece == "":
        coords = np.array([[0, 0]]) 
    elif piece == "I":
        coords = np.array([[0, 3], [0, 4], [0, 5], [0, 6]]) 
    elif piece == "T":
            coords = np.array([[1, 3], [1, 4], [1, 5], [0, 4]]) 
    elif piece == "L":
            coords = np.array([[1, 3], [1, 4], [1, 5], [0, 5]])
    elif piece == "J":
            coords = np.array([[1, 3], [1, 4], [1, 5], [0, 3]]) 
    elif piece == "S":
            coords = np.array([[1, 5], [1, 4], [0, 3], [0, 4]]) 
    elif piece == "Z":
            coords = np.array([[1, 3], [1, 4], [0, 4], [0, 5]]) 
    else: 
        coords = np.array([[0, 4], [0, 5], [1, 4], [1, 5]]) 
    
    return coords, getColor()

def display(board, coords, color, next_info, held_info, score, SPEED): 
    # Generates the display
    
    border = np.uint8(127 - np.zeros([20, 1, 3])) 
    border_ = np.uint8(127 - np.zeros([1, 23, 3])) 
    
    dummy = board.copy() 
    dummy[coords[:,0], coords[:,1]] = color
    
    right = np.uint8(np.zeros([20, 10, 3])) 
    right[next_info[0][:,0] + 2, next_info[0][:,1]] = next_info[1] 
    
    dummy = np.concatenate(( border, dummy, border, right, border), 1) 
    dummy = np.concatenate((border_, dummy, border_), 0) 
    dummy = dummy.repeat(20, 0).repeat(20, 1) 
    dummy = cv2.putText(dummy, str(score), (325, 150), cv2.FONT_HERSHEY_DUPLEX, 1, [0, 0, 255], 2)

# Instructions for the player 
    index_pos = 300
    x_index_pos = 300
    dummy = cv2.putText(dummy, "A - left", (x_index_pos, index_pos), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 234])
    dummy = cv2.putText(dummy, "D - right", (x_index_pos, index_pos+25), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 234])
    dummy = cv2.putText(dummy, "S - drain", (x_index_pos, index_pos+50), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 234])
    dummy = cv2.putText(dummy, "W - rotate", (x_index_pos, index_pos+75), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 234]) 
    # dummy = cv2.putText(dummy, "J - rotate left", (45, 300), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 255]) 
    # dummy = cv2.putText(dummy, "L - rotate right", (45, 325), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 255]) 
    # dummy = cv2.putText(dummy, "I - hold", (45, 350), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 255]) 
    
    cv2.imshow("Tetris", dummy) 
    key = cv2.waitKey(int(1000/SPEED)) 
    
    return key

def getNextPiece(): 
    next_piece = choice(["O", "I", "S", "Z", "L", "J", "T"])
    
    return next_piece 
SPEED = 1 # Controls the speed of the tetris pieces 

# Make a board 

board = np.uint8(np.zeros([20, 10, 3])) 

# Initialize some variables 

quit = False 
place = False 
drop = False 
switch = False 
held_piece = "" 
flag = 0 
score = 0 
next_piece ="" 
current_piece = "" 
# All the tetris pieces
if __name__ == "__main__":
    next_piece = getNextPiece()
    while not quit: 
        # Check if user wants to swap held and current pieces
        if switch:
            # swap held_piece and current_piece
            held_piece, current_piece = current_piece, held_piece 
            switch = False 
        else: 
            # Generates the next piece and updates the current piece 
            current_piece = next_piece 
            next_piece = getNextPiece() 
        if flag > 0:
            flag -= 1 
        # Determines the color and position of the current, next, and held pieces 
        
        held_info = getInfo(held_piece) 
        
        next_info = getInfo(next_piece) 
        
        coords, color = getInfo(current_piece) 
        
        if current_piece == "I": 
            top_left = [-2, 3] 
        if not np.all(board[coords[:,0], coords[:,1]] == 0): 
            break
        while True: 
            # Shows the board and gets the key press
            key = display(board, coords, color, next_info, held_info, score, SPEED) 
            # Create a copy of the position 
            dummy = coords.copy() 
            print("speed ",SPEED, "key ",key," ", ord("s")) 
            
            if key == ord("s"): 
                drop = True 
            
            elif key == ord("a"): 
                # Moves the piece left if it isn't against the left wall 
                if np.min(coords[:,1]) > 0: 
                    coords[:,1] -= 1 
                if current_piece == "I":
                    top_left[1] -= 1 
            elif key == ord("d"): 
                # Moves the piece right if it isn't against the right wall 
                if np.max(coords[:,1]) < 9: 
                    coords[:,1] += 1 
                    if current_piece == "I": 
                        top_left[1] += 1
            elif key == ord("w"): 
                    # Rotation mechanism 
                # arr is the array of nearby points which get rotated and pov is the indexes of the blocks within arr 
                
                if current_piece != "I" and current_piece != "O":
                    if coords[1,1] > 0 and coords[1,1] < 9: 
                        arr = coords[1] - 1 + np.array([[[x, y] for y in range(3)] for x in range(3)]) 
                        pov = coords - coords[1] + 1 
                        
                elif current_piece == "I": 
                    # The straight piece has a 4x4 array, so it needs seperate code 
                            
                    arr = top_left + np.array([[[x, y] for y in range(4)] for x in range(4)]) 
                    pov = np.array([np.where(np.logical_and(arr[:,:,0] == pos[0], arr[:,:,1] == pos[1])) for pos in coords]) 
                    pov = np.array([k[0] for k in np.swapaxes(pov, 1, 2)]) 
                    
                    # Rotates the array and repositions the piece to where it is now 
                    
                if current_piece != "O": 
                    if key == ord("j"): 
                        arr = np.rot90(arr, -1) 
                    else: 
                        arr = np.rot90(arr) 
                    coords = arr[pov[:,0], pov[:,1]]     
                # Hard drop set to true 
                # drop = True 
                
            elif key == ord("i"): 
                # Goes out of the loop and tells the program to switch held and current pieces 
                if flag == 0: 
                    if held_piece == "": 
                        held_piece = current_piece 
                    else: 
                        switch = True
                    flag = 2
                    break 
            
            elif key == 8 or key == 27:
                quit = True 
                break 
            
            # Checks if the piece is overlapping with other pieces or if it's outside the board, and if so, changes the position to the position before anything happened
            
            if np.max(coords[:,0]) < 20 and np.min(coords[:,0]) >= 0:
                if not (current_piece == "I" and (np.max(coords[:,1]) >= 10 or np.min(coords[:,1]) < 0)): 
                    if not np.all(board[coords[:,0], coords[:,1]] == 0): 
                        coords = dummy.copy() 
                else:
                    coords = dummy.copy() 
            else: coords = dummy.copy() 
            
            if drop:
                # Every iteration of the loop moves the piece down by 1 and if the piece is resting on the ground or another piece, then it stops and places it
                while not place: 
                    if np.max(coords[:,0]) != 19:
                        # Checks if the piece is resting on something 
                        for pos in coords: 
                            if not np.array_equal(board[pos[0] + 1, pos[1]], [0, 0, 0]): 
                                place = True 
                                break 
                    else: 
                        # If the position of the piece is at the ground level, then it places
                        place = True 
                        
                    if place: 
                        break 
                    
                    # Keeps going down and checking when the piece needs to be placed 
                    
                    coords[:,0] += 1 
                    
                    if current_piece == "I": 
                        top_left[0] += 1 
                        
                drop = False 
                
            else: 
                # Checks if the piece needs to be placed 
                if np.max(coords[:,0]) != 19: 
                    for pos in coords: 
                        if not np.array_equal(board[pos[0] + 1, pos[1]], [0, 0, 0]): 
                            place = True 
                            break 
                else: 
                    place = True
            
            if place: 
                # Places the piece where it is on the board 
                for pos in coords: 
                    board[tuple(pos)] = color 
                
                # Resets place to False 
                place = False 
                break 
            
            # Moves down by 1 
            
            coords[:,0] += 1 
            if current_piece == "I": 
                top_left[0] += 1 
                
        # Clears lines and also counts how many lines have been cleared and updates the score 
        
        lines = 0 
        
        for line in range(20): 
            if np.all([np.any(pos != 0) for pos in board[line]]):
                lines += 1
                board[1:line+1] = board[:line] 
                
        score += lines*10

