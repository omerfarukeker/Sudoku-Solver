# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:16:23 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
from candidate_handler import candidates_update
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver

#%% X-WING  
def x_wing(board,cands,square_pos):
    #check xwings for both rows and columns
    for rowcol in ["rows","cols"]:
        if rowcol == "cols":
            cands = cands.T
        ischanged = 0
        #construct candidate table
        wings = []
        for i in range(1,10):
            wing = []
            for rows in cands.index:
                use = cands.loc[rows].dropna()
                temp = []
                for cols in use.index:
                    if i in use[cols]:
                        temp.append(cols)
                wing.append(temp)
            wings.append(wing)      
        
        #loop through the candidates and eliminate
        for wing in range(len(wings)):
            # print(wings[wing])
            for i in range(9):
                for j in range(i+1,9):
                    if (len(wings[wing][i]) == 2) & (len(wings[wing][j]) == 2):
                        # print(f"pair_r{i}c{j}")
                        if wings[wing][i] == wings[wing][j]:
                            #remove candidates in the columns
                            for rem in wings[wing][i]:
                                use = cands[rem].dropna()
                                for ix in use.index:
                                    if not((ix == i) | (ix == j)):
                                        temp = use[ix].tolist()
                                        try:
                                            temp.remove(wing+1)
                                            print(f"R{ix}C{rem}     X-Wing, removed {wing+1} from {rowcol}")
                                            ischanged = 1
                                        except:
                                            pass
                                        use[ix] = np.array(temp)
                                cands[rem] = use
    cands = cands.T
    if ischanged:
        solver.solver(board,cands,square_pos) 