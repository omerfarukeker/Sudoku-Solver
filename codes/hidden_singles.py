# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:45:02 2020

@author: omer.eker
"""
import pandas as pd
from candidate_handler import candidates_update
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver

#%% HIDDEN SINGLES
def hidden_singles(board,cands,square_pos):
    is_changed = 0
    #check rows
    for row in range(9):
        temp = []
        for col in range(9):
            if board.iloc[row,col] == ".":
                temp.extend(cands.iloc[row,col])
        valco = pd.Series(temp).value_counts()
        for valun in valco.index[valco == 1].values: #????? there can be 1 and only 1 single candidate in a row..
            temp1 = cands.loc[row].dropna().apply(lambda x: valun in x)
            inx = temp1.index[temp1 == True]
            if len(inx):
                is_changed = 1
                for inxt in inx:
                    print(f"R{row+1}C{inxt+1}={valun} : Hidden Singles (row)")
                    board.iloc[row,inxt] = valun
                    cands = candidates_update(cands,row,inxt,valun,square_pos)
    
    #check columns
    for col in range(9):
        temp = []
        for row in range(9):
            if board.iloc[row,col] == ".":
                temp.extend(cands.iloc[row,col])
        valco = pd.Series(temp).value_counts()
        for valun in valco.index[valco == 1].values:
            temp1 = cands.iloc[:,col].dropna().apply(lambda x: valun in x)
            inx = temp1.index[temp1 == True]
            if len(inx):
                is_changed = 1
                for inxt in inx:
                    print(f"R{inxt+1}C{col+1}={valun} : Hidden Singles (col)")
                    board.iloc[inxt,col] = valun
                    cands = candidates_update(cands,inxt,col,valun,square_pos)        

    #check squares
    for i in [[0,1,2],[3,4,5],[6,7,8]]:
        for j in [[0,1,2],[3,4,5],[6,7,8]]:
            a = cands.iloc[i,j]
            a_flat = pd.Series(a.values.flatten()).dropna()
            temp = []
            for ix in a_flat: 
                temp.extend(ix)
            valco = pd.Series(temp).value_counts()
            
            if any(valco == 1):
                to_change_all = valco.index[valco == 1].values
                for to_change in to_change_all: #loop all values to be changed (sometimes multiple changes needed in a single box)
                    for rowx in a.index:
                        for colx in a.columns:
                            try: 
                                if board.iloc[rowx,colx] == ".":
                                    if to_change in a.loc[rowx][colx]:
                                        print(f"R{rowx+1}C{colx+1}={to_change} : Hidden Singles (square)")
                                        board.iloc[rowx,colx] = to_change
                                        cands = candidates_update(cands,rowx,colx,to_change,square_pos)
                                        is_changed = 1
                            except:
                                print("except")
    if is_changed:
        solver.solver(board,cands,square_pos)                       
    