# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:05:04 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver

#%% HIDDEN PAIRS
def hidden_pairs(board,cands,square_pos):
    ischanged = 0

    # ROWS
    # construct candidate table for rows
    cand_inxs = []
    for i in range(1,10):
        candx = []
        for rows in cands.index:
            use = cands.loc[rows].dropna()
            temp = []
            for cols in use.index:
                if i in use[cols]:
                    temp.append(cols)
            candx.append(temp)
        cand_inxs.append(candx) 
    
    # loop through rows to find hidden pairs
    for rows in range(9): #loop rows of candidates
    # for rows in [7]: #loop rows of candidates
        omer = {}
        for candx in range(9): #loop candidates from 1 to 9
            # print(f"number = {candx+1}, found in cols {cand_inxs[candx][rows]}")
            omer[candx+1] = cand_inxs[candx][rows]
            
        omer = pd.Series(omer)        
        omer = omer[omer.apply(lambda x: len(x)>0)]
        valco = omer.value_counts()  
        
        try:
            cols_to_remove = valco[valco==2].index.tolist()[0]
            if len(cols_to_remove) == 2:
                vals_to_remove = omer.index[omer.apply(lambda x: x != cols_to_remove)].values
                temp = cands.loc[rows][cols_to_remove]
                
                for col in temp.index:
                    temp1 = temp[col].tolist()
                    for rem in vals_to_remove:
                        try:
                            temp1.remove(rem)
                            print(f"R{rows}C{col}     Hidden Pairs (row), {rem} removed")
                            ischanged = 1
                        except:
                            pass
        
                    temp[col] = np.array(temp1)
                
                cands.loc[rows][cols_to_remove] = temp
        except:
            pass
    
    # COLUMNS
    cand_inxs = []
    for i in range(1,10):
        candx = []
        for cols in cands.columns:
            use = cands[cols].dropna()
            temp = []
            for rows in use.index:
                if i in use.loc[rows]:
                    temp.append(rows)
            candx.append(temp)
        cand_inxs.append(candx) 
    
    # loop through cols to find hidden pairs
    for cols in range(9): #loop cols of candidates
        omer = {}
        for candx in range(9): #loop candidates from 1 to 9
            omer[candx+1] = cand_inxs[candx][cols]
            
        omer = pd.Series(omer)        
        omer = omer[omer.apply(lambda x: len(x)>0)]
        valco = omer.value_counts()  
        
        try:
            rows_to_remove = valco[valco==2].index.tolist()[0]
            if len(rows_to_remove) == 2:
                vals_to_remove = omer.index[omer.apply(lambda x: x != rows_to_remove)].values
                temp = cands[cols][rows_to_remove]
                
                for row in temp.index:
                    temp1 = temp.loc[row].tolist()
                    for rem in vals_to_remove:
                        try:
                            temp1.remove(rem)
                            print(f"R{row}C{cols}     Hidden Pairs (col), {rem} removed")
                            ischanged = 1
                        except:
                            pass
        
                    temp.loc[row] = np.array(temp1)
                
                cands[cols][rows_to_remove] = temp
        except:
            pass
        
    #BOX
    for i in [[0,1,2],[3,4,5],[6,7,8]]:
        for j in [[0,1,2],[3,4,5],[6,7,8]]:
            use = cands.iloc[i,j]    
            use_flat = pd.Series(use.values.flatten()).dropna()
            temp = []
            for ix in use_flat:
                temp.extend(ix)
            valco = pd.Series(temp).value_counts()
            valco_inx = valco.index[valco == 2]
            
            omer = {}
            for valun in valco_inx:
                tempinx = []
                for rows in use.index:
                    for cols in use.columns:
                        try:
                            if valun in use.loc[rows][cols]:
                                tempinx.append([rows,cols])
                        except:
                            pass
                omer[valun] = tempinx
            
            
            #find pairs
            omer = pd.Series(omer)
            omer.sort_index(inplace=True)
            
            pairs = []
            rowcol = []
            for pair1 in omer.index:
                for pair2 in omer.index[omer.index>pair1]:
                    if omer[pair1] == omer[pair2]:
                        pairs.append([pair1,pair2])
                        rowcol.append(omer[pair1])
            
            if len(pairs):     
                #locate them in the box
                for pairvals,pairinx in zip(pairs,rowcol):
                    for inx in pairinx:
                        if cands.iloc[inx[0],inx[1]].tolist() == pairvals:
                            break
                        cands.iloc[inx[0],inx[1]] = np.array(pairvals)
                        ischanged = 1
                        print(f"R{inx[0]}C{inx[1]}     Hidden Pairs (square) {pairvals}")

    if ischanged:
        solver.solver(board,cands,square_pos) 
        
      