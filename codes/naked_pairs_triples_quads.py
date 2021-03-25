# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:10:49 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
from candidate_handler import candidates_update
from select_group import select_group
# from naked_remove import naked_remove
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver
import itertools
#%% NAKED PAIRS-TRIPLES
#find naked pairs-triples-quads in the candidates dataframe
def naked_pairs_triples(board,cands,square_pos):
    ischanged = 0
    
    #go through combinations (2,3 and 4 elements at a time)
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
                for comb in itertools.combinations(use, pair_triple_quad):
                    comb = [i.tolist() for i in comb]
                    temp = []
                    for i in comb:
                        temp.extend(i)
                    naked_values = pd.Series(temp).unique()
                    
                    if len(naked_values) == pair_triple_quad:
                        # #determine naked pair,triple indexes
                        naked_inxs = use.apply(lambda x: len(set(x).difference(naked_values))!=0)
                        naked_inxs = naked_inxs.index[naked_inxs]
                        # print(naked_inxs)
                        # print("here")
                        
                        #if there are cells to remove naked pairs,triples
                        if len(naked_inxs):
                            # #removes pairs, triples values from the other cells for a group (row col or box)
                            cands,ischanged = naked_remove(rowcolbox,group_no,naked_inxs,naked_values,cands,square_pos,pair_triple_quad)

                        if ischanged:
                            solver.solver(board,cands,square_pos)    
                            
                            
#%% NAKED QUADS
#find naked quads in the candidates dataframe
def naked_quads(board,cands,square_pos):
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
            for comb in itertools.combinations(use, pair_triple_quad):
                comb = [i.tolist() for i in comb]
                temp = []
                for i in comb:
                    temp.extend(i)
                naked_values = pd.Series(temp).unique()
                
                if len(naked_values) == pair_triple_quad:
                    # #determine naked quad indexes
                    naked_inxs = use.apply(lambda x: len(set(x).difference(naked_values))!=0)
                    naked_inxs = naked_inxs.index[naked_inxs]
                    # print(naked_inxs)
                    # print("here")
                    
                    #if there are cells to remove naked quads
                    if len(naked_inxs):
                        # #removes quads values from the other cells for a group (row col or box)
                        cands,ischanged = naked_remove(rowcolbox,group_no,naked_inxs,naked_values,cands,square_pos,pair_triple_quad)

                    if ischanged:
                        solver.solver(board,cands,square_pos)    

#removes pairs, triples or quads values from the other cells for a group (row col or box)
#it is different than "hidden_remove" function 
def naked_remove(rowcolbox,group_no,naked_inxs,comb,cands,square_pos,no_of_nakeds):
    pairtriplequad = {2:"Pair",3:"Triple",4:"Quad"}
    ischanged = 0
    for cells in naked_inxs:
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
        removed_vals = set(comb)&set(cands.iloc[row,col])
        
        #replace values in the cell with the intersection of combination and the cell
        if len(removed_vals):
            # cands.iloc[row,col] = np.array(list(set(comb)&set(cands.iloc[row,col])))
            # cands.iloc[row,col] = np.array(list(set(cands.iloc[row,col]).difference(set(comb))))
            # cands.loc[row][col] = np.array(list(set(cands.iloc[row,col]).difference(set(comb))))
            # cands.set_value(row,col,np.array(list(set(cands.iloc[row,col]).difference(set(comb)))))
            cands.at[row,col] = np.array(list(set(cands.iloc[row,col]).difference(set(comb))))
            print(f"R{row:<1}C{col:<1}     Naked {pairtriplequad[no_of_nakeds]:>7}s ({rowcolbox:<3}), {str(removed_vals):<15} removed, {pairtriplequad[no_of_nakeds]:>7}s: {str(comb):>6}")
            ischanged = 1
            
    return cands,ischanged     