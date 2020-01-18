# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 21:26:17 2020

@author: omerzulal
"""
import numpy as np

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