# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:10:49 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
from candidate_handler import candidates_update
from select_group import select_group
# from hidden_remove import hidden_remove
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver
import itertools
#%% HIDDEN PAIRS-TRIPLES
#find hidden pairs-triples-quads in the candidates dataframe
def hidden_pairs_triples(board,cands,square_pos):
    ischanged = 0
    
    #go through combinations (2 and 3 elements at a time)
    for pair_triple_quad in [2,3]:
        #check for rows, columns and box consecutively
        for rowcolbox in ["row","col","box"]:
            #check each groups of rows, columns or boxes
            for group_no in range(9):
                #get the group
                use = select_group(rowcolbox,cands,group_no,square_pos)
                
                #find unique values in the group
                vals = []
                for ix in use:
                    vals.extend(ix)
                vals = pd.Series(vals).unique()

                #find pair, triple combinations of the unique values
                for comb in itertools.combinations(vals, pair_triple_quad):
                    inxs = np.full(use.shape,False)
                    for com in comb:
                        inxs = (inxs) | (use.apply(lambda x: com in x))
                    
                    #if it is a pair,triple
                    if sum(inxs) == pair_triple_quad:
                        no_of_hidden = sum(inxs)
                        #determine hidden pair,triple indexes
                        hidden_inxs = inxs.index[inxs]
    
                        #remove the value from the specific cell of the candidates
                        cands,ischanged = hidden_remove(rowcolbox,group_no,hidden_inxs,comb,cands,square_pos,no_of_hidden)

                        if ischanged:
                            solver.solver(board,cands,square_pos) 
                  
#%% HIDDEN QUADS
#find hidden quads in the candidates dataframe
def hidden_quads(board,cands,square_pos):
    ischanged = 0
    
    #go through combinations (4 elements at a time)
    pair_triple_quad = 4
    #check for rows, columns and box consecutively
    for rowcolbox in ["row","col","box"]:
        #check each groups of rows, columns or boxes
        for group_no in range(9):
            #get the group
            use = select_group(rowcolbox,cands,group_no,square_pos)
            
            #find unique values in the group
            vals = []
            for ix in use:
                vals.extend(ix)
            vals = pd.Series(vals).unique()

            #find quad combinations of the unique values
            for comb in itertools.combinations(vals, pair_triple_quad):
                inxs = np.full(use.shape,False)
                for com in comb:
                    inxs = (inxs) | (use.apply(lambda x: com in x))
                
                #if it is a quad
                if sum(inxs) == pair_triple_quad:
                    no_of_hidden = sum(inxs)
                    #determine hidden quad indexes
                    hidden_inxs = inxs.index[inxs]

                    #remove the value from the specific cell of the candidates
                    cands,ischanged = hidden_remove(rowcolbox,group_no,hidden_inxs,comb,cands,square_pos,no_of_hidden)

                    if ischanged:
                        solver.solver(board,cands,square_pos) 

#removes values except hidden pairs, triples or quads from a group (row col or box)
#it is different than "naked_remove" function 
def hidden_remove(rowcolbox,group_no,hidden_inxs,comb,cands,square_pos,no_of_hidden):
    pairtriplequad = {2:"Pair",3:"Triple",4:"Quad"}
    ischanged = 0
    for cells in hidden_inxs:
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
            print(f"R{row:<1}C{col:<1}     Hidden {pairtriplequad[no_of_hidden]:>7}s ({rowcolbox:<3}), {str(removed_vals):<15} removed, {pairtriplequad[no_of_hidden]:>7}s: {str(comb):>6}")
            ischanged = 1
            
    return cands,ischanged