# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 00:37:37 2020

@author: omerzulal
"""

import numpy as np

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
            cands.iloc[row,col] = np.array(list(set(cands.iloc[row,col]).difference(set(comb))))
            print(f"R{row:<1}C{col:<1}     Naked {pairtriplequad[no_of_nakeds]:>7}s ({rowcolbox:<3}), {str(removed_vals):<15} removed, {pairtriplequad[no_of_nakeds]:>7}s: {str(comb):>6}")
            ischanged = 1
            
    return cands,ischanged