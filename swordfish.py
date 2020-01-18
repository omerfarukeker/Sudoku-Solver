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
import itertools

#%%fast starter, load data
# import pickle
# # pickle.dump([cands,board,grid,square_pos],open("for_swordfish.sav","wb"))
# cands,board,grid,square_pos = pickle.load(open("for_swordfish.sav","rb"))

#%% SWORDFISH  
def swordfish(board,cands,square_pos):
    ischanged = 0
    #check swordfish for both rows and columns
    for rowcol in ["rows","cols"]:
        # print(rowcol)
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
        
        for wing in range(len(wings)):
            # print(wings[wing])
            for comb in itertools.combinations(enumerate(wings[wing]),3):
                # print(comb)
                flag = False
                temp = []
                for i in comb:
                    if len(i[1])<=1:
                        flag = True
                    temp.extend(i[1])
                
                if flag:    
                    continue
                temp = pd.Series(temp)
                valco = temp.value_counts()
                if len(valco)==3 and sum(valco)>=6:
                    # print(comb)
                    # print(valco)
                    cols_to_remove = temp.unique()
                    # print(cols_to_remove)
                    
                    #remove values from the columns
                    rem = wing+1
                    for cols in cols_to_remove:
                        #drop the wing rows and nans
                        use = cands[cols].dropna()
                        for rows in use.index:
                            if rem in use[rows] and not rows in [comb[0][0],comb[1][0],comb[2][0]]:
                                cands.set_value(rows,cols,np.delete(cands.iloc[rows,cols],np.where(cands.iloc[rows,cols]==rem)))
                                ischanged = 1
                                print(f"R{rows}C{cols}     Swordfish, {rem} removed from {rowcol}")
                    if ischanged:
                        solver.solver(board,cands,square_pos) 
                    
    cands = cands.T
    return cands

# cands = swordfish(board,cands,square_pos)