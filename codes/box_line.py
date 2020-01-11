# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:15:03 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
from candidate_handler import candidates_update
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver

#%% BOX/LINE REDUCTION

def box_line(board,cands,square_pos):
    ischanged = 0
    
    #rows
    for rows in range(9):
        use = cands.loc[rows].dropna()
        for val in range(1,10):
            inxs = use.apply(lambda x: val in x)
            if len(inxs) == 0:
                break
            inxs = list(inxs.index[inxs])
            
            #find locations of the box/line reduction candidates
            if len(inxs) == 2 or len(inxs) == 3:
                board_pos = square_pos.loc[rows][inxs]
                if np.diff(board_pos).sum() == 0:
                    square = board_pos.iloc[0]
                    inx = pd.Series(square_pos[square_pos == square].stack().index.tolist())
                    
                    #go through the square cells except the box/line
                    for ix in inx:
                        if ix[0] != rows:
                        # if ix != (rows,board_pos.index[0]) and ix != (rows,board_pos.index[1]) and ix != (rows,board_pos.index[2]):
                            try:
                                temp = cands.iloc[ix].tolist()
                                temp.remove(val)
                                cands.iloc[ix] = np.array(temp)
                                ischanged = 1
                                print(f"R{ix[0]}C{ix[1]}     Box/Line (row) reduction value {val} removed")
                            except:
                                pass
        
        #columns
        for cols in range(9):
            use = cands[cols].dropna()
            for val in range(1,10):
                inxs = use.apply(lambda x: val in x)
                if len(inxs) == 0:
                    break
                inxs = list(inxs.index[inxs])
                
                #find locations of the box/line reduction candidates
                if len(inxs) == 2 or len(inxs) == 3:
                    board_pos = square_pos[cols][inxs]
                    if np.diff(board_pos).sum() == 0:
                        square = board_pos.iloc[0]
                        inx = pd.Series(square_pos[square_pos == square].stack().index.tolist())
                        
                        #go through the square cells except the box/line
                        for ix in inx:
                            if ix[1] != cols:
                            # if ix != (board_pos.index[0],cols) and ix != (board_pos.index[1],cols):
                                try:
                                    temp = cands.iloc[ix].tolist()
                                    temp.remove(val)
                                    cands.iloc[ix] = np.array(temp)
                                    ischanged = 1
                                    print(f"R{ix[0]}C{ix[1]}     Box/Line (col) reduction value {val} removed")
                                except:
                                    pass
        
        
    if ischanged:
        solver.solver(board,cands,square_pos) 