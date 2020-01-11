# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:27:33 2020

@author: omer.eker
"""
import pandas as pd
import numpy as np
from cells_seen import cells_seen

#%% INITIALISE CANDIDATES
def candidates(board):
    cands = pd.DataFrame(np.full((9,9),np.nan))
    for row in range(9):
        for col in range(9):
            temp = []
            if board.iloc[row,col] == ".":
                temp.extend(board.iloc[row,:])
                temp.extend(board.iloc[:,col])
                temp.extend(board.loc[board.index[row]][board.columns[col]].values.flatten())
                temp = pd.Series(temp)
                drops = temp[temp!="."].unique()
                cand = pd.Series(np.arange(1,10),index=np.arange(1,10)).drop(drops).values.astype("O")
                
                #this part is for handling the "ValueError: setting an array element as a sequence"
                if len(cand) == 1:
                    if cand%1 == 0.0:
                        temp = cand.tolist()
                        temp.append(99)
                        cands[col][row] = np.array(temp).astype("O")
                        temp.remove(99)
                        cands[col][row] = np.array(temp).astype("O")
                else:
                    cands[col][row] = cand

    return cands
#%% UPDATE CANDIDATES
def candidates_update(cands,row,col,val,square_pos):
    #remove the value from candidate matrix first
    cands.iloc[row,col] = np.nan
    
    #locate the cells seen by the key cell
    seen_cells = cells_seen((row,col),square_pos)
    
    #remove the value from the seen cells
    for i in seen_cells:
        try:
            if val in cands.iloc[i]:
                cands.loc[i[0]][i[1]] = np.delete(cands.iloc[i],np.where(cands.iloc[i]==val))
        except:
            pass
    
    return cands