# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:29:00 2020

@author: omer.eker
"""
import sys
import pandas as pd
#%% construct the board from 81 digit grid string
def init_board(grid):
    
    if len(grid)==81:
        board = []
        
        for i in range(81):
            board.append(int(grid[i]))
        
        board = pd.Series(board).replace(0,".")
        board = pd.DataFrame(board.values.reshape((9,9)))
        
        board.index = ["A","A","A","B","B","B","C","C","C"]
        board.columns = ["A","A","A","B","B","B","C","C","C"]
        
        #helps finding the boxes when (row,col) pair is known
        square_pos = pd.DataFrame([ [1,1,1,2,2,2,3,3,3],
                                    [1,1,1,2,2,2,3,3,3],
                                    [1,1,1,2,2,2,3,3,3],
                                    [4,4,4,5,5,5,6,6,6],
                                    [4,4,4,5,5,5,6,6,6],
                                    [4,4,4,5,5,5,6,6,6],
                                    [7,7,7,8,8,8,9,9,9],
                                    [7,7,7,8,8,8,9,9,9],
                                    [7,7,7,8,8,8,9,9,9]])
        return board,square_pos
    else:
        print(f"Board length: {len(grid)}")
        sys.exit(1)