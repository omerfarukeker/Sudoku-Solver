# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:02:01 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver

#%% NAKED PAIRS
def naked_pairs(board,cands,square_pos):
    ischanged = 0
    
    #check rows
    for row in range(9):
        use = cands.loc[row].dropna()
        try:
            pairs = use[use.index[use.apply(lambda x: len(x) == 2)]]
            if len(pairs) >= 2:
                for i in pairs.index:
                    for j in pairs.index[pairs.index > i]:
                        if all(pairs[i] == pairs[j]):
                            # print(f"Row{row} Naked Pair: {pairs[i]}")
                            #remove found pair values in the rest of the cells in candidates
                            inxs = use.index.tolist()
                            inxs.remove(i)
                            inxs.remove(j)
                            for k in inxs:
                                temp = cands.loc[row][k].tolist()
                                for l in pairs[i]:
                                    try:
                                        temp.remove(l)
                                        print(f"R{row}C{k}     Naked Pair (row) {pairs[i]}, {l} removed")
                                        ischanged = 1
                                    except:
                                        pass
                                        # print("No length item")
                                cands.loc[row][k] = np.array(temp)
        except:
            pass
            # print(f"No pair found in row")
            
    #check columns
    for col in range(9):
        use = cands[col].dropna()
        try:
            pairs = use[use.index[use.apply(lambda x: len(x) == 2)]]
            if len(pairs) >= 2:
                for i in pairs.index:
                    for j in pairs.index[pairs.index > i]:
                        if all(pairs[i] == pairs[j]):
                            #remove found pair values in the rest of the cells in candidates
                            inxs = use.index.tolist()
                            inxs.remove(i)
                            inxs.remove(j)
                            for k in inxs:
                                temp = cands[col][k].tolist()
                                for l in pairs[i]:
                                    try:
                                        temp.remove(l)
                                        print(f"R{k}C{col}     Naked Pair (col) {pairs[i]}, {l} removed")
                                        ischanged = 1
                                    except:
                                        pass
                                        
                                cands[col][k] = np.array(temp)
                                
        except:
            pass
    
    #check squares
    for i in [[0,1,2],[3,4,5],[6,7,8]]:
        for j in [[0,1,2],[3,4,5],[6,7,8]]:
            use = cands.iloc[i,j]
            use_flat = pd.Series(use.values.flatten()).dropna()
            try:
                pairs = use_flat[use_flat.index[use_flat.apply(lambda x: len(x) == 2)]]
                if len(pairs) >= 2:
                    for pair1 in pairs.index:
                        for pair2 in pairs.index[pairs.index > pair1]:
                            if all(pairs[pair1] == pairs[pair2]):
                                # print(f"Square Naked Pair: {pairs[pair1]}")
                                #remove found pair values in the rest of the cells in candidates
                                
                                for ii in i:
                                    for jj in j:
                                        try:
                                            if len(use.loc[ii][jj])>=2:
                                                check = use.loc[ii][jj] == pairs[pair1]
                                                try:
                                                    check = all(check)
                                                except:
                                                    pass
                                                if not check:
                                                    temp = use.loc[ii][jj].tolist()
                                                    for l in pairs[pair1]:
                                                        try:
                                                            temp.remove(l)
                                                            print(f"R{ii}C{jj}     Naked Pair (square) {pairs[pair1]}, {l} removed")
                                                            ischanged = 1
                                                        except:
                                                            pass
                                                    use.loc[ii][jj] = np.array(temp)
                                                
                                        except:
                                            pass
                                cands.iloc[i,j] = use
            except:
                pass
                
            
        
    if ischanged:
        solver.solver(board,cands,square_pos) 
        