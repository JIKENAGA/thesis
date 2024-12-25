import chessfunctions
import neuralnetwork
import torch
import numpy as np
import torch.nn as nn
import chessboardtests
model = neuralnetwork.NeuralNetwork()

    
model = neuralnetwork.NeuralNetwork()
model.load_state_dict(torch.load("/home/jikenaga2/model4"))
model.eval()


# position = chessfunctions.startingChessboard()

startingBoards = chessboardtests.listOfStartingBoards()
endBoards = chessboardtests.listOfEndBoards()

# for board in startingBoards:
#     possiblemovelist = chessfunctions.findEveryPossibleMove(board, "white")
#     currentPlayer = "white"
#     firstmovetensor = torch.tensor(possiblemovelist[0]).float()
#     firstmovetensor = firstmovetensor[None,:,:,:]
#     bestBoardPosition = model(firstmovetensor)
#     bestmove = possiblemovelist[0]
    
#     for move in possiblemovelist:
    
#         movetensor = torch.tensor(move).float()
#         movetensor = movetensor[None,:, :,:]
#         output = model(movetensor)
#         if currentPlayer == "white":
#             if output[0].item() > bestBoardPosition:
#                 bestmove = move

#         else:
#             if output[0].item() < bestBoardPosition:
#                 bestmove = move
                
#     chessfunctions.visualizeChessboard(board)
#     chessfunctions.visualizeChessboard(bestmove)
#     print(bestBoardPosition[0].item())


    




def createBoard():

    board = np.zeros([6,2,8,8])

    # np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.black, 1, :], [0,1,2,3,4,5,6,7,], 1)
    np.put(board[chessfunctions.pieces.pawn, chessfunctions.colors.white, 6, :], [0,1,2,3,4,5,6,7,], 1)
    # np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.black, 0, :], [1,6], 1)
    np.put(board[chessfunctions.pieces.knight, chessfunctions.colors.white, 7, :], [1,6], 1)
    # np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.black, 0, :], [2,5], 1)
    np.put(board[chessfunctions.pieces.bishop, chessfunctions.colors.white, 7, :], [2,5], 1)
    # np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.black, 0, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.rook, chessfunctions.colors.white, 7, :], [0,7], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.black, 0, :], [4], 1)
    np.put(board[chessfunctions.pieces.king, chessfunctions.colors.white, 7, :], [4], 1)
    # np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.black, 0, :], [3], 1)
    np.put(board[chessfunctions.pieces.queen, chessfunctions.colors.white, 7, :], [3], 1)
    
    return board
possiblemovelist = chessfunctions.findEveryPossibleMove(createBoard(), "white")
currentPlayer = "white"
firstmovetensor = torch.tensor(possiblemovelist[0]).float()
firstmovetensor = firstmovetensor[None,:,:,:]
bestBoardPosition = model(firstmovetensor)
bestmove = possiblemovelist[0]
for move in possiblemovelist:
    
    movetensor = torch.tensor(move).float()
    movetensor = movetensor[None,:, :,:]
    output = model(movetensor)
    if currentPlayer == "white":
        if output[0].item() > bestBoardPosition:
            bestmove = move
            
    else:
        if output[0].item() < bestBoardPosition:
            bestmove = move
            
    chessfunctions.visualizeChessboard(move)
    print(output[0].item())
    
# chessfunctions.visualizeChessboard(bestmove)
    # if output > bestBoardPosition:
    #     bestmove = move
        
