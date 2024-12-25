import numpy as np
import chessfunctions
def listOfStartingBoards():
    return [startingBoard1(), startingBoard2(), startingBoard3(), startingBoard4(), startingBoard5(),startingBoard6(), startingBoard7(),startingBoard8(), startingBoard9(), startingBoard10()]

def listOfEndBoards():
    return [endBoard1(), endBoard2(),endBoard3(),endBoard4(),endBoard5(),endBoard6(),endBoard7(),endBoard8(),endBoard9(),endBoard10(),]
def startingBoard1():

    board = np.zeros([6,2,8,8])

    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [0,1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [4], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [1,6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board

def startingBoard2():

    board = np.zeros([6,2,8,8])

    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [0,1,2,3,4,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,3,4,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [1,6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1,6], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board

def startingBoard3():

    board = np.zeros([6,2,8,8])

    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [0,1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [4], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board

def startingBoard4():

    board = np.zeros([6,2,8,8])

    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [0,1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [4], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 3, :], [1], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board

def startingBoard5():

    board = np.zeros([6,2,8,8])

    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [0,1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [4], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 3, :], [1], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board

def startingBoard6():

    board = np.zeros([6,2,8,8])

    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [0,1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [4], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 3, :], [1], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board

def startingBoard7():

    board = np.zeros([6,2,8,8])

    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 2, :], [0], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [4], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 3, :], [1], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board

def startingBoard8():

    board = np.zeros([6,2,8,8])

    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [1,2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 2, :], [0], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [4], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 4, :], [0], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board

def startingBoard9():

    board = np.zeros([6,2,8,8])

    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 2, :], [0], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 4, :], [0], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board

def startingBoard10():

    board = np.zeros([6,2,8,8])

    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 2, :], [0], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board

def endBoard1():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 2, :], [0], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 2, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 2, :], [5], 1)
    
    return board

def endBoard2():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 2, :], [4], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 2, :], [5], 1)
    
    return board

def endBoard3():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 2, :], [2], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 2, :], [5], 1)
    
    return board

def endBoard4():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 1, :], [3], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 2, :], [2], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 2, :], [5], 1)
    
    return board

def endBoard5():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 2, :], [2], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 0, :], [7], 1)
    
    return board

def endBoard6():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 1, :], [0], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 2, :], [2], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 0, :], [7], 1)
    
    return board
def endBoard7():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 1, :], [7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 2, :], [2], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 0, :], [7], 1)
    
    return board

def endBoard8():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 1, :], [7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 2, :], [2], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 0, :], [7], 1)
    
    return board
def endBoard9():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 1, :], [7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 2, :], [4], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 0, :], [7], 1)
    
    return board

def endBoard10():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [2,3,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 3, :], [1,4], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 5, :], [3], 1)
    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 4, :], [4], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 2, :], [2], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 5, :], [5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 5, :], [1], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 1, :], [7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [6], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 2, :], [4], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 0, :], [7], 1)
    
    return board