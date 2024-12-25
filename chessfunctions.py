import random
import re
import numpy as np
import enum
import zstandard as zstd
import time

class pieces():
    pawn = 0
    knight = 1
    bishop = 2
    rook = 3
    queen = 4
    king = 5
    notking=range(0,5)
    
class colors():
    black = 0
    white = 1
    
def changetopiece(thing):
    if thing == '00':
        return u'\u265F'
    elif thing == '01':
        return u'\u2659'
    elif thing == '10':
        return u'\u265E'
    elif thing == '11':
        return u'\u2658'
    elif thing == '20':
        return u'\u265D'
    elif thing == '21':
        return u'\u2657'
    elif thing == '30':
        return u'\u265C'
    elif thing == '31':
        return u'\u2656'
    elif thing == '40':
        return u'\u265B'
    elif thing == '41':
        return u'\u2655'
    elif thing == '50':
        return u'\u265A'
    elif thing == '51':
        return u'\u2654'
        
    else:
        return thing    
    
def startingChessboard():
    
    board = np.zeros([6,2,8,8])
    
    np.put(board[pieces.pawn, colors.black, 1, :], [0,1,2,3,4,5,6,7,], 1)
    np.put(board[pieces.pawn, colors.white, 6, :], [0,1,2,3,4,5,6,7,], 1)
    np.put(board[pieces.knight, colors.black, 0, :], [1,6], 1)
    np.put(board[pieces.knight, colors.white, 7, :], [1,6], 1)
    np.put(board[pieces.bishop, colors.black, 0, :], [2,5], 1)
    np.put(board[pieces.bishop, colors.white, 7, :], [2,5], 1)
    np.put(board[pieces.rook, colors.black, 0, :], [0,7], 1)
    np.put(board[pieces.rook, colors.white, 7, :], [0,7], 1)
    np.put(board[pieces.king, colors.black, 0, :], [4], 1)
    np.put(board[pieces.king, colors.white, 7, :], [4], 1)
    np.put(board[pieces.queen, colors.black, 0, :], [3], 1)
    np.put(board[pieces.queen, colors.white, 7, :], [3], 1)
    return board


def visualizeChessboard(board): #change to unicode later
    visualizeboard = np.zeros((8,8),dtype=object)
    for i in range(6):
        for j in range(2):
            row = np.where(board[i,j,:,:]==1)[0]
            column = np.where(board[i,j,:,:] ==1)[1]
            for k in range(len(row)):

                np.put(visualizeboard[row[k]],column[k],changetopiece(str(i)+str(j)))
                
    visualizeboard[visualizeboard == 0] = u"\u25FB"

    print(visualizeboard)
    
def changeBoardPosition(position): #changes each board position into a matrix indice for hte list
    if list(position)[-1] == '+':
        num = 8 - int(list(position)[-2])
        if list(position)[-3] == 'a':
            return num, 0

        if list(position)[-3] == 'b':
            return num, 1

        if list(position)[-3] == 'c':
            return num, 2

        if list(position)[-3] == 'd':
            return num, 3

        if list(position)[-3] == 'e':
            return num, 4

        if list(position)[-3] == 'f':
            return num, 5
        if list(position)[-3] == 'g':
            return num, 6
        if list(position)[-3] == 'h':
            return num, 7
    else:
        num = 8 - int(list(position)[-1])
        if list(position)[-2] == 'a':
            return num, 0

        if list(position)[-2] == 'b':
            return num, 1

        if list(position)[-2] == 'c':
            return num, 2

        if list(position)[-2] == 'd':
            return num, 3

        if list(position)[-2] == 'e':
            return num, 4

        if list(position)[-2] == 'f':
            return num, 5
        if list(position)[-2] == 'g':
            return num, 6
        if list(position)[-2] == 'h':
            return num, 7
        
def findOldColumn(letter):
    if letter.isalpha():
        if letter == 'a':
            return 0
        if letter == 'b':
            return 1
        if letter == 'c':
            return 2
        if letter == 'd':
            return 3
        if letter == 'e':
            return 4
        if letter == 'f':
            return 5
        if letter == 'g':
            return 6
        if letter == 'h':
            return 7
    elif letter.isdigit():
        if letter == '8':
            return 0
        if letter =='7':
            return 1
        if letter =='6':
            return 2
        if letter =='5':
            return 3
        if letter == '4':
            return 4
        if letter == '3':
            return 5
        if letter == '2':
            return 6
        if letter =='1':
            return 7
        
    raise ValueError('findOldColumn not working')

def findPiece(move):
    if list(move)[0].isupper()==False:
        return 'pawn'
    elif list(move)[0] == 'N':
        return 'knight'
    elif list(move)[0] == 'B':
        return 'bishop'
    elif list(move)[0] == 'R':
        return 'rook'
    elif list(move)[0] == 'Q':
        return 'queen'
    elif list(move)[0] == 'K':
        return 'king'
    
def checkTwoPieces(rorc, x, color,piecenum, board):
    if rorc == 'row':
        if np.count_nonzero(board[piecenum,color,x,:] == 1) >1:
            return True
        else:
            return False
    
    else:
        if np.count_nonzero(board[piecenum,color,:,x] == 1) >1:
            return True
        else: 
            return False

def findDiagonal(row,column):
    diagonal = column-row
    return diagonal
    
    
def findOldPosition(position, copyboard,row,column,piece,color): #needs to return both a previous position
    #error finder
    currentboard = copyboard.copy()
    if 'x' not in list(position):
        if np.any(currentboard[:,:, row, column]==1):
            raise ValueError('There is a piece in the place you are trying to go to', position)
        
    if 'x' in list(position) and len(position) <= 4:


        
        #checking for en passant
        if piece == 'pawn': #check if pawn
            oldColumn = findOldColumn(list(position)[0])

            if color == 'white': #check if white

                if np.any(currentboard[:, colors.black, row, column] == 1): #if white check if there is a black piece in the spot we are going into
                    #we should pass this as then we are just taking here
                    currentboard[:,:, row, column] = 0
                    currentboard[pieces.pawn, colors.white, row, column] =1
                    currentboard[pieces.pawn, colors.white, row+1, oldColumn] =0
                    return currentboard
                        
                        
                else: #in the case where there is none
                    if currentboard[pieces.pawn, colors.black,row+1,column] == 1:#check if there is a 1 behind the black pawn
                        #check where whitepawn is coming from
                        currentboard[pieces.pawn, colors.white, row, column] =1
                        currentboard[pieces.pawn, colors.white, row+1, oldColumn] =0
                        currentboard[pieces.pawn, colors.black,row+1,column] = 0
                        return currentboard

                    raise ValueError('could not find previous pawn when taking', position)
                        
            elif color == 'black':
                if np.any(currentboard[:, colors.white, row, column] == 1): #if white check if there is a black piece in the spot we are going into
                    currentboard[:,:, row, column] = 0
                    #we should pass this as then we are just taking here
                    currentboard[pieces.pawn, colors.black, row, column] =1
                    currentboard[pieces.pawn, colors.black, row-1, oldColumn] =0
                    return currentboard

                        
                        
                else: #in the case where there is none
                    if currentboard[pieces.pawn, colors.white,row-1,column] == 1:#check if there is a 1 behind the black pawn
                        #check where whitepawn is coming from
                        currentboard[pieces.pawn, colors.black, row, column] =1
                        currentboard[pieces.pawn, colors.black, row-1, oldColumn] =0
                        currentboard[pieces.pawn, colors.white ,row-1,column] = 0
                        return currentboard
                    raise ValueError('could not find previous pawn when taking', position)

                        
        currentboard[:,:, row, column] = 0
        

                #check behind to left and right
                
                #find if there is a pawn that passed it the turn before?
                
                
    #we should find a way to see if there can be 2. Easiest is checking the lengths of the string. 
    #in this there will be 5 cases
    #string length 4 with no x inside
    #string length 5 with no x inside
    #string length 5 with x inside
    #string length 6 with x inside
    #in the case of pawns we have already fixed this
    elif 'x' not in list(position) and len(position) == 4:
        if color == 'white':
            if position[1].isdigit():
                oldRow = findOldColumn(position[1])
                if piece == 'knight':
                    #check if there are multiple ones in that same row/file
                    
                    currentboard[pieces.knight,colors.white, oldRow,: ] = 0
                    currentboard[pieces.knight, colors.white, row, column] = 1
                    return currentboard
                    
                if piece == 'queen':
                    if checkTwoPieces('row',oldRow, colors.white, pieces.queen, currentboard):
                        checkColumn =  np.where(currentboard[pieces.queen, colors.white, oldRow, :] == 1)[0]
                        for piece in checkColumn:
                            if abs(piece - column) == abs(oldRow-row) or piece == column:

                
                                currentboard[pieces.queen, colors.white, oldRow, piece] = 0
                                currentboard[pieces.queen,colors.white, row, column] = 1
                                return currentboard

                    
                    currentboard[pieces.queen,colors.white, oldRow,: ] = 0
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    return currentboard
                if piece == 'bishop':
                    currentboard[pieces.bishop,colors.white, oldRow,: ] = 0
                    currentboard[pieces.bishop, colors.white, row, column] = 1
                    return currentboard
                if piece == 'rook':
                    currentboard[pieces.rook,colors.white, oldRow,: ] = 0
                    currentboard[pieces.rook, colors.white, row, column] = 1
                    return currentboard
            elif position[1].isalpha():
                oldColumn = findOldColumn(position[1])
        
                if piece == 'knight':
                    currentboard[pieces.knight,colors.white, :,oldColumn ] = 0
                    currentboard[pieces.knight, colors.white, row, column] = 1
                    return currentboard
                if piece == 'queen':

                    if checkTwoPieces('column',oldColumn, colors.white, pieces.queen, currentboard):
                        checkColumn =  np.where(currentboard[pieces.queen, colors.white, :, oldColumn] == 1)[0]
                        for piece in checkColumn:
                            if abs(oldColumn - column) == abs(piece-row) or piece == row:

                
                                currentboard[pieces.queen, colors.white, piece, oldColumn] = 0
                                currentboard[pieces.queen,colors.white, row, column] = 1
                                return currentboard


                            
                        
                    currentboard[pieces.queen,colors.white, :,oldColumn ] = 0
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    return currentboard
                if piece == 'rook':
                    currentboard[pieces.rook,colors.white, :,oldColumn ] = 0
                    currentboard[pieces.rook, colors.white, row, column] = 1
                    return currentboard
                if piece == 'bishop':
                    currentboard[pieces.bishop,colors.white, :,oldColumn ] = 0
                    currentboard[pieces.bishop, colors.white, row, column] = 1
                    return currentboard
            
        if color == 'black':
            if position[1].isdigit():
                oldRow = findOldColumn(position[1])
                if piece == 'knight':
                    currentboard[pieces.knight,colors.black, oldRow,: ] = 0
                    currentboard[pieces.knight, colors.black, row, column] = 1
                    return currentboard
                    
                if piece == 'queen':
                    if checkTwoPieces('row',oldRow, colors.black, pieces.queen, currentboard):
                        checkColumn =  np.where(currentboard[pieces.queen, colors.black, oldRow, :] == 1)[0]
                        for piece in checkColumn:
                            if abs(piece - column) == abs(oldRow-row) or piece == column:

                
                                currentboard[pieces.queen, colors.black, oldRow, piece] = 0
                                currentboard[pieces.queen,colors.black, row, column] = 1
                                return currentboard
                    currentboard[pieces.queen,colors.black, oldRow,: ] = 0
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    return currentboard
                    
                if piece == 'bishop':
                    currentboard[pieces.bishop,colors.black, oldRow,: ] = 0
                    currentboard[pieces.bishop, colors.black, row, column] = 1
                    return currentboard
                if piece == 'rook':
                    currentboard[pieces.rook,colors.black, oldRow,: ] = 0
                    currentboard[pieces.rook, colors.black, row, column] = 1
                    return currentboard
            elif position[1].isalpha():
                oldColumn = findOldColumn(position[1])
        
                if piece == 'knight':
                    currentboard[pieces.knight,colors.black, :,oldColumn ] = 0
                    currentboard[pieces.knight, colors.black, row, column] = 1
                    return currentboard
                if piece == 'queen':
                    if checkTwoPieces('column',oldColumn, colors.black, pieces.queen, currentboard):
                        checkColumn =  np.where(currentboard[pieces.queen, colors.black, :, oldColumn] == 1)[0]
                        for piece in checkColumn:
                            if abs(oldColumn - column) == abs(piece-row) or piece == row:

                
                                currentboard[pieces.queen, colors.black, piece, oldColumn] = 0
                                currentboard[pieces.queen,colors.black, row, column] = 1
                                return currentboard
                    currentboard[pieces.queen,colors.black, :,oldColumn ] = 0
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    return currentboard
                if piece == 'rook':
                    currentboard[pieces.rook,colors.black, :,oldColumn ] = 0
                    currentboard[pieces.rook, colors.black, row, column] = 1
                    return currentboard
                if piece == 'bishop':
                    currentboard[pieces.bishop,colors.black, :,oldColumn ] = 0
                    currentboard[pieces.bishop, colors.black, row, column] = 1
                    return currentboard
        raise ValueError('x not in position nad position length 4', position)
    elif 'x' not in list(position) and len(position) == 5:
        if color == 'white':
            oldRow, oldColumn = changeBoardPosition(position[1:3])
            if piece == 'queen':
                currentboard[pieces.queen, colors.white, row, column] = 1
                currentboard[pieces.queen, colors.white, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'rook':
                currentboard[pieces.rook, colors.white, row, column] = 1
                currentboard[pieces.rook, colors.white, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'knight':
                currentboard[pieces.knight, colors.white, row, column] = 1
                currentboard[pieces.knight, colors.white, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'bishop':
                currentboard[pieces.bishop, colors.white, row, column] = 1
                currentboard[pieces.bishop, colors.white, oldRow, oldColumn] = 0
                return currentboard
        if color == 'black':
            oldRow, oldColumn = changeBoardPosition(position[1:3])
            if piece == 'queen':
                currentboard[pieces.queen, colors.black, row, column] = 1
                currentboard[pieces.queen, colors.black, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'rook':
                currentboard[pieces.rook, colors.black, row, column] = 1
                currentboard[pieces.rook, colors.black, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'knight':
                currentboard[pieces.knight, colors.black, row, column] = 1
                currentboard[pieces.knight, colors.black, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'bishop':
                currentboard[pieces.bishop, colors.black, row, column] = 1
                currentboard[pieces.bishop, colors.black, oldRow, oldColumn] = 0
                return currentboard
        raise ValueError('x not in position nad position length 5', position)
            
    elif 'x' in list(position) and len(position) == 5:
        currentboard[:,:, row, column] = 0
        if color == 'white':
            if position[1].isdigit():
                oldRow = findOldColumn(position[1])
                if piece == 'knight':
                    currentboard[pieces.knight,colors.white, oldRow,: ] = 0
                    currentboard[pieces.knight, colors.white, row, column] = 1
                    return currentboard
                    
                if piece == 'queen':
                    currentboard[pieces.queen,colors.white, oldRow,: ] = 0
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    return currentboard
                if piece == 'bishop':
                    currentboard[pieces.bishop,colors.white, oldRow,: ] = 0
                    currentboard[pieces.bishop, colors.white, row, column] = 1
                    return currentboard
                if piece == 'rook':
                    currentboard[pieces.rook,colors.white, oldRow,: ] = 0
                    currentboard[pieces.rook, colors.white, row, column] = 1
                    return currentboard
            elif position[1].isalpha():
                oldColumn = findOldColumn(position[1])
        
                if piece == 'knight':
                    currentboard[pieces.knight,colors.white, :,oldColumn ] = 0
                    currentboard[pieces.knight, colors.white, row, column] = 1
                    return currentboard
                if piece == 'queen':
                    currentboard[pieces.queen,colors.white, :,oldColumn ] = 0
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    return currentboard
                if piece == 'rook':
                    currentboard[pieces.rook,colors.white, :,oldColumn ] = 0
                    currentboard[pieces.rook, colors.white, row, column] = 1
                    return currentboard
                if piece == 'bishop':
                    currentboard[pieces.bishop,colors.white, :,oldColumn ] = 0
                    currentboard[pieces.bishop, colors.white, row, column] = 1
                    return currentboard
            
        if color == 'black':
            if position[1].isdigit():
                oldRow = findOldColumn(position[1])
                if piece == 'knight':
                    currentboard[pieces.knight,colors.black, oldRow,: ] = 0
                    currentboard[pieces.knight, colors.black, row, column] = 1
                    return currentboard
                    
                if piece == 'queen':
                    currentboard[pieces.queen,colors.black, oldRow,: ] = 0
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    return currentboard
                    
                if piece == 'bishop':
                    currentboard[pieces.bishop,colors.black, oldRow,: ] = 0
                    currentboard[pieces.bishop, colors.black, row, column] = 1
                    return currentboard
                if piece == 'rook':
                    currentboard[pieces.rook,colors.black, oldRow,: ] = 0
                    currentboard[pieces.rook, colors.black, row, column] = 1
                    return currentboard
            elif position[1].isalpha():
                oldColumn = findOldColumn(position[1])
        
                if piece == 'knight':
                    currentboard[pieces.knight,colors.black, :,oldColumn ] = 0
                    currentboard[pieces.knight, colors.black, row, column] = 1
                    return currentboard
                if piece == 'queen':
                    currentboard[pieces.queen,colors.black, :,oldColumn ] = 0
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    return currentboard
                if piece == 'rook':
                    currentboard[pieces.rook,colors.black, :,oldColumn ] = 0
                    currentboard[pieces.rook, colors.black, row, column] = 1
                    return currentboard
                if piece == 'bishop':
                    currentboard[pieces.bishop,colors.black, :,oldColumn ] = 0
                    currentboard[pieces.bishop, colors.black, row, column] = 1
                    return currentboard
        raise ValueError('x in position nad position length 5', position)
    elif 'x' in list(position) and len(position) == 6:
        currentboard[:,:, row, column] = 0
        if color == 'white':
            oldRow, oldColumn = changeBoardPosition(position[1:3])
            if piece == 'queen':
                currentboard[pieces.queen, colors.white, row, column] = 1
                currentboard[pieces.queen, colors.white, oldRow, oldRolumn] = 0
                return currentboard
            if piece == 'rook':
                currentboard[pieces.rook, colors.white, row, column] = 1
                currentboard[pieces.rook, colors.white, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'knight':
                currentboard[pieces.knight, colors.white, row, column] = 1
                currentboard[pieces.knight, colors.white, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'bishop':
                currentboard[pieces.bishop, colors.white, row, column] = 1
                currentboard[pieces.bishop, colors.white, oldRow, oldColumn] = 0
                return currentboard
        if color == 'black':
            oldRow, oldColumn = changeBoardPosition(position[1:3])
            if piece == 'queen':
                currentboard[pieces.queen, colors.black, row, column] = 1
                currentboard[pieces.queen, colors.black, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'rook':
                currentboard[pieces.rook, colors.black, row, column] = 1
                currentboard[pieces.rook, colors.black, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'knight':
                currentboard[pieces.knight, colors.black, row, column] = 1
                currentboard[pieces.knight, colors.black, oldRow, oldColumn] = 0
                return currentboard
            if piece == 'bishop':
                currentboard[pieces.bishop, colors.black, row, column] = 1
                currentboard[pieces.bishop, colors.black, oldRow, oldColumn] = 0
                return currentboard
        raise ValueError('x in position nad position length 6', position)
            
    if color == 'black':
        if piece == 'pawn':


            #check 1 behind it
            if currentboard[pieces.pawn, colors.black, row-1, column] == 1:
                currentboard[pieces.pawn, colors.black, row, column] = 1
                currentboard[pieces.pawn, colors.black, row-1, column] = 0
                return currentboard
            #check 2 behind it
            elif currentboard[pieces.pawn, colors.black, row-2, column] == 1:
                currentboard[pieces.pawn, colors.black, row, column] = 1
                currentboard[pieces.pawn, colors.black, row-2, column] = 0
                return currentboard
            else:
                 raise ValueError('Could not find previous pawn position', position)

        elif piece == 'knight':



            #check the 8 possible spots it could have came from and if there are multiple spots it could have been in
            if column < 6 and row != 7:
                 if currentboard[pieces.knight, colors.black, row+1, column+2] == 1:

                    currentboard[pieces.knight, colors.black, row, column] = 1
                    currentboard[pieces.knight, colors.black, row+1, column+2] = 0
                    return currentboard

            if column != 7 and row < 6:
                if currentboard[pieces.knight, colors.black, row+2, column+1] == 1:
                    currentboard[pieces.knight, colors.black, row, column] = 1
                    currentboard[pieces.knight, colors.black, row+2, column+1] = 0
                    return currentboard

            if column < 6 and row > 0:
                if currentboard[pieces.knight, colors.black, row-1, column+2] == 1:
                    currentboard[pieces.knight, colors.black, row, column] = 1
                    currentboard[pieces.knight, colors.black, row-1, column+2] = 0
                    return currentboard
            if column <7 and row >1:
                if currentboard[pieces.knight, colors.black, row-2, column+1] == 1:
                    currentboard[pieces.knight, colors.black, row, column] = 1
                    currentboard[pieces.knight, colors.black, row-2, column+1] = 0
                    return currentboard

            if column >1 and row <7 :
                if currentboard[pieces.knight, colors.black, row+1, column-2] == 1:
                    currentboard[pieces.knight, colors.black, row, column] = 1
                    currentboard[pieces.knight, colors.black, row+1, column-2] = 0
                    return currentboard

            if row < 6 and column > 0:

                if currentboard[pieces.knight, colors.black, row+2, column-1] == 1:

                    currentboard[pieces.knight, colors.black, row, column] = 1
                    currentboard[pieces.knight, colors.black, row+2, column-1] = 0
                    return currentboard

            if row > 0 and column >1:
                if currentboard[pieces.knight, colors.black, row-1, column-2] == 1:
                    currentboard[pieces.knight, colors.black, row, column] = 1
                    currentboard[pieces.knight, colors.black, row-1, column-2] = 0
                    return currentboard
            
            if row > 1 and column > 0:
                if currentboard[pieces.knight, colors.black, row-2, column-1] == 1:
                    currentboard[pieces.knight, colors.black, row, column] = 1
                    currentboard[pieces.knight, colors.black, row-2, column-1] = 0
                    return currentboard
                raise ValueError('could not find knight', position)
        elif piece == 'bishop':
            findcolumn = column
            findrow = row
            #go up right
            while findcolumn != 7 and findrow != 0:
                findcolumn +=1
                findrow -=1

                if currentboard[pieces.bishop, colors.black, findrow, findcolumn] == 1:
                    currentboard[pieces.bishop, colors.black, row, column] = 1
                    currentboard[pieces.bishop, colors.black, findrow, findcolumn] = 0
                    return currentboard

            #go down right
            findcolumn = column
            findrow = row
            while findcolumn != 7 and findrow != 7:
                findcolumn +=1
                findrow +=1

                if currentboard[pieces.bishop, colors.black, findrow, findcolumn] == 1:
                    currentboard[pieces.bishop, colors.black, row, column] = 1
                    currentboard[pieces.bishop, colors.black, findrow, findcolumn] = 0
                    return currentboard

            #go up left
            findcolumn = column
            findrow = row
            while findcolumn !=0 and findrow != 0:
                findcolumn -=1
                findrow -=1

                if currentboard[pieces.bishop, colors.black, findrow, findcolumn] == 1:
                    currentboard[pieces.bishop, colors.black, row, column] = 1
                    currentboard[pieces.bishop, colors.black, findrow, findcolumn] = 0
                    return currentboard
            #go down left
            findcolumn = column
            findrow = row
            while findcolumn !=0 and findrow != 7:
                findcolumn -=1
                findrow +=1

                if currentboard[pieces.bishop, colors.black, findrow, findcolumn] == 1:
                    currentboard[pieces.bishop, colors.black, row, column] = 1
                    currentboard[pieces.bishop, colors.black, findrow, findcolumn] = 0
                    return currentboard
            raise ValueError('could not find bishop', position)
        elif piece == 'rook':
            findcolumn = column
            while findcolumn !=7:
                findcolumn +=1

                if currentboard[pieces.rook, colors.black, row, findcolumn] == 1:
                    currentboard[pieces.rook, colors.black, row, column] = 1
                    currentboard[pieces.rook, colors.black, row, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, row ,findcolumn] == 1):
                    break
            findcolumn = column
            while findcolumn != 0:
                findcolumn -=1

                if currentboard[pieces.rook, colors.black, row, findcolumn] == 1:
                    currentboard[pieces.rook, colors.black, row, column] = 1
                    currentboard[pieces.rook, colors.black, row, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, row ,findcolumn] == 1):
                    break

            findrow = row
            while findrow != 7:
                findrow +=1

                if currentboard[pieces.rook, colors.black, findrow, column] == 1:
                    currentboard[pieces.rook, colors.black, row, column] = 1
                    currentboard[pieces.rook, colors.black, findrow, column] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,column] == 1):
                    break

            findrow = row
            while findrow != 0:
                findrow -=1

                if currentboard[pieces.rook, colors.black, findrow, column] == 1:
                    currentboard[pieces.rook, colors.black, row, column] = 1
                    currentboard[pieces.rook, colors.black, findrow, column] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,column] == 1):
                    break
            raise ValueError('could not find rook', position)

        elif piece == 'queen':
            findcolumn = column
            findrow = row
            #go up right
            while findcolumn != 7 and findrow != 0:
                findcolumn +=1
                findrow -=1

                if currentboard[pieces.queen, colors.black, findrow, findcolumn] == 1:
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    currentboard[pieces.queen, colors.black, findrow, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,findcolumn] == 1):
                    break

            #go down right
            findcolumn = column
            findrow = row
            while findcolumn != 7 and findrow != 7:
                findcolumn +=1
                findrow +=1

                if currentboard[pieces.queen, colors.black, findrow, findcolumn] == 1:
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    currentboard[pieces.queen, colors.black, findrow, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,findcolumn] == 1):
                    break

            #go up left
            findcolumn = column
            findrow = row
            while findcolumn !=0 and findrow != 0:
                findcolumn -=1
                findrow -=1

                if currentboard[pieces.queen, colors.black, findrow, findcolumn] == 1:
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    currentboard[pieces.queen, colors.black, findrow, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,findcolumn] == 1):
                    break
            #go down left
            findcolumn = column
            findrow = row
            while findcolumn !=0 and findrow != 7:
                findcolumn -=1
                findrow +=1

                if currentboard[pieces.queen, colors.black, findrow, findcolumn] == 1:
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    currentboard[pieces.queen, colors.black, findrow, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,findcolumn] == 1):
                    break

            findcolumn = column
            while findcolumn !=7:
                findcolumn +=1

                if currentboard[pieces.queen, colors.black, row, findcolumn] == 1:
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    currentboard[pieces.queen, colors.black, row, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, row ,findcolumn] == 1):
                    break
            findcolumn = column
            while findcolumn != 0:
                findcolumn -=1

                if currentboard[pieces.queen, colors.black, row, findcolumn] == 1:
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    currentboard[pieces.queen, colors.black, row, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, row ,findcolumn] == 1):
                    break

            findrow = row
            while findrow != 7:
                findrow +=1

                if currentboard[pieces.queen, colors.black, findrow, column] == 1:
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    currentboard[pieces.queen, colors.black, findrow, column] = 0
                    return currentboard
                
                if np.any(currentboard[:, :, findrow ,column] == 1):
                    break

            findrow = row
            while findrow != 0:
                findrow -=1

                if currentboard[pieces.queen, colors.black, findrow, column] == 1:
                    currentboard[pieces.queen, colors.black, row, column] = 1
                    currentboard[pieces.queen, colors.black, findrow, column] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,column] == 1):
                    break
            raise ValueError('could not find queen', position)

        if piece == 'king':
            #check the 8 different positions
            if column != 7:
                if currentboard[pieces.king, colors.black, row, column+1] == 1: #right 
                    currentboard[pieces.king, colors.black, row, column] = 1
                    currentboard[pieces.king, colors.black, row, column+1] = 0
                    return currentboard
            if row != 7:
                if currentboard[pieces.king, colors.black, row+1, column] == 1: #down
                    currentboard[pieces.king, colors.black, row, column] = 1
                    currentboard[pieces.king, colors.black, row+1, column] = 0
                    return currentboard
            if row !=7 and column!=7:
                if currentboard[pieces.king, colors.black, row+1, column+1] == 1:#down/right
                    currentboard[pieces.king, colors.black, row, column] = 1
                    currentboard[pieces.king, colors.black, row+1, column+1] = 0
                    return currentboard
            if row !=0:
                if currentboard[pieces.king, colors.black, row-1, column] == 1:#up
                    currentboard[pieces.king, colors.black, row, column] = 1
                    currentboard[pieces.king, colors.black, row-1, column] = 0
                    return currentboard
            if row!=0 and column !=7:
                if currentboard[pieces.king, colors.black, row-1, column+1] == 1:#upright
                    currentboard[pieces.king, colors.black, row, column] = 1
                    currentboard[pieces.king, colors.black, row-1, column+1] = 0
                    return currentboard
            if column != 0:
                if currentboard[pieces.king, colors.black, row, column-1] == 1: #left
                    currentboard[pieces.king, colors.black, row, column] = 1
                    currentboard[pieces.king, colors.black, row, column-1] = 0
                    return currentboard
                if row !=7:
                    if currentboard[pieces.king, colors.black, row+1, column-1] == 1: #leftdown
                        currentboard[pieces.king, colors.black, row, column] = 1
                        currentboard[pieces.king, colors.black, row+1, column-1] = 0
                        return currentboard
                if row !=0:
                    if currentboard[pieces.king, colors.black, row-1, column-1] == 1:#leftup
                        currentboard[pieces.king, colors.black, row, column] = 1
                        currentboard[pieces.king, colors.black, row-1, column-1] = 0
                        return currentboard
            raise ValueError('could not find king', position)

    if color == 'white':
        if piece == 'pawn':

            #check 1 behind it
            if currentboard[pieces.pawn, colors.white, row+1, column] == 1:
                currentboard[pieces.pawn, colors.white, row, column] = 1
                currentboard[pieces.pawn, colors.white, row+1, column] = 0
                return currentboard
            #check 2 behind it
            elif currentboard[pieces.pawn, colors.white, row+2, column] == 1:
                currentboard[pieces.pawn, colors.white, row, column] = 1
                currentboard[pieces.pawn, colors.white, row+2, column] = 0
                return currentboard
            else:
                 raise ValueError('Could not find previous pawn position', position)

        elif piece == 'knight':
            #check the 8 possible spots it could have came from and if there are multiple spots it could have been in

                #check 8 possible spots
            if column < 6 and row != 7:
                 if currentboard[pieces.knight, colors.white, row+1, column+2] == 1:

                    currentboard[pieces.knight, colors.white, row, column] = 1
                    currentboard[pieces.knight, colors.white, row+1, column+2] = 0
                    return currentboard

            if column != 7 and row < 6:
                if currentboard[pieces.knight, colors.white, row+2, column+1] == 1:
                    currentboard[pieces.knight, colors.white, row, column] = 1
                    currentboard[pieces.knight, colors.white, row+2, column+1] = 0
                    return currentboard

            if column < 6 and row > 0:
                if currentboard[pieces.knight, colors.white, row-1, column+2] == 1:
                    currentboard[pieces.knight, colors.white, row, column] = 1
                    currentboard[pieces.knight, colors.white, row-1, column+2] = 0
                    return currentboard
            if column <7 and row >1:
                if currentboard[pieces.knight, colors.white, row-2, column+1] == 1:
                    currentboard[pieces.knight, colors.white, row, column] = 1
                    currentboard[pieces.knight, colors.white, row-2, column+1] = 0
                    return currentboard

            if column >1 and row <7 :
                if currentboard[pieces.knight, colors.white, row+1, column-2] == 1:
                    currentboard[pieces.knight, colors.white, row, column] = 1
                    currentboard[pieces.knight, colors.white, row+1, column-2] = 0
                    return currentboard

            if row < 6 and column > 0:
                if currentboard[pieces.knight, colors.white, row+2, column-1] == 1:

                    currentboard[pieces.knight, colors.white, row, column] = 1
                    currentboard[pieces.knight, colors.white, row+2, column-1] = 0
                    return currentboard

            if row > 0 and column >1:
                if currentboard[pieces.knight, colors.white, row-1, column-2] == 1:
                    currentboard[pieces.knight, colors.white, row, column] = 1
                    currentboard[pieces.knight, colors.white, row-1, column-2] = 0
                    return currentboard
            
            if row > 1 and column > 0:
                if currentboard[pieces.knight, colors.white, row-2, column-1] == 1:
                    currentboard[pieces.knight, colors.white, row, column] = 1
                    currentboard[pieces.knight, colors.white, row-2, column-1] = 0
                    return currentboard
            raise ValueError('could not find knight',position)
        elif piece == 'bishop':
            findcolumn = column
            findrow = row
            #go up right
            while findcolumn != 7 and findrow != 0:
                findcolumn +=1
                findrow -=1

                if currentboard[pieces.bishop, colors.white, findrow, findcolumn] == 1:
                    currentboard[pieces.bishop, colors.white, row, column] = 1
                    currentboard[pieces.bishop, colors.white, findrow, findcolumn] = 0
                    return currentboard

            #go down right
            findcolumn = column
            findrow = row
            while findcolumn != 7 and findrow != 7:
                findcolumn +=1
                findrow +=1

                if currentboard[pieces.bishop, colors.white, findrow, findcolumn] == 1:
                    currentboard[pieces.bishop, colors.white, row, column] = 1
                    currentboard[pieces.bishop, colors.white, findrow, findcolumn] = 0
                    return currentboard

            #go up left
            findcolumn = column
            findrow = row
            while findcolumn !=0 and findrow != 0:
                findcolumn -=1
                findrow -=1

                if currentboard[pieces.bishop, colors.white, findrow, findcolumn] == 1:
                    currentboard[pieces.bishop, colors.white, row, column] = 1
                    currentboard[pieces.bishop, colors.white, findrow, findcolumn] = 0
                    return currentboard
            #go down left
            findcolumn = column
            findrow = row
            while findcolumn !=0 and findrow != 7:
                findcolumn -=1
                findrow +=1

                if currentboard[pieces.bishop, colors.white, findrow, findcolumn] == 1:
                    currentboard[pieces.bishop, colors.white, row, column] = 1
                    currentboard[pieces.bishop, colors.white, findrow, findcolumn] = 0
                    return currentboard
            raise ValueError('could not find bishop', position)
        elif piece == 'rook':
            findcolumn = column
            while findcolumn !=7:
                findcolumn +=1
                

                if currentboard[pieces.rook, colors.white, row, findcolumn] == 1:
                    currentboard[pieces.rook, colors.white, row, column] = 1
                    currentboard[pieces.rook, colors.white, row, findcolumn] = 0
                    return currentboard
                
                if np.any(currentboard[:, :, row ,findcolumn] == 1):
                    # visualizeChessboard(currentboard)
                    # print(currentboard[:,:,row, findcolumn])
                    break
            findcolumn = column
            while findcolumn != 0:
                findcolumn -=1

                if currentboard[pieces.rook, colors.white, row, findcolumn] == 1:
                    currentboard[pieces.rook, colors.white, row, column] = 1
                    currentboard[pieces.rook, colors.white, row, findcolumn] = 0
                    return currentboard
                
                if np.any(currentboard[:, :, row ,findcolumn] == 1):
                    break

            findrow = row
            while findrow != 7:
                findrow +=1

                if currentboard[pieces.rook, colors.white, findrow, column] == 1:
                    currentboard[pieces.rook, colors.white, row, column] = 1
                    currentboard[pieces.rook, colors.white, findrow, column] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,column] == 1):
                    break

            findrow = row
            while findrow != 0:
                findrow -=1

                if currentboard[pieces.rook, colors.white, findrow, column] == 1:
                    currentboard[pieces.rook, colors.white, row, column] = 1
                    currentboard[pieces.rook, colors.white, findrow, column] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,column]) == 1:
                   
                    break
            raise ValueError('could not find rook', position)
        elif piece == 'queen':
            findcolumn = column
            findrow = row
            #go up right
            while findcolumn != 7 and findrow != 0:
                findcolumn +=1
                findrow -=1

                if currentboard[pieces.queen, colors.white, findrow, findcolumn] == 1:
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    currentboard[pieces.queen, colors.white, findrow, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,findcolumn] == 1):
                    break

            #go down right
            findcolumn = column
            findrow = row
            while findcolumn != 7 and findrow != 7:
                findcolumn +=1
                findrow +=1

                if currentboard[pieces.queen, colors.white, findrow, findcolumn] == 1:
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    currentboard[pieces.queen, colors.white, findrow, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,findcolumn] == 1):
                    break

            #go up left
            findcolumn = column
            findrow = row
            while findcolumn !=0 and findrow != 0:
                findcolumn -=1
                findrow -=1

                if currentboard[pieces.queen, colors.white, findrow, findcolumn] == 1:
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    currentboard[pieces.queen, colors.white, findrow, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,findcolumn] == 1):
                    break
            #go down left
            findcolumn = column
            findrow = row
            while findcolumn !=0 and findrow != 7:
                findcolumn -=1
                findrow +=1

                if currentboard[pieces.queen, colors.white, findrow, findcolumn] == 1:
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    currentboard[pieces.queen, colors.white, findrow, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,findcolumn] == 1):
                    break

            findcolumn = column
            while findcolumn !=7:
                findcolumn +=1

                if currentboard[pieces.queen, colors.white, row, findcolumn] == 1:
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    currentboard[pieces.queen, colors.white, row, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, row ,findcolumn] == 1):
                    break
            findcolumn = column
            while findcolumn != 0:
                findcolumn -=1

                if currentboard[pieces.queen, colors.white, row, findcolumn] == 1:
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    currentboard[pieces.queen, colors.white, row, findcolumn] = 0
                    return currentboard
                if np.any(currentboard[:, :, row ,findcolumn] == 1):
                    break

            findrow = row
            while findrow != 7:
                findrow +=1

                if currentboard[pieces.queen, colors.white, findrow, column] == 1:
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    currentboard[pieces.queen, colors.white, findrow, column] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,column] == 1):
                    break

            findrow = row
            while findrow != 0:
                findrow -=1

                if currentboard[pieces.queen, colors.white, findrow, column] == 1:
                    currentboard[pieces.queen, colors.white, row, column] = 1
                    currentboard[pieces.queen, colors.white, findrow, column] = 0
                    return currentboard
                if np.any(currentboard[:, :, findrow ,column] == 1):
                    break
            raise ValueError('could not find queen', position)
        if piece == 'king':

            #check the 8 different positions
            if column != 7:

                if currentboard[pieces.king, colors.white, row, column+1] == 1: #right 

                        currentboard[pieces.king, colors.white, row, column] = 1
                        currentboard[pieces.king, colors.white, row, column+1] = 0
                        return currentboard
            if row != 7:

                    
                if currentboard[pieces.king, colors.white, row+1, column] == 1: #down
                    currentboard[pieces.king, colors.white, row, column] = 1
                    currentboard[pieces.king, colors.white, row+1, column] = 0
                    return currentboard
            if row!=7 and column !=7:
                if currentboard[pieces.king, colors.white, row+1, column+1] == 1:#down/right
                    currentboard[pieces.king, colors.white, row, column] = 1
                    currentboard[pieces.king, colors.white, row+1, column+1] = 0
                    return currentboard
            if row !=0:
                if currentboard[pieces.king, colors.white, row-1, column] == 1:#up
                    currentboard[pieces.king, colors.white, row, column] = 1
                    currentboard[pieces.king, colors.white, row-1, column] = 0
                    return currentboard
            if row !=0 and column !=7:
                if currentboard[pieces.king, colors.white, row-1, column+1] == 1:#upright
                    currentboard[pieces.king, colors.white, row, column] = 1
                    currentboard[pieces.king, colors.white, row-1, column+1] = 0
                    return currentboard
            if column != 0:
                if currentboard[pieces.king, colors.white, row, column-1] == 1: #left
                        currentboard[pieces.king, colors.white, row, column] = 1
                        currentboard[pieces.king, colors.white, row, column-1] = 0
                        return currentboard
                if row !=7:
                    

                    if currentboard[pieces.king, colors.white, row+1, column-1] == 1: #leftdown
                        currentboard[pieces.king, colors.white, row, column] = 1
                        currentboard[pieces.king, colors.white, row+1, column-1] = 0
                        return currentboard

                if row !=0:
                    if currentboard[pieces.king, colors.white, row-1, column-1] == 1:#leftup
                        currentboard[pieces.king, colors.white, row, column] = 1
                        currentboard[pieces.king, colors.white, row-1, column-1] = 0
                        return currentboard
            raise ValueError('King not found', position)

    else:
        raise ValueError('no color found')
        
def promotePiece(position, color, oldBoard):


    newBoard = oldBoard.copy()
    if 'x' in list(position):
        row, column = changeBoardPosition(list(position)[2:4])
        oldColumn = findOldColumn(list(position)[0])
        
        newBoard[:,:,row, column] = 0
        piece = findPiece(list(position)[-1])
        
        #first we must find where the pawn came from
        if piece =='queen':
            if color == 'white':
                newBoard[pieces.pawn, colors.white, row+1, oldColumn] = 0
                newBoard[pieces.queen, colors.white, row, column] = 1
                return newBoard
            if color == 'black':


                newBoard[pieces.pawn, colors.black, row-1, oldColumn] = 0
                newBoard[pieces.queen, colors.black, row, column] = 1

                return newBoard
        elif piece =='knight':
            if color == 'white':
                newBoard[pieces.pawn, colors.white, row+1, oldColumn] = 0
                newBoard[pieces.knight, colors.white, row, column] = 1
                return newBoard
            if color == 'black':
                newBoard[pieces.pawn, colors.black, row-1, oldColumn] = 0
                newBoard[pieces.knight, colors.black, row, column] = 1
                return newBoard
        elif piece =='bishop':
            if color == 'white':
                newBoard[pieces.pawn, colors.white, row+1, oldColumn] = 0
                newBoard[pieces.bishop, colors.white, row, column] = 1
                return newBoard
            if color == 'black':
                newBoard[pieces.pawn, colors.black, row-1, oldColumn] = 0
                newBoard[pieces.bishop, colors.black, row, column] = 1
                return newBoard
        elif piece =='rook':
            if color == 'white':
                newBoard[pieces.pawn, colors.white, row+1, oldColumn] = 0
                newBoard[pieces.rook, colors.white, row, column] = 1
                return newBoard
            if color == 'black':
                newBoard[pieces.pawn, colors.black, row-1, oldColumn] = 0
                newBoard[pieces.rook, colors.black, row, column] = 1
                return newBoard
        
    else:
        row, column = changeBoardPosition(list(position)[0:2])
        piece = findPiece(list(position)[-1])
        if piece == 'queen':
            if color == 'white':
                newBoard[pieces.queen, colors.white, row, column] = 1
                newBoard[pieces.pawn, colors.white, row+1, column] = 0
                return newBoard
            elif color == 'black':
                newBoard[pieces.queen, colors.black, row, column] = 1
                newBoard[pieces.pawn, colors.black, row-1, column] = 0
                return newBoard
            
        elif piece == 'rook':
            if color == 'white':
                newBoard[pieces.rook, colors.white, row, column] = 1
                newBoard[pieces.pawn, colors.white, row+1, column] = 0
                return newBoard
            elif color == 'black':
                newBoard[pieces.rook, colors.black, row, column] = 1
                newBoard[pieces.pawn, colors.black, row-1, column] = 0
                return newBoard
            
        elif piece == 'knight':
            if color == 'white':
                newBoard[pieces.knight, colors.white, row, column] = 1
                newBoard[pieces.pawn, colors.white, row+1, column] = 0
                return newBoard
            elif color == 'black':
                newBoard[pieces.knight, colors.black, row, column] = 1
                newBoard[pieces.pawn, colors.black, row-1, column] = 0
                return newBoard
            
        elif piece == 'bishop':
            if color == 'white':
                newBoard[pieces.bishop, colors.white, row, column] = 1
                newBoard[pieces.pawn, colors.white, row+1, column] = 0
                return newBoard
            elif color == 'black':
                newBoard[pieces.bishop, colors.black, row, column] = 1
                newBoard[pieces.pawn, colors.black, row-1, column] = 0
                return newBoard
            
class ChessGame: #this should be a list that contains a bunch of chess boards.
    def __init__(self, startingBoard):
        self.game = [startingBoard]
        self.winner = None
        self.pieces = 32
        
    def addBoard(self,move,color):
        row, column = changeBoardPosition(move)
        piece = findPiece(move)
        test = findOldPosition(move,self.game[-1],row, column,piece, color)
        # visualizeChessboard(test)
        self.game.append(test)
        
    def promote(self, move, color):

        test = promotePiece(move, color, self.game[-1])
        self.game.append(test)
        
            
    
    def castle(self, move, color):
        if color == 'white':
            if move == 'O-O':
                #first check if theres things between white king and kingside rook
                if np.all(self.game[-1][:,:,7,5] == 0) and np.all(self.game[-1][:, :, 7,6] ==0):
                    newboard = self.game[-1].copy()
                    newboard[pieces.king, colors.white, 7,6] = 1
                    newboard[pieces.king, colors.white, 7,4] = 0
                    
                    newboard[pieces.rook, colors.white, 7,5] = 1
                    newboard[pieces.rook, colors.white, 7,7] = 0
                    self.game.append(newboard)
            elif move == 'O-O-O':
                if np.all(self.game[-1][:,:,7,1] == 0) and np.all(self.game[-1][:, :, 7,2] ==0) and np.all(self.game[-1][:,:,7,3] ==0):
                    newboard = self.game[-1].copy()
                    newboard[pieces.king, colors.white, 7,2] = 1
                    newboard[pieces.king, colors.white, 7,4] = 0
                    
                    newboard[pieces.rook, colors.white, 7,3] = 1
                    newboard[pieces.rook, colors.white, 7,0] = 0
                    self.game.append(newboard)


        elif color == 'black':
            if move == 'O-O':
                #first check if theres things between white king and kingside rook
                if np.all(self.game[-1][:,:,0,5] == 0) and np.all(self.game[-1][:, :, 0,6] ==0):
                    newboard = self.game[-1].copy()
                    newboard[pieces.king, colors.black, 0,6] = 1
                    newboard[pieces.king, colors.black, 0,4] = 0
                    
                    newboard[pieces.rook, colors.black, 0,5] = 1
                    newboard[pieces.rook, colors.black, 0,7] = 0
                    self.game.append(newboard)
            elif move == 'O-O-O':
                if np.all(self.game[-1][:,:,0,1] == 0) and np.all(self.game[-1][:, :, 0,2] ==0) and np.all(self.game[-1][:,:,0,3] ==0):
                    newboard = self.game[-1].copy()
                    newboard[pieces.king, colors.black, 0,2] = 1
                    newboard[pieces.king, colors.black, 0,4] = 0
                    
                    newboard[pieces.rook, colors.black, 0,3] = 1
                    newboard[pieces.rook, colors.black, 0,0] = 0
                    self.game.append(newboard)

    
    def updateWinner(self, winner):
        self.winner = winner
    
    def getWinner(self):
        return self.winner
        
    def copyBoard(self):
        return self.game[-1]
    
    def getBoard(self, index):
        return self.game[index]
    
    def getData(self):
        return self.game, self.winner

    def visualizeGame(self):
        for game in self.game:
            visualizeChessboard(game)
            
    def visualizeArray(self):
        return self.game
    
    def takePiece(self):
        self.pieces -= 1
    
    def addPiece(self):
        self.pieces +=1
    
    def checkPieces(self, position):
        num_pieces = (self.game[-1] == 1).sum()
        if self.pieces != num_pieces:
            raise ValueError('number of pieces is incorrect', position)
        if np.array_equal(self.game[-1],self.game[-2]):
            raise ValueError('the last 2 boards are the same', position)
        
    def lengthOfGame(self):
        return len(self.game)

def analyzeGame(game):
    moves = game.split()
    # print(moves)
    startChessboard = startingChessboard()
    newGame = ChessGame(startChessboard)
    for i in range(len(moves)):
   
            
        if moves[i] == '{White' or moves[i]=='0-1':
            newGame.updateWinner('Black')
            break

        elif moves[i] == '{Black' or moves[i]=='1-0':
            newGame.updateWinner('White')
            break
            
        
        elif moves[i] == '{Game' or moves[i]=='{Neither' or moves[i]== '1-1':
            newGame.updateWinner('Draw')
            break
        
            
        elif i %3 == 0:
            assert re.match('[0-9]+\.', moves[i]) 
        
        elif i % 3 == 1: #this will be white's move
            if 'x' in moves[i]:
                newGame.takePiece()
            if list(moves[i])[0] == 'O':
                # print('test')
                if list(moves[i])[-1] == '+' or list(moves[i])[-1] == '#':
                    newGame.castle(moves[i][0:-1], 'white')
                else:
                    newGame.castle(moves[i], 'white')
                    
            elif '=' in list(moves[i]):
                if list(moves[i])[-1] == '+' or list(moves[i])[-1] == '#':
                    newGame.promote(moves[i][0:-1], 'white')
                elif list(moves[i])[-2] == '=':
                    
                    newGame.promote(moves[i], 'white')
    
            elif list(moves[i])[-1] == '+' or list(moves[i])[-1] == '#':

                newGame.addBoard(''.join(list(moves[i])[0:-1]), 'white')
            else:
                newGame.addBoard(moves[i], 'white')
#                 newBoard = newGame.copyBoard()
#                 row, column = changeBoardPosition(moves[i])
#                 piece = findPiece(moves[i])

#                 addedboard = findOldPosition(moves[i],newBoard,row, column,piece,'white')
#                 # print(addedboard,[pieces.pawn, colors.white])
#                 # visualizeChessboard(addedboard)
#                 visualizeChessboard(newGame.getBoard(0))
                    # newGame.addBoard(newBoard
            newGame.checkPieces(moves[i])
            # print(moves[i])
            # visualizeChessboard(newGame.copyBoard())
            

        elif i % 3 == 2:
            if 'x' in moves[i]:
                newGame.takePiece()
            if list(moves[i])[0] == 'O':
                # print('test')
                if list(moves[i])[-1] == '+' or list(moves[i])[-1] == '#':
                    newGame.castle(''.join(list(moves[i])[0:-1]), 'black')
                else:
                    newGame.castle(moves[i], 'black')
                    
            elif '=' in list(moves[i]):
                if list(moves[i])[-1] == '+' or list(moves[i])[-1] == '#':
                    newGame.promote(moves[i][0:-1], 'black')
                elif list(moves[i])[-2] == '=':
                    newGame.promote(moves[i], 'black')
                
            elif list(moves[i])[-1] == '+' or list(moves[i])[-1] == '#':
                newGame.addBoard(''.join(list(moves[i])[0:-1]), 'black')
            else:
                newGame.addBoard(moves[i], 'black')
#                 newBoard = newGame.copyBoard()
#                 row, column = changeBoardPosition(moves[i])
#                 piece = findPiece(moves[i])

#                 addedboard = findOldPosition(moves[i],newBoard,row, column,piece,'black')
                # print(addedboard,[pieces.pawn, colors.white])
                # visualizeChessboard(addedboard)
                
                # newGame.addBoard(newBoard)
            # if i ==8:
            #     # newGame.visualizeGame()
            #     break
        # newGame.visualizeAll()
            newGame.checkPieces(moves[i])
            # print(moves[i])
            # visualizeChessboard(newGame.copyBoard())
    return newGame

def checkIfBoardPossible(board, color):
    if color == 'black':
    #check rook
        findRook = np.where(board[pieces.rook, colors.black, :, :] == 1)
        for x, y in zip(findRook[0], findRook[1]):
            if np.any(board[pieces.rook, colors.white, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
            if np.any(board[pieces.king,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False
        findKnight = np.where(board[pieces.knight, colors.black, :, :] == 1)
        for x, y in zip(findKnight[0], findKnight[1]):
            if np.any(board[pieces.knight, colors.white, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.king,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False
        findBishop = np.where(board[pieces.bishop, colors.black, :, :] == 1)
        for x, y in zip(findBishop[0], findBishop[1]):
            if np.any(board[pieces.bishop, colors.white, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.king,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False
        findQueen = np.where(board[pieces.queen, colors.black, :, :] == 1)
        for x, y in zip(findQueen[0], findQueen[1]):
            if np.any(board[pieces.queen, colors.white, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.king,:, x,y] ==1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
        findKing = np.where(board[pieces.king, colors.black, :, :] == 1)
        for x, y in zip(findKing[0], findKing[1]):
            if np.any(board[pieces.king, colors.white, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False
        findPawn = np.where(board[pieces.pawn, colors.black, :, :] == 1)
        for x, y in zip(findPawn[0], findPawn[1]):
            if np.any(board[pieces.pawn, colors.white, x,y]== 1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.king,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False       
        findRook = np.where(board[pieces.rook, colors.white, :, :] == 1)
        
        for x, y in zip(findRook[0], findRook[1]):

            findDown = x
            while findDown != 0:
                findDown-=1
                if np.any(board[:, :, findDown, y] == 1):
                    if np.any(board[pieces.king, colors.black, findDown, y] == 1):

                        return False
                    else:
                        break


            findUp = x

            while findUp != 7:
                findUp+=1
                if np.any(board[:, :, findUp, y] == 1):
                    if np.any(board[pieces.king, colors.black, findUp, y] == 1):
                        return False
                    else:
                        break


            findRight = y

            while findRight!=7:
                findRight+=1
                if np.any(board[:, :, x, findRight] == 1):
                    if np.any(board[pieces.king, colors.black, x, findRight] == 1):
                        return False
                    else:
                        break


            findLeft= y
            while findLeft!=0:
                findLeft-=1
                if np.any(board[:, :, x, findLeft] == 1):
                    if np.any(board[pieces.king, colors.black, x, findLeft] == 1):
                        return False
                    else:
                        break
        #now do bishop
        findBishop = np.where(board[pieces.bishop, colors.white, :, :] == 1)

        for x, y in zip(findBishop[0], findBishop[1]):

            
            findDown = x
            findRight = y
            while findDown != 0 and findRight != 7:
                findDown-=1
                findRight+=1
                if np.any(board[:, :, findDown, findRight] == 1):
                    if np.any(board[pieces.king, colors.black, findDown, findRight] == 1):

                        return False
                    else:
                        break


            findUp = x
            findRight = y
            while findUp != 7 and findRight != 7:
                findUp+=1
                findRight+=1
                if np.any(board[:, :, findUp, findRight] == 1):
                    if np.any(board[pieces.king, colors.black, findUp, findRight] == 1):

                        return False
                    else:
                        break


            findUp = x
            findLeft = y
            while findUp != 7 and findLeft != 0:
                findUp+=1
                findLeft-=1
                if np.any(board[:, :, findUp, findLeft] == 1):
                    if np.any(board[pieces.king, colors.black, findUp, findLeft] == 1):

                        return False
                    else:
                        break

            findDown = x
            findLeft = y
            while findDown != 0 and findLeft != 0:
                findDown-=1
                findLeft-=1
                if np.any(board[:, :, findDown, findLeft] == 1):
                    if np.any(board[pieces.king, colors.black, findDown, findLeft] == 1):

                        return False
                    else:
                        break
        #now do queen
        findQueen = np.where(board[pieces.queen, colors.white, :, :] == 1)
        for x, y in zip(findQueen[0], findQueen[1]):



            findDown = x
            while findDown != 0:
                findDown-=1
                if np.any(board[:, :, findDown, y] == 1):
                    if np.any(board[pieces.king, colors.black, findDown, y] == 1):

                        return False
                    else:
                        break


            findUp = x

            while findUp != 7:
                findUp+=1
                if np.any(board[:, :, findUp, y] == 1):
                    if np.any(board[pieces.king, colors.black, findUp, y] == 1):
                        return False
                    else:
                        break


            findRight = y

            while findRight!=7:
                findRight+=1
                if np.any(board[:, :, x, findRight] == 1):
                    if np.any(board[pieces.king, colors.black, x, findRight] == 1):
                        return False
                    else:
                        break


            findLeft= y
            while findLeft!=0:
                findLeft-=1
                if np.any(board[:, :, x, findLeft] == 1):
                    if np.any(board[pieces.king, colors.black, x, findLeft] == 1):
                        return False
                    else:
                        break
            findDown = x
            findRight = y
            while findDown != 0 and findRight != 7:
                findDown-=1
                findRight+=1
                if np.any(board[:, :, findDown, findRight] == 1):
                    if np.any(board[pieces.king, colors.black, findDown, findRight] == 1):

                        return False
                    else:
                        break


            findUp = x
            findRight = y
            while findUp != 7 and findRight != 7:
                findUp+=1
                findRight+=1
                if np.any(board[:, :, findUp, findRight] == 1):
                    if np.any(board[pieces.king, colors.black, findUp, findRight] == 1):

                        return False
                    else:
                        break


            findUp = x
            findLeft = y
            while findUp != 7 and findLeft != 0:
                findUp+=1
                findLeft-=1
                if np.any(board[:, :, findUp, findLeft] == 1):
                    if np.any(board[pieces.king, colors.black, findUp, findLeft] == 1):

                        return False
                    else:
                        break

            findDown = x
            findLeft = y
            while findDown != 0 and findLeft != 0:
                findDown-=1
                findLeft-=1
                if np.any(board[:, :, findDown, findLeft] == 1):
                    if np.any(board[pieces.king, colors.black, findDown, findLeft] == 1):

                        return False
                    else:
                        break
        #now do knight
        findKnight = np.where(board[pieces.knight, colors.white, :, :] == 1)
        for x, y in zip(findKnight[0], findKnight[1]):


            if x+2 <= 7 and y+1 <= 7:
                if np.any(board[pieces.king, colors.black, x+2, y+1] == 1):
                    return False

            if x+2 <= 7 and y-1 >=0:

                if np.any(board[pieces.king, colors.black, x+2, y-1] == 1):
                    return False

            if x-2 >= 0 and y+1 <=7:
                if np.any(board[pieces.king, colors.black, x-2, y+1] == 1):
                    return False

            if x-2 >= 0 and y-1 >=0:
                if np.any(board[pieces.king, colors.black, x-2, y-1] == 1):
                    return False

            if x+1 <= 7 and y+2 <= 7:
                if np.any(board[pieces.king, colors.black, x+1, y+2] == 1):
                    return False

            if x+1 <= 7 and y-2 >=0:
                if np.any(board[pieces.king, colors.black, x+1, y-2] == 1):
                    return False

            if x-1 >= 0 and y+2 <=7:
                if np.any(board[pieces.king, colors.black, x-1, y+2] == 1):
                    return False

            if x-1 >= 0 and y-2 >=0:

                if np.any(board[pieces.king, colors.black, x-1, y-2] == 1):
                    return False

        findpawn = np.where(board[pieces.pawn, colors.white, :, :] == 1)
        for x, y in zip(findpawn[0], findpawn[1]):

            if x-1 >=0 and y-1 >=0:
                if np.any(board[pieces.king, colors.black, x-1, y-1] == 1):
                    return False

            if x-1 >=0 and y+1 <=7:
                if np.any(board[pieces.king, colors.black, x-1, y+1] == 1):
                    return False

        findKing = np.where(board[pieces.king, colors.white, :, :] == 1)
        for x,y in zip(findKing[0], findKing[1]):

            if x+1 <= 7 and y+1 <=7:
                if np.any(board[pieces.king, colors.black, x+1, y+1] == 1):
                    return False

            if x+1 <= 7:
                if np.any(board[pieces.king, colors.black, x+1, y] == 1):
                    return False

            if x+1 <= 7 and y-1 >=0:
                if np.any(board[pieces.king, colors.black, x+1, y-1] == 1):
                    return False
            if x-1 >= 0 and y+1 <=7:
                if np.any(board[pieces.king, colors.black, x-1, y+1] == 1):
                    return False

            if x-1 >= 0:
                if np.any(board[pieces.king, colors.black, x-1, y] == 1):
                    return False

            if x-1 >= 0 and y-1 >=0:
                if np.any(board[pieces.king, colors.black, x-1, y-1] == 1):
                    return False
            if y+1 <= 7:
                if np.any(board[pieces.king, colors.black, x, y+1] == 1):
                    return False

            if y-1 >= 0:
                if np.any(board[pieces.king, colors.black, x, y-1] == 1):
                    return False

    elif color == 'white':
        findRook = np.where(board[pieces.rook, colors.white, :, :] == 1)
        for x, y in zip(findRook[0], findRook[1]):
            if np.any(board[pieces.rook, colors.black, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
            if np.any(board[pieces.king,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False
        findKnight = np.where(board[pieces.knight, colors.white, :, :] == 1)
        for x, y in zip(findKnight[0], findKnight[1]):
            if np.any(board[pieces.knight, colors.black, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.king,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False
        findBishop = np.where(board[pieces.bishop, colors.white, :, :] == 1)
        for x, y in zip(findBishop[0], findBishop[1]):
            if np.any(board[pieces.bishop, colors.black, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.king,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False
        findQueen = np.where(board[pieces.queen, colors.white, :, :] == 1)
        for x, y in zip(findQueen[0], findQueen[1]):
            if np.any(board[pieces.queen, colors.black, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.king,:, x,y] ==1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
        findKing = np.where(board[pieces.king, colors.white, :, :] == 1)
        for x, y in zip(findKing[0], findKing[1]):
            if np.any(board[pieces.king, colors.black, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False
        findPawn = np.where(board[pieces.pawn, colors.white, :, :] == 1)
        for x, y in zip(findPawn[0], findPawn[1]):
            if np.any(board[pieces.pawn, colors.black, x,y]== 1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.king,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False       
        findRook = np.where(board[pieces.rook, colors.black, :, :] == 1)
    
        for x, y in zip(findRook[0], findRook[1]):
            
            findDown = x
            while findDown != 0:
                findDown-=1
                if np.any(board[:, :, findDown, y] == 1):
                    if np.any(board[pieces.king, colors.white, findDown, y] == 1):

                        return False
                    else:
                        break


            findUp = x

            while findUp != 7:
                findUp+=1
                if np.any(board[:, :, findUp, y] == 1):
                    if np.any(board[pieces.king, colors.white, findUp, y] == 1):
                        return False
                    else:
                        break


            findRight = y

            while findRight!=7:
                findRight+=1
                if np.any(board[:, :, x, findRight] == 1):
                    if np.any(board[pieces.king, colors.white, x, findRight] == 1):
                        return False
                    else:
                        break


            findLeft= y
            while findLeft!=0:
                findLeft-=1
                if np.any(board[:, :, x, findLeft] == 1):
                    if np.any(board[pieces.king, colors.white, x, findLeft] == 1):
                        return False
                    else:
                        break
        #now do bishop
        findBishop = np.where(board[pieces.bishop, colors.black, :, :] == 1)
        for x, y in zip(findBishop[0], findBishop[1]):
            findDown = x
            findRight = y
            while findDown != 0 and findRight != 7:
                findDown-=1
                findRight+=1
                if np.any(board[:, :, findDown, findRight] == 1):
                    if np.any(board[pieces.king, colors.white, findDown, findRight] == 1):

                        return False
                    else:
                        break


            findUp = x
            findRight = y
            while findUp != 7 and findRight != 7:
                findUp+=1
                findRight+=1
                if np.any(board[:, :, findUp, findRight] == 1):
                    if np.any(board[pieces.king, colors.white, findUp, findRight] == 1):

                        return False
                    else:
                        break


            findUp = x
            findLeft = y
            while findUp != 7 and findLeft != 0:
                findUp+=1
                findLeft-=1
                if np.any(board[:, :, findUp, findLeft] == 1):
                    if np.any(board[pieces.king, colors.white, findUp, findLeft] == 1):

                        return False
                    else:
                        break

            findDown = x
            findLeft = y
            while findDown != 0 and findLeft != 0:
                findDown-=1
                findLeft-=1
                if np.any(board[:, :, findDown, findLeft] == 1):
                    if np.any(board[pieces.king, colors.white, findDown, findLeft] == 1):

                        return False
                    else:
                        break
        #now do queen
        findQueen = np.where(board[pieces.queen, colors.black, :, :] == 1)
        for x, y in zip(findQueen[0], findQueen[1]):
            findDown = x
            while findDown != 0:
                findDown-=1
                if np.any(board[:, :, findDown, y] == 1):
                    if np.any(board[pieces.king, colors.white, findDown, y] == 1):

                        return False
                    else:
                        break


            findUp = x

            while findUp != 7:
                findUp+=1
                if np.any(board[:, :, findUp, y] == 1):
                    if np.any(board[pieces.king, colors.white, findUp, y] == 1):
                        return False
                    else:
                        break


            findRight = y

            while findRight!=7:
                findRight+=1
                if np.any(board[:, :, x, findRight] == 1):
                    if np.any(board[pieces.king, colors.white, x, findRight] == 1):
                        return False
                    else:
                        break


            findLeft= y
            while findLeft!=0:
                findLeft-=1
                if np.any(board[:, :, x, findLeft] == 1):
                    if np.any(board[pieces.king, colors.white, x, findLeft] == 1):
                        return False
                    else:
                        break
            findDown = x
            findRight = y
            while findDown != 0 and findRight != 7:
                findDown-=1
                findRight+=1
                if np.any(board[:, :, findDown, findRight] == 1):
                    if np.any(board[pieces.king, colors.white, findDown, findRight] == 1):

                        return False
                    else:
                        break


            findUp = x
            findRight = y
            while findUp != 7 and findRight != 7:
                findUp+=1
                findRight+=1
                if np.any(board[:, :, findUp, findRight] == 1):
                    if np.any(board[pieces.king, colors.white, findUp, findRight] == 1):

                        return False
                    else:
                        break


            findUp = x
            findLeft = y
            while findUp != 7 and findLeft != 0:
                findUp+=1
                findLeft-=1
                if np.any(board[:, :, findUp, findLeft] == 1):
                    if np.any(board[pieces.king, colors.white, findUp, findLeft] == 1):

                        return False
                    else:
                        break

            findDown = x
            findLeft = y
            while findDown != 0 and findLeft != 0:
                findDown-=1
                findLeft-=1
                if np.any(board[:, :, findDown, findLeft] == 1):
                    if np.any(board[pieces.king, colors.white, findDown, findLeft] == 1):

                        return False
                    else:
                        break
        #now do knight
        findKnight = np.where(board[pieces.knight, colors.black, :, :] == 1)
        for x, y in zip(findKnight[0], findKnight[1]):

            # print('got past knight checks')
            # print(board[:,:,x,y])
            # print(x,y)
            # print(board[pieces.bishop,colors.white,x,y])
            if x+2 <= 7 and y+1 <= 7:
                if np.any(board[pieces.king, colors.white, x+2, y+1] == 1):
                    return False

            if x+2 <= 7 and y-1 >=0:

                if np.any(board[pieces.king, colors.white, x+2, y-1] == 1):
                    return False

            if x-2 >= 0 and y+1 <=7:
                if np.any(board[pieces.king, colors.white, x-2, y+1] == 1):
                    return False

            if x-2 >= 0 and y-1 >=0:
                if np.any(board[pieces.king, colors.white, x-2, y-1] == 1):
                    return False

            if x+1 <= 7 and y+2 <= 7:
                if np.any(board[pieces.king, colors.white, x+1, y+2] == 1):
                    return False

            if x+1 <= 7 and y-2 >=0:
                if np.any(board[pieces.king, colors.white, x+1, y-2] == 1):
                    return False

            if x-1 >= 0 and y+2 <=7:
                if np.any(board[pieces.king, colors.white, x-1, y+2] == 1):
                    return False

            if x-1 >= 0 and y-2 >=0:

                if np.any(board[pieces.king, colors.white, x-1, y-2] == 1):
                    return False

        findpawn = np.where(board[pieces.pawn, colors.black, :, :] == 1)
        for x, y in zip(findpawn[0], findpawn[1]):



            if x+1 <=7 and y-1 >=0:
                if np.any(board[pieces.king, colors.white, x+1, y-1] == 1):
                    return False

            if x+1 <=7 and y+1 <=7:
                if np.any(board[pieces.king, colors.white, x+1, y+1] == 1):
                    return False

        findKing = np.where(board[pieces.king, colors.black, :, :] == 1)
        for x,y in zip(findKing[0], findKing[1]):
            if np.any(board[pieces.king, colors.white, x,y]== 1):
                return False
            if np.any(board[pieces.pawn,:, x,y] ==1):
                return False
            if np.any(board[pieces.bishop,:, x,y] ==1):
                return False
            if np.any(board[pieces.knight,:, x,y] ==1):
                return False
            if np.any(board[pieces.rook,:, x,y] ==1):
                return False
            if np.any(board[pieces.queen,:, x,y] ==1):
                return False
            if x+1 <= 7 and y+1 <=7:
                if np.any(board[pieces.king, colors.black, x+1, y+1] == 1):
                    return False

            if x+1 <= 7:
                if np.any(board[pieces.king, colors.white, x+1, y] == 1):
                    return False

            if x+1 <= 7 and y-1 >=0:
                if np.any(board[pieces.king, colors.white, x+1, y-1] == 1):
                    return False
            if x-1 >= 0 and y+1 <=7:
                if np.any(board[pieces.king, colors.white, x-1, y+1] == 1):
                    return False

            if x-1 >= 0:
                if np.any(board[pieces.king, colors.white, x-1, y] == 1):
                    return False

            if x-1 >= 0 and y-1 >=0:
                if np.any(board[pieces.king, colors.white, x-1, y-1] == 1):
                    return False
            if y+1 <= 7:
                if np.any(board[pieces.king, colors.white, x, y+1] == 1):
                    return False

            if y-1 >= 0:
                if np.any(board[pieces.king, colors.white, x, y-1] == 1):
                    return False
    return True

def findEveryPossibleMove(board, toMove):
    #make move
    #pawn
    possibleMoveList = []
    if toMove == 'white':
        
        findPawn = np.where(board[pieces.pawn, colors.white, :, :] == 1)

        for x, y in zip(findPawn[0], findPawn[1]):
            if x == 6:
                #pawn moves up 1
                newBoard = board.copy()
                newBoard[pieces.pawn, colors.white, x-1, y] = 1
                newBoard[pieces.pawn, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)
                
                #pawn moves up 2
                newBoard = board.copy()
                newBoard[pieces.pawn, colors.white, x-2, y] = 1
                newBoard[pieces.pawn, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)

            elif x-1 == 0:
                for i in range(1,5):
                    newBoard = board.copy()
                    newBoard[i,colors.white,x-1,y] = 1
                    newBoard[pieces.pawn, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
            
            else:
                newBoard = board.copy()
                newBoard[pieces.pawn, colors.white, x-1, y] = 1
                newBoard[pieces.pawn, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)
            
            #check captures now
            if y-1 >=0:
                if np.any(board[:, colors.black, x-1, y-1] == 1) and x-1!=0:
                    newBoard = board.copy()
                    newBoard[:, colors.black,x-1,y-1] = 0 
                    newBoard[pieces.pawn, colors.white,x,y] = 1
                    newBoard[pieces.pawn, colors.white, x-1,y-1] = 1
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                    
                if np.any(board[:, colors.black, x-1, y-1] == 1) and x-1==0:
                    for i in range(1,5):
                        newBoard = board.copy()
                        newBoard[:, colors.black,x-1,y-1] = 0 
                        newBoard[i,colors.white,x-1,y-1] = 1
                        newBoard[pieces.pawn, colors.white, x, y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
            if y+1 <=7:
                if np.any(board[:, colors.black, x-1, y+1] == 1) and x-1!=0:
                    newBoard = board.copy()
                    newBoard[:, colors.black,x-1,y+1] = 0 
                    newBoard[pieces.pawn, colors.white,x,y] = 1
                    newBoard[pieces.pawn, colors.white, x-1,y+1] = 1
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                        
                if np.any(board[:, colors.black, x-1, y+1] == 1) and x-1==0:
                    for i in range(1,5):
                        newBoard = board.copy()
                        newBoard[:, colors.black,x-1,y+1] = 0 
                        newBoard[i,colors.white,x-1,y+1] = 1
                        newBoard[pieces.pawn, colors.white, x, y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                
                
        #do knight now
        findKnight = np.where(board[pieces.knight, colors.white, :, :] == 1)
        for x, y in zip(findKnight[0], findKnight[1]):
            if x+2 <= 7 and y+1 <= 7:
                if np.any(board[:, colors.black, x+2, y+1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x+2,y+1] = 0 
                    newBoard[pieces.knight,colors.white,x+2,y+1] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.white,x+2,y+1] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if x+2 <= 7 and y-1 >=0:

                if np.any(board[:, colors.black, x+2, y-1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x+2,y-1] = 0 
                    newBoard[pieces.knight,colors.white,x+2,y-1] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.white,x+2,y-1] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if x-2 >= 0 and y+1 <=7:
                if np.any(board[:, colors.black, x-2, y+1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x-2,y+1] = 0 
                    newBoard[pieces.knight,colors.white,x-2,y+1] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.white,x-2,y+1] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if x-2 >= 0 and y-1 >=0:
                if np.any(board[:, colors.black, x-2, y-1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x-2,y-1] = 0 
                    newBoard[pieces.knight,colors.white,x-2,y-1] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.white,x-2,y-1] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if x+1 <= 7 and y+2 <= 7:
                if np.any(board[:, colors.black, x+1, y+2] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x+1,y+2] = 0 
                    newBoard[pieces.knight,colors.white,x+1,y+2] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.white,x+1,y+2] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if x+1 <= 7 and y-2 >=0:
                if np.any(board[:, colors.black, x+1, y-2] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x+1,y-2] = 0 
                    newBoard[pieces.knight,colors.white,x+1,y-2] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.white,x+1,y-2] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if x-1 >= 0 and y+2 <=7:
                if np.any(board[:, colors.black, x-1, y+2] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x-1,y+2] = 0 
                    newBoard[pieces.knight,colors.white,x-1,y+2] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.white,x-1,y+2] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
            if x-1 >= 0 and y-2 >=0:

                if np.any(board[:, colors.black, x-1, y-2] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x-1,y-2] = 0 
                    newBoard[pieces.knight,colors.white,x-1,y-2] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.white,x-1,y-2] = 1
                    newBoard[pieces.knight, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
        
        findBishop = np.where(board[pieces.bishop, colors.white, :, :] == 1)
        for x, y in zip(findBishop[0], findBishop[1]):
            findDown = x
            findRight = y
            while findDown != 0 and findRight != 7:
                findDown-=1
                findRight+=1
                
                newBoard = board.copy()
                if np.any(board[:, :, findDown, findRight] == 1):
                    if np.any(board[:, colors.black, findDown, findRight]) == 1:
                        newBoard[:, colors.black, findDown, findRight] = 0
                        newBoard[pieces.bishop,colors.white,findDown,findRight] = 1
                        newBoard[pieces.bishop,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.bishop,colors.white,findDown,findRight] = 1
                newBoard[pieces.bishop, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)


            findUp = x
            findRight = y
            while findUp != 7 and findRight != 7:
                findUp+=1
                findRight+=1
                
                newBoard = board.copy()
                if np.any(board[:, :, findUp, findRight] == 1):
                    if np.any(board[:, colors.black, findUp, findRight] == 1):
                        newBoard[:, colors.black, findUp, findRight] = 0
                        newBoard[pieces.bishop,colors.white,findUp,findRight] = 1
                        newBoard[pieces.bishop,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.bishop,colors.white,findUp,findRight] = 1
                newBoard[pieces.bishop, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)


            findUp = x
            findLeft = y
            while findUp != 7 and findLeft != 0:
                findUp+=1
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, findUp, findLeft] == 1):
                    if np.any(board[:, colors.black, findUp, findLeft] == 1):
                        newBoard[:, colors.black, findUp, findLeft] = 0
                        newBoard[pieces.bishop,colors.white,findUp,findLeft] = 1
                        newBoard[pieces.bishop,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.bishop,colors.white,findUp,findLeft] = 1
                newBoard[pieces.bishop, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)

            findDown = x
            findLeft = y
            while findDown != 0 and findLeft != 0:
                findDown-=1
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, findDown, findLeft] == 1):
                    if np.any(board[:, colors.black, findDown, findLeft] == 1):
                        newBoard[:, colors.black, findDown, findLeft] = 0
                        newBoard[pieces.bishop,colors.white,findDown,findLeft] = 1
                        newBoard[pieces.bishop,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.bishop,colors.white,findDown,findLeft] = 1
                newBoard[pieces.bishop, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)
                    
        findRook = np.where(board[pieces.rook, colors.white, :, :] == 1)
    
        for x, y in zip(findRook[0], findRook[1]):
            
            findDown = x
            while findDown != 0:
                findDown-=1
                newBoard = board.copy()
                if np.any(board[:, :, findDown, y] == 1):
                    if np.any(board[:, colors.black, findDown, y] == 1):
                        newBoard[:, colors.black, findDown, y] = 0
                        newBoard[pieces.rook,colors.white,findDown,y] = 1
                        newBoard[pieces.rook,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.rook,colors.white,findDown,y] = 1
                newBoard[pieces.rook, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)


            findUp = x
            while findUp != 7:
                findUp+=1
                newBoard = board.copy()
                if np.any(board[:, :, findUp, y] == 1):
                    if np.any(board[:, colors.black, findUp, y] == 1):
                        newBoard[:, colors.black, findUp, y] = 0
                        newBoard[pieces.rook,colors.white,findUp,y] = 1
                        newBoard[pieces.rook,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.rook,colors.white,findUp,y] = 1
                newBoard[pieces.rook, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)


            findRight = y

            while findRight!=7:
                findRight+=1
                newBoard = board.copy()
                if np.any(board[:, :, x, findRight] == 1):
                    if np.any(board[:, colors.black, x, findRight] == 1):
                        newBoard[:, colors.black, x, findRight] = 0
                        newBoard[pieces.rook,colors.white,x, findRight] = 1
                        newBoard[pieces.rook,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.rook,colors.white,x, findRight] = 1
                newBoard[pieces.rook, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)


            findLeft= y
            while findLeft!=0:
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, x, findLeft] == 1):
                    if np.any(board[:, colors.black, x, findLeft] == 1):
                        newBoard[:, colors.black, x, findLeft] = 0
                        newBoard[pieces.rook,colors.white,x, findLeft] = 1
                        newBoard[pieces.rook,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.rook,colors.white,x, findLeft] = 1
                newBoard[pieces.rook, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)
                    
        findQueen = np.where(board[pieces.queen, colors.white, :, :] == 1)
    
        for x, y in zip(findQueen[0], findQueen[1]):
            
            findDown = x
            while findDown != 0:
                findDown-=1
                newBoard = board.copy()
                if np.any(board[:, :, findDown, y] == 1):
                    if np.any(board[:, colors.black, findDown, y] == 1):
                        newBoard[:, colors.black, findDown, y] = 0
                        newBoard[pieces.queen,colors.white,findDown,y] = 1
                        newBoard[pieces.queen,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.white,findDown,y] = 1
                newBoard[pieces.queen, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)


            findUp = x

            while findUp != 7:
                findUp+=1
                newBoard = board.copy()
                if np.any(board[:, :, findUp, y] == 1):
                    if np.any(board[:, colors.black, findUp, y] == 1):
                        newBoard[:, colors.black, findUp, y] = 0
                        newBoard[pieces.queen,colors.white,findUp,y] = 1
                        newBoard[pieces.queen,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.white,findUp,y] = 1
                newBoard[pieces.queen, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)


            findRight = y

            while findRight!=7:
                findRight+=1
                newBoard = board.copy()
                if np.any(board[:, :, x, findRight] == 1):
                    if np.any(board[:, colors.black, x, findRight] == 1):
                        newBoard[:, colors.black, x, findRight] = 0
                        newBoard[pieces.queen,colors.white,x, findRight] = 1
                        newBoard[pieces.queen,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.white,x, findRight] = 1
                newBoard[pieces.queen, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)


            findLeft= y
            while findLeft!=0:
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, x, findLeft] == 1):
                    if np.any(board[:, colors.black, x, findLeft] == 1):
                        newBoard[:, colors.black, x, findLeft] = 0
                        newBoard[pieces.queen,colors.white,x, findLeft] = 1
                        newBoard[pieces.queen,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.white,x, findLeft] = 1
                newBoard[pieces.queen, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)
                    
            findDown = x
            findRight = y
            while findDown != 0 and findRight != 7:
                findDown-=1
                findRight+=1
                
                newBoard = board.copy()
                if np.any(board[:, :, findDown, findRight] == 1):
                    if np.any(board[:, colors.black, findDown, findRight]) == 1:
                        newBoard[:, colors.black, findDown, findRight] = 0
                        newBoard[pieces.queen,colors.white,findDown,findRight] = 1
                        newBoard[pieces.queen,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.white,findDown,findRight] = 1
                newBoard[pieces.queen, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)


            findUp = x
            findRight = y
            while findUp != 7 and findRight != 7:
                findUp+=1
                findRight+=1
                
                newBoard = board.copy()
                if np.any(board[:, :, findUp, findRight] == 1):
                    if np.any(board[:, colors.black, findUp, findRight] == 1):
                        newBoard[:, colors.black, findUp, findRight] = 0
                        newBoard[pieces.queen,colors.white,findUp,findRight] = 1
                        newBoard[pieces.queen,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.white,findUp,findRight] = 1
                newBoard[pieces.queen, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)


            findUp = x
            findLeft = y
            while findUp != 7 and findLeft != 0:
                findUp+=1
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, findUp, findLeft] == 1):
                    if np.any(board[:, colors.black, findUp, findLeft] == 1):
                        newBoard[:, colors.black, findUp, findLeft] = 0
                        newBoard[pieces.queen,colors.white,findUp,findLeft] = 1
                        newBoard[pieces.queen,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.white,findUp,findLeft] = 1
                newBoard[pieces.queen, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)

            findDown = x
            findLeft = y
            while findDown != 0 and findLeft != 0:
                findDown-=1
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, findDown, findLeft] == 1):
                    if np.any(board[:, colors.black, findDown, findLeft] == 1):
                        newBoard[:, colors.black, findDown, findLeft] = 0
                        newBoard[pieces.queen,colors.white,findDown,findLeft] = 1
                        newBoard[pieces.queen,colors.white,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'white') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.white,findDown,findLeft] = 1
                newBoard[pieces.queen, colors.white, x, y] = 0
                if checkIfBoardPossible(newBoard, 'white') == True:
                    possibleMoveList.append(newBoard)
                    
        findKing = np.where(board[pieces.king, colors.white, :, :] == 1)
        for x,y in zip(findKing[0], findKing[1]):

            if x+1 <= 7 and y+1 <=7:
                if np.any(board[:, colors.black, x+1, y+1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x+1,y+1] = 0 
                    newBoard[pieces.king,colors.white,x+1,y+1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.white,x+1,y+1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if x+1 <= 7:
                if np.any(board[:, colors.black, x+1, y] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x+1, y] = 0 
                    newBoard[pieces.king,colors.white,x+1, y] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.white,x+1, y] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if x+1 <= 7 and y-1 >=0:
                if np.any(board[:, colors.black, x+1, y-1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x+1, y-1] = 0 
                    newBoard[pieces.king,colors.white,x+1, y-1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.white,x+1, y-1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
            if x-1 >= 0 and y+1 <=7:
                if np.any(board[:, colors.black, x-1, y+1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x-1, y+1] = 0 
                    newBoard[pieces.king,colors.white,x-1, y+1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.white,x-1, y+1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if x-1 >= 0:
                if np.any(board[:, colors.black, x-1, y] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x-1, y] = 0 
                    newBoard[pieces.king,colors.white,x-1, y] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.white,x-1, y] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if x-1 >= 0 and y-1 >=0:
                if np.any(board[:, colors.black, x-1, y-1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x-1, y-1] = 0 
                    newBoard[pieces.king,colors.white,x-1, y-1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.white,x-1, y-1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
            if y+1 <= 7:
                if np.any(board[:, colors.black, x, y+1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x, y+1] = 0 
                    newBoard[pieces.king,colors.white,x, y+1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.white,x, y+1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)

            if y-1 >= 0:
                if np.any(board[:, colors.black, x, y-1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.black,x, y-1] = 0 
                    newBoard[pieces.king,colors.white,x, y-1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.white,x, y-1] = 1
                    newBoard[pieces.king, colors.white, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'white') == True:
                        possibleMoveList.append(newBoard)
    #check if king is in check afterwards
    elif toMove == 'black':
        findPawn = np.where(board[pieces.pawn, colors.black, :, :] == 1)

        for x, y in zip(findPawn[0], findPawn[1]):
            if x == 6:
                #pawn moves up 1
                newBoard = board.copy()
                newBoard[pieces.pawn, colors.black, x-1, y] = 1
                newBoard[pieces.pawn, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)
                
                #pawn moves up 2
                newBoard = board.copy()
                newBoard[pieces.pawn, colors.black, x-2, y] = 1
                newBoard[pieces.pawn, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)

            elif x-1 == 0:
                for i in range(1,5):
                    newBoard = board.copy()
                    newBoard[i,colors.black,x-1,y] = 1
                    newBoard[pieces.pawn, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
            
            else:
                newBoard = board.copy()
                newBoard[pieces.pawn, colors.black, x-1, y] = 1
                newBoard[pieces.pawn, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)
            
            #check captures now
            if y-1 >=0:
                if np.any(board[:, colors.white, x-1, y-1] == 1) and x-1!=0:
                    newBoard = board.copy()
                    newBoard[:, colors.white,x-1,y-1] = 0 
                    newBoard[pieces.pawn, colors.black,x,y] = 1
                    newBoard[pieces.pawn, colors.black, x-1,y-1] = 1
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                    
                if np.any(board[:, colors.white, x-1, y-1] == 1) and x-1==0:
                    for i in range(1,5):
                        newBoard = board.copy()
                        newBoard[:, colors.white,x-1,y-1] = 0 
                        newBoard[i,colors.black,x-1,y-1] = 1
                        newBoard[pieces.pawn, colors.black, x, y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
            if y+1 <=7:
                if np.any(board[:, colors.white, x-1, y+1] == 1) and x-1!=0:
                    newBoard = board.copy()
                    newBoard[:, colors.white,x-1,y+1] = 0 
                    newBoard[pieces.pawn, colors.black,x,y] = 1
                    newBoard[pieces.pawn, colors.black, x-1,y+1] = 1
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                        
                if np.any(board[:, colors.white, x-1, y+1] == 1) and x-1==0:
                    for i in range(1,5):
                        newBoard = board.copy()
                        newBoard[:, colors.white,x-1,y+1] = 0 
                        newBoard[i,colors.black,x-1,y+1] = 1
                        newBoard[pieces.pawn, colors.black, x, y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                
                
        #do knight now
        findKnight = np.where(board[pieces.knight, colors.black, :, :] == 1)
        for x, y in zip(findKnight[0], findKnight[1]):
            if x+2 <= 7 and y+1 <= 7:
                if np.any(board[:, colors.white, x+2, y+1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x+2,y+1] = 0 
                    newBoard[pieces.knight,colors.black,x+2,y+1] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.black,x+2,y+1] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if x+2 <= 7 and y-1 >=0:

                if np.any(board[:, colors.white, x+2, y-1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x+2,y-1] = 0 
                    newBoard[pieces.knight,colors.black,x+2,y-1] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.black,x+2,y-1] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if x-2 >= 0 and y+1 <=7:
                if np.any(board[:, colors.white, x-2, y+1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x-2,y+1] = 0 
                    newBoard[pieces.knight,colors.black,x-2,y+1] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.black,x-2,y+1] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if x-2 >= 0 and y-1 >=0:
                if np.any(board[:, colors.white, x-2, y-1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x-2,y-1] = 0 
                    newBoard[pieces.knight,colors.black,x-2,y-1] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.black,x-2,y-1] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if x+1 <= 7 and y+2 <= 7:
                if np.any(board[:, colors.white, x+1, y+2] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x+1,y+2] = 0 
                    newBoard[pieces.knight,colors.black,x+1,y+2] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.black,x+1,y+2] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if x+1 <= 7 and y-2 >=0:
                if np.any(board[:, colors.white, x+1, y-2] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x+1,y-2] = 0 
                    newBoard[pieces.knight,colors.black,x+1,y-2] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.black,x+1,y-2] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if x-1 >= 0 and y+2 <=7:
                if np.any(board[:, colors.white, x-1, y+2] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x-1,y+2] = 0 
                    newBoard[pieces.knight,colors.black,x-1,y+2] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.black,x-1,y+2] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
            if x-1 >= 0 and y-2 >=0:

                if np.any(board[:, colors.white, x-1, y-2] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x-1,y-2] = 0 
                    newBoard[pieces.knight,colors.black,x-1,y-2] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.knight,colors.black,x-1,y-2] = 1
                    newBoard[pieces.knight, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
        
        findBishop = np.where(board[pieces.bishop, colors.black, :, :] == 1)
        for x, y in zip(findBishop[0], findBishop[1]):
            findDown = x
            findRight = y
            while findDown != 0 and findRight != 7:
                findDown-=1
                findRight+=1
                
                newBoard = board.copy()
                if np.any(board[:, :, findDown, findRight] == 1):
                    if np.any(board[:, colors.white, findDown, findRight]) == 1:
                        newBoard[:, colors.white, findDown, findRight] = 0
                        newBoard[pieces.bishop,colors.black,findDown,findRight] = 1
                        newBoard[pieces.bishop,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.bishop,colors.black,findDown,findRight] = 1
                newBoard[pieces.bishop, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)


            findUp = x
            findRight = y
            while findUp != 7 and findRight != 7:
                findUp+=1
                findRight+=1
                
                newBoard = board.copy()
                if np.any(board[:, :, findUp, findRight] == 1):
                    if np.any(board[:, colors.white, findUp, findRight] == 1):
                        newBoard[:, colors.white, findUp, findRight] = 0
                        newBoard[pieces.bishop,colors.black,findUp,findRight] = 1
                        newBoard[pieces.bishop,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.bishop,colors.black,findUp,findRight] = 1
                newBoard[pieces.bishop, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)


            findUp = x
            findLeft = y
            while findUp != 7 and findLeft != 0:
                findUp+=1
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, findUp, findLeft] == 1):
                    if np.any(board[:, colors.white, findUp, findLeft] == 1):
                        newBoard[:, colors.white, findUp, findLeft] = 0
                        newBoard[pieces.bishop,colors.black,findUp,findLeft] = 1
                        newBoard[pieces.bishop,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.bishop,colors.black,findUp,findLeft] = 1
                newBoard[pieces.bishop, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)

            findDown = x
            findLeft = y
            while findDown != 0 and findLeft != 0:
                findDown-=1
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, findDown, findLeft] == 1):
                    if np.any(board[:, colors.white, findDown, findLeft] == 1):
                        newBoard[:, colors.white, findDown, findLeft] = 0
                        newBoard[pieces.bishop,colors.black,findDown,findLeft] = 1
                        newBoard[pieces.bishop,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.bishop,colors.black,findDown,findLeft] = 1
                newBoard[pieces.bishop, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)
                    
        findRook = np.where(board[pieces.rook, colors.black, :, :] == 1)
    
        for x, y in zip(findRook[0], findRook[1]):
            
            findDown = x
            while findDown != 0:
                findDown-=1
                newBoard = board.copy()
                if np.any(board[:, :, findDown, y] == 1):
                    if np.any(board[:, colors.white, findDown, y] == 1):
                        newBoard[:, colors.white, findDown, y] = 0
                        newBoard[pieces.rook,colors.black,findDown,y] = 1
                        newBoard[pieces.rook,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.rook,colors.black,findDown,y] = 1
                newBoard[pieces.rook, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)


            findUp = x
            while findUp != 7:
                findUp+=1
                newBoard = board.copy()
                if np.any(board[:, :, findUp, y] == 1):
                    if np.any(board[:, colors.white, findUp, y] == 1):
                        newBoard[:, colors.white, findUp, y] = 0
                        newBoard[pieces.rook,colors.black,findUp,y] = 1
                        newBoard[pieces.rook,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.rook,colors.black,findUp,y] = 1
                newBoard[pieces.rook, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)


            findRight = y

            while findRight!=7:
                findRight+=1
                newBoard = board.copy()
                if np.any(board[:, :, x, findRight] == 1):
                    if np.any(board[:, colors.white, x, findRight] == 1):
                        newBoard[:, colors.white, x, findRight] = 0
                        newBoard[pieces.rook,colors.black,x, findRight] = 1
                        newBoard[pieces.rook,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.rook,colors.black,x, findRight] = 1
                newBoard[pieces.rook, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)


            findLeft= y
            while findLeft!=0:
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, x, findLeft] == 1):
                    if np.any(board[:, colors.white, x, findLeft] == 1):
                        newBoard[:, colors.white, x, findLeft] = 0
                        newBoard[pieces.rook,colors.black,x, findLeft] = 1
                        newBoard[pieces.rook,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.rook,colors.black,x, findLeft] = 1
                newBoard[pieces.rook, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)
                    
        findQueen = np.where(board[pieces.queen, colors.black, :, :] == 1)
    
        for x, y in zip(findQueen[0], findQueen[1]):
            
            findDown = x
            while findDown != 0:
                findDown-=1
                newBoard = board.copy()
                if np.any(board[:, :, findDown, y] == 1):
                    if np.any(board[:, colors.white, findDown, y] == 1):
                        newBoard[:, colors.white, findDown, y] = 0
                        newBoard[pieces.queen,colors.black,findDown,y] = 1
                        newBoard[pieces.queen,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.black,findDown,y] = 1
                newBoard[pieces.queen, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)


            findUp = x

            while findUp != 7:
                findUp+=1
                newBoard = board.copy()
                if np.any(board[:, :, findUp, y] == 1):
                    if np.any(board[:, colors.white, findUp, y] == 1):
                        newBoard[:, colors.white, findUp, y] = 0
                        newBoard[pieces.queen,colors.black,findUp,y] = 1
                        newBoard[pieces.queen,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.black,findUp,y] = 1
                newBoard[pieces.queen, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)


            findRight = y

            while findRight!=7:
                findRight+=1
                newBoard = board.copy()
                if np.any(board[:, :, x, findRight] == 1):
                    if np.any(board[:, colors.white, x, findRight] == 1):
                        newBoard[:, colors.white, x, findRight] = 0
                        newBoard[pieces.queen,colors.black,x, findRight] = 1
                        newBoard[pieces.queen,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.black,x, findRight] = 1
                newBoard[pieces.queen, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)


            findLeft= y
            while findLeft!=0:
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, x, findLeft] == 1):
                    if np.any(board[:, colors.white, x, findLeft] == 1):
                        newBoard[:, colors.white, x, findLeft] = 0
                        newBoard[pieces.queen,colors.black,x, findLeft] = 1
                        newBoard[pieces.queen,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.black,x, findLeft] = 1
                newBoard[pieces.queen, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)
                    
            findDown = x
            findRight = y
            while findDown != 0 and findRight != 7:
                findDown-=1
                findRight+=1
                
                newBoard = board.copy()
                if np.any(board[:, :, findDown, findRight] == 1):
                    if np.any(board[:, colors.white, findDown, findRight]) == 1:
                        newBoard[:, colors.white, findDown, findRight] = 0
                        newBoard[pieces.queen,colors.black,findDown,findRight] = 1
                        newBoard[pieces.queen,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.black,findDown,findRight] = 1
                newBoard[pieces.queen, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)


            findUp = x
            findRight = y
            while findUp != 7 and findRight != 7:
                findUp+=1
                findRight+=1
                
                newBoard = board.copy()
                if np.any(board[:, :, findUp, findRight] == 1):
                    if np.any(board[:, colors.white, findUp, findRight] == 1):
                        newBoard[:, colors.white, findUp, findRight] = 0
                        newBoard[pieces.queen,colors.black,findUp,findRight] = 1
                        newBoard[pieces.queen,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.black,findUp,findRight] = 1
                newBoard[pieces.queen, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)


            findUp = x
            findLeft = y
            while findUp != 7 and findLeft != 0:
                findUp+=1
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, findUp, findLeft] == 1):
                    if np.any(board[:, colors.white, findUp, findLeft] == 1):
                        newBoard[:, colors.white, findUp, findLeft] = 0
                        newBoard[pieces.queen,colors.black,findUp,findLeft] = 1
                        newBoard[pieces.queen,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.black,findUp,findLeft] = 1
                newBoard[pieces.queen, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)

            findDown = x
            findLeft = y
            while findDown != 0 and findLeft != 0:
                findDown-=1
                findLeft-=1
                newBoard = board.copy()
                if np.any(board[:, :, findDown, findLeft] == 1):
                    if np.any(board[:, colors.white, findDown, findLeft] == 1):
                        newBoard[:, colors.white, findDown, findLeft] = 0
                        newBoard[pieces.queen,colors.black,findDown,findLeft] = 1
                        newBoard[pieces.queen,colors.black,x,y] = 0
                        if checkIfBoardPossible(newBoard, 'black') == True:
                            possibleMoveList.append(newBoard)
                    break
                
                newBoard[pieces.queen,colors.black,findDown,findLeft] = 1
                newBoard[pieces.queen, colors.black, x, y] = 0
                if checkIfBoardPossible(newBoard, 'black') == True:
                    possibleMoveList.append(newBoard)
                    
        findKing = np.where(board[pieces.king, colors.black, :, :] == 1)
        for x,y in zip(findKing[0], findKing[1]):

            if x+1 <= 7 and y+1 <=7:
                if np.any(board[:, colors.white, x+1, y+1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x+1,y+1] = 0 
                    newBoard[pieces.king,colors.black,x+1,y+1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.black,x+1,y+1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if x+1 <= 7:
                if np.any(board[:, colors.white, x+1, y] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x+1, y] = 0 
                    newBoard[pieces.king,colors.black,x+1, y] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.black,x+1, y] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if x+1 <= 7 and y-1 >=0:
                if np.any(board[:, colors.white, x+1, y-1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x+1, y-1] = 0 
                    newBoard[pieces.king,colors.black,x+1, y-1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.black,x+1, y-1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
            if x-1 >= 0 and y+1 <=7:
                if np.any(board[:, colors.white, x-1, y+1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x-1, y+1] = 0 
                    newBoard[pieces.king,colors.black,x-1, y+1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.black,x-1, y+1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if x-1 >= 0:
                if np.any(board[:, colors.white, x-1, y] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x-1, y] = 0 
                    newBoard[pieces.king,colors.black,x-1, y] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.black,x-1, y] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if x-1 >= 0 and y-1 >=0:
                if np.any(board[:, colors.white, x-1, y-1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x-1, y-1] = 0 
                    newBoard[pieces.king,colors.black,x-1, y-1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.black,x-1, y-1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
            if y+1 <= 7:
                if np.any(board[:, colors.white, x, y+1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x, y+1] = 0 
                    newBoard[pieces.king,colors.black,x, y+1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.black,x, y+1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

            if y-1 >= 0:
                if np.any(board[:, colors.white, x, y-1] == 1):
                    newBoard = board.copy()
                    newBoard[:, colors.white,x, y-1] = 0 
                    newBoard[pieces.king,colors.black,x, y-1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)
                else:
                    newBoard = board.copy()
                    newBoard[pieces.king,colors.black,x, y-1] = 1
                    newBoard[pieces.king, colors.black, x, y] = 0
                    if checkIfBoardPossible(newBoard, 'black') == True:
                        possibleMoveList.append(newBoard)

    return possibleMoveList

def createListOfGames(your_filename,totalData, outfilex, outfiley):
    dctx = zstd.ZstdDecompressor()
    i = 0
    list_of_games = []
    list_of_errors = []
    list_of_combined =[]
    partline = False
    decodeBug = False
    numData = 0
    x_data= []
    y_data = []
    
    with open(your_filename, 'rb') as fin:
        reader = dctx.stream_reader(fin)
        while True:
            chunk = reader.read(3000)
            byte_string = chunk

    # Convert the byte string to a string using the decode() method
            try:
                decoded_string = byte_string.decode("utf-8")
            except:
                print("could not decode line")
                decodeBug=True
            # Print the decoded string
            if decodeBug !=True:
                decoded_lines = decoded_string.splitlines()
                # print(decoded_lines)
                if partline == True:
                    newline = pline + decoded_lines[0]
                    list_of_combined.append(newline)
                    decoded_lines[0] = 'a'

                for line in decoded_lines:
                    if len(line) > 0:
                        if line[0:2] == '1.':
                            # print('test')
                            if line[-2:] == '-0' or line[-2:] == '-1':


                                # print(line)

                                try:
                                    # print('test2')
                                    game = analyzeGame(line)
                                    board, winner = game.getData()
                                    
                                    x_data.append(board)
                                    if winner == "White":
                                        y_data.append(1)
                                    elif winner == "Black":
                                        y_data.append(0)
                                    elif winner == "Draw":
                                        y_data.append(.5)
                                    
                                    numData+=1
                                    if numData >= totalData:
                                        break
                                    # print(list_of_games)
                                except:
                                    # print('error')
                                    list_of_errors.append(line)
                                partline = False
                            else:
                                pline = line
                                partline = True
            else:
                decodeBug=False
            # print(list_of_games)

            # print(list_of_games)
            if numData >= totalData:
                break
#             i+=1

#             if i >= numChunks:
#                 break

    np.savez(outfilex, x_data)

    
    return list_of_games, list_of_errors

# def createData(data, numDatapoints, numPergame):
#     createarray = np.zeros(shape= [numDatapoints*numPergame,2,6,2,8,8] )
#     numpoints = 0
#     listOfWinners = []
#     while numpoints < numDatapoints:

#         game = data[numpoints]
#         listofnums = []

#         for i in range(numPergame):
#             listofnums.append(random.randint(0,game.lengthOfGame()-1))
            
#         # print(listofnums)
#         if game.getWinner() == 'White':

#             for num in listofnums:
                
#                 if num %2 ==0:
#                     createarray[numpoints, 0,:,:,:,:] = game.getBoard(num)
#                     try:
#                         createarray[numpoints, 1,:,:,:,:] = game.getBoard(num+1)
#                     except:
#                         createarray[numpoints, 0,:,:,:,:] = game.getBoard(num-2)
#                         createarray[numpoints, 1,:,:,:,:] = game.getBoard(num-1)

#                 else:
#                     try:
#                         createarray[numpoints, 0,:,:,:,:] = game.getBoard(num-1)
#                         createarray[numpoints, 1,:,:,:,:] = game.getBoard(num)
#                     except:
#                         createarray[numpoints, 0,:,:,:,:] = game.getBoard(num+1)
#                         createarray[numpoints, 1,:,:,:,:] = game.getBoard(num+2)
#                 listOfWinners.append('white')
#                 numpoints+=1

#         elif game.getWinner() == 'Black':
#             for num in listofnums:
#                 if num %2 ==1:
#                     createarray[numpoints, 0,:,:,:,:] = game.getBoard(num)
#                     try:
#                         createarray[numpoints, 1,:,:,:,:] = game.getBoard(num+1)
#                     except:
#                         createarray[numpoints, 0,:,:,:,:] = game.getBoard(num-2)
#                         createarray[numpoints, 1,:,:,:,:] = game.getBoard(num-1)

#                 else:
#                     try:
#                         createarray[numpoints, 0,:,:,:,:] = game.getBoard(num-1)
#                         createarray[numpoints, 1,:,:,:,:] = game.getBoard(num)
#                     except:
#                         createarray[numpoints, 0,:,:,:,:] = game.getBoard(num+1)
#                         createarray[numpoints, 1,:,:,:,:] = game.getBoard(num+2)
#                 listOfWinners.append('black')
#                 numpoints+=1
#     return createarray, listOfWinners

def newCreateData(your_filename, numDataPoints,xsavefiles,ysavefiles):
    # def createListOfGames(your_filename,numChunks):
    dctx = zstd.ZstdDecompressor()
    i = 0
    x_data = np.zeros(shape= [numDataPoints,6,2,8,8])
    y_data = np.zeros(shape= [numDataPoints])
    # list_of_games = []
    # list_of_errors = []
    list_of_combined =[]
    partline = False
    numpoints = 0
    decodeBug = False
    progress = True
    
    
    
    with open(your_filename, 'rb') as fin:
        reader = dctx.stream_reader(fin)
        
        while True:
            chunk = reader.read(3000)
            if not chunk:
                break
            byte_string = chunk
            try:
    # Convert the byte string to a string using the decode() method
                decoded_string = byte_string.decode("utf-8")
            except:
                
                decodeBug = True
                # Print the decoded string
            if decodeBug != True:
                decoded_lines = decoded_string.splitlines()

                if partline == True:
                    newline = pline + decoded_lines[0]
                    list_of_combined.append(newline)
                    decoded_lines[0] = 'a'

                for line in decoded_lines:
                    if len(line) > 0:
                        if line[0:2] == '1.':
                            if line[-2:] == '-0' or line[-2:] == '-1':


                                # print(line)

                                try:


                                    game = analyzeGame(line)
                                    randnum = random.randint(0,game.lengthOfGame()-1)
                                    x_data[numpoints,:,:,:,:] = game.getBoard(randnum)

                                    if game.getWinner() == "White":
                                        y_data[numpoints] = 1
                                    elif game.getWinner() == "Black":
                                        y_data[numpoints] = 0
                                    elif game.getWinner() == "Draw":
                                        y_data[numpoints] = .5
                                    numpoints +=1
                                    progress = True
                                    

                                    if numpoints >= numDataPoints:
                                        break

                                except:
                                    # list_of_errors.append(line)
                                    pass
                                partline = False
                            else:
                                pline = line
                                partline = True
            else:
                decodeBug = False
            
            if numpoints % 1000 == 0 and progress == True:
                print("you have now created", numpoints, "data points")
                progress = False
            if numpoints >= numDataPoints:
                break

            # print(list_of_games)
            
            # i+=1
            # if i >= numChunks:
            #     break
    np.save(xsavefiles, x_data)
    np.save(ysavefiles, y_data)
    
    return x_data, y_data
    # return list_of_games, list_of_errors
#     x_data = np.zeros(shape= [numDataPoints,6,2,8,8])
#     y_data = []
#     numpoints = 0
    
#     while numpoints < numDataPoints:
#         game = data[numpoints]
#         randnum = random.randint(0,game.lengthOfGame()-1)

#         x_data[numpoints,:,:,:,:] = game.getBoard(randnum)

#         if game.getWinner() == "White":
#             y_data.append(1)
#         elif game.getWinner() == "Black":
#             y_data.append(0)
#         elif game.getWinner() == "Draw":
#             y_data.append(.5)
#         numpoints +=1
#     return x_data, y_data
def newCreateMultiData(fileList, numDataPoints, xDataName, yDataName):
    dataMade = 0
    dctx = zstd.ZstdDecompressor()
    arraysize = int(numDataPoints / 10)
    print(arraysize)
    dataMadeMod = 0
    filenum = 1
    decodeBug= False
    list_of_combined =[]
    
    x_data = np.zeros(shape = [arraysize, 6,2,8,8])
    y_data = np.zeros(shape = [arraysize])
    # np.save(xDataName,x_data)
    # np.save(yDataName, y_data)
    
    partline = False
    print("I start creating Data")
    test = 0
    progress = True
    for file in fileList:
        print("now using file:", file)


        with open(file, 'rb') as fin:
            reader = dctx.stream_reader(fin)
        
            while True:
                chunk = reader.read(3000)
                if not chunk:
                    break
                byte_string = chunk
                
                try:
    # Convert the byte string to a string using the decode() method
                    decoded_string = byte_string.decode("utf-8")
                except:

                    decodeBug = True
                    # Print the decoded string
                if decodeBug != True:
                    decoded_lines = decoded_string.splitlines()
                    
                    if partline == True:
                        newline = pline + decoded_lines[0]
                        try:
                            game = analyzeGame(line)
                            randnum = random.randint(0,game.lengthOfGame()-1)
                            x_data[dataMadeMod,:,:,:,:] = game.getBoard(randnum)

                            if game.getWinner() == "White":
                                y_data[dataMadeMod] = 1
                            elif game.getWinner() == "Black":
                                y_data[dataMadeMod] = 0
                            elif game.getWinner() == "Draw":
                                y_data[dataMadeMod] = .5

                            dataMade +=1
                            dataMadeMod +=1

                            if dataMadeMod == arraysize:


                                np.save(xDataName + str(filenum), x_data)
                                np.save(yDataName + str(filenum), y_data)
                                dataMadeMod = 0
                                filenum+=1


                            progress = True
                            if dataMade >= numDataPoints:

                                break
                                
                        except:
                            pass
                        decoded_lines[0] = 'a'
                        
                    for line in decoded_lines:
                        if len(line) > 0:
                            if line[0:2] == '1.':
                                if line[-2:] == '-0' or line[-2:] == '-1':
                                    try:
                                        
                                        game = analyzeGame(line)
                                        randnum = random.randint(0,game.lengthOfGame()-1)
                                        x_data[dataMadeMod,:,:,:,:] = game.getBoard(randnum)

                                        if game.getWinner() == "White":
                                            y_data[dataMadeMod] = 1
                                        elif game.getWinner() == "Black":
                                            y_data[dataMadeMod] = 0
                                        elif game.getWinner() == "Draw":
                                            y_data[dataMadeMod] = .5
                                        
                                        dataMade +=1
                                        dataMadeMod +=1
                                        
                                        if dataMadeMod == arraysize:

                                            
                                            np.save(xDataName + str(filenum), x_data)
                                            np.save(yDataName + str(filenum), y_data)
                                            dataMadeMod = 0
                                            filenum+=1
 
                                            
                                        progress = True


                                        if dataMade >= numDataPoints:

                                            break

                                    except:
                                        # list_of_errors.append(line)
                                        pass
                                    
                                    partline = False
                                else:
                                    pline = line
                                    partline = True
                            
                else:
                    decodeBug = False
                if dataMade % 100 == 0 and progress == True:
                    print("you have now created", dataMade, "data points")
                    progress = False
                if dataMade >= numDataPoints:
                    break
        
        if dataMade >= numDataPoints:
            break
        
        
        
    

def newCreateDataTest(your_filename, numDataPoints, numTestPoints):
    # def createListOfGames(your_filename,numChunks):
    dctx = zstd.ZstdDecompressor()
    i = 0
    x_data = np.zeros(shape= [numDataPoints,6,2,8,8])
    y_data = []
    x_test_data = np.zeros(shape= [numTestPoints,6,2,8,8])
    y_test_data = []
    # list_of_games = []
    # list_of_errors = []
    list_of_combined =[]
    partline = False
    numpoints = 0
    totalPoints = numDataPoints + numTestPoints
    
    with open(your_filename, 'rb') as fin:
        reader = dctx.stream_reader(fin)
        
        while True:
            chunk = reader.read(3000)
            byte_string = chunk

    # Convert the byte string to a string using the decode() method
            decoded_string = byte_string.decode("utf-8")

            # Print the decoded string
            decoded_lines = decoded_string.splitlines()

            if partline == True:
                newline = pline + decoded_lines[0]
                list_of_combined.append(newline)
                decoded_lines[0] = 'a'
            
            for line in decoded_lines:
                if len(line) > 0:
                    if line[0:2] == '1.':
                        if line[-2:] == '-0' or line[-2:] == '-1':


                            # print(line)

                            try:
                                
                                if numPoints < numDataPoints:
                                    game = analyzeGame(line)
                                    randnum = random.randint(0,game.lengthOfGame()-1)
                                    x_data[numpoints,:,:,:,:] = game.getBoard(randnum)

                                    if game.getWinner() == "White":
                                        y_data.append(1)
                                    elif game.getWinner() == "Black":
                                        y_data.append(0)
                                    elif game.getWinner() == "Draw":
                                        y_data.append(.5)
                                    numpoints +=1
                                else:
                                    game = analyzeGame(line)
                                    randnum = random.randint(0,game.lengthOfGame()-1)
                                    x_test_data[numpoints,:,:,:,:] = game.getBoard(randnum)

                                    if game.getWinner() == "White":
                                        y_test_data.append(1)
                                    elif game.getWinner() == "Black":
                                        y_test_data.append(0)
                                    elif game.getWinner() == "Draw":
                                        y_test_data.append(.5)
                                    numpoints +=1

                                if numpoints >= totalPoints:
                                    break
                      
                            except:
                                # list_of_errors.append(line)
                                pass
                            partline = False
                        else:
                            pline = line
                            partline = True
            if numpoints >= totalPoints:
                break

            # print(list_of_games)
            
            # i+=1
            # if i >= numChunks:
            #     break
    return x_data, y_data, x_test_data, y_test_data

    