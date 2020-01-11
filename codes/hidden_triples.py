# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:10:49 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
from candidate_handler import candidates_update
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver
import itertools
#%% HIDDEN TRIPLES

#selects the group (row col or box)
def select_group(rowcolbox,cands,group_no,square_pos):
    if rowcolbox == "row":
        use = cands.loc[group_no].dropna()
    elif rowcolbox == "col":
        use = cands[group_no].dropna()
    elif rowcolbox == "box":
        inx = square_pos[square_pos==group_no+1].stack().index
        use = pd.Series([cands.iloc[i] for i in inx]).dropna()
    return use

#removes a value from a group (row col or box)
def remove_value(rowcolbox,group_no,triple_inx,comb,cands,square_pos):
    for cells in triple_inx:
        if rowcolbox == "row":
            row = group_no
            col = cells
        elif rowcolbox == "col":
            row = cells
            col = group_no
        elif rowcolbox == "box":
            box_inx = square_pos[square_pos==group_no+1].stack().index
            row = box_inx[cells][0]
            col = box_inx[cells][1]
        
        #following line is for printing purposes only
        removed_vals = set(cands.iloc[row,col]).difference(set(comb))
        
        #replace values in the cell with the intersection of combination and the cell
        if len(removed_vals):
            cands.iloc[row,col] = np.array(list(set(comb)&set(cands.iloc[row,col])))
            print(f"R{row}C{col}     Hidden Triples ({rowcolbox}), {removed_vals} removed, Triple: {comb}")
            
    return cands

#find hidden triples in the candidates dataframe
def hidden_triples(board,cands,square_pos):
    ischanged = 0
    
    #for all
    for rowcolbox in ["row","col","box"]:
        for group_no in range(9):
            use = select_group(rowcolbox,cands,group_no,square_pos)

            vals = []
            for ix in use:
                vals.extend(ix)
            vals = pd.Series(vals).unique()
            #go through combinations (3 elements at a time)
            for comb in itertools.combinations(vals, 3):
                inxs = (use.apply(lambda x: comb[0] in x)) | (use.apply(lambda x: comb[1] in x)) | (use.apply(lambda x: comb[2] in x))
                
                #if it is a triple
                if sum(inxs) == 3:
                    #determine hidden triple indexes
                    triple_inx = inxs.index[inxs]

                    #remove the value from the specific cell of the candidates
                    cands = remove_value(rowcolbox,group_no,triple_inx,comb,cands,square_pos)

    if ischanged:
        solver.solver(board,cands,square_pos)    
     