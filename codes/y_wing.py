# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:18:16 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
from candidate_handler import candidates_update
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver
import itertools

#%% Y-WING
#find if there is a key cell in the "rectangular formation y-wing"
def find_rect_key(comb):
    #check if comb[0] is the key
    if (comb[0][0] == comb[1][0] and comb[0][1] == comb[2][1]) or (comb[0][0] == comb[2][0] and comb[0][1] == comb[1][1]):
        key = comb[0]
    #check if comb[1] is the key
    elif (comb[1][0] == comb[0][0] and comb[1][1] == comb[2][1]) or (comb[1][0] == comb[2][0] and comb[1][1] == comb[0][1]):
        key = comb[1]
    #check if comb[2] is the key
    elif (comb[2][0] == comb[0][0] and comb[2][1] == comb[1][1]) or (comb[2][0] == comb[1][0] and comb[2][1] == comb[0][1]):
        key = comb[2]
    else:
        key = False
        
    return key

#find if two cells are in the same box
def is_same_box(a,b,square_pos):
    box = False
    if square_pos.iloc[a[0],a[1]] == square_pos.iloc[b[0],b[1]]:
        # box = square_pos.iloc[a[0],a[1]]
        box = True
    return box

#find if there is a key cell in "not rectangular formation y-wing"
def find_key(comb,square_pos):
    #check if comb[0] is the key
    if (is_same_box(comb[0], comb[1],square_pos) and (comb[0][0]==comb[2][0] or comb[0][1]==comb[2][1])) or\
        (is_same_box(comb[0], comb[2],square_pos) and (comb[0][0]==comb[1][0] or comb[0][1]==comb[1][1])):
            key = comb[0]
    #check if comb[1] is the key
    elif (is_same_box(comb[1], comb[0],square_pos) and (comb[1][0]==comb[2][0] or comb[1][1]==comb[2][1])) or\
        (is_same_box(comb[1], comb[2],square_pos) and (comb[1][0]==comb[0][0] or comb[1][1]==comb[0][1])):
            key = comb[1]      
    #check if comb[2] is the key
    elif (is_same_box(comb[2], comb[0],square_pos) and (comb[2][0]==comb[1][0] or comb[2][1]==comb[1][1])) or\
        (is_same_box(comb[2], comb[1],square_pos) and (comb[2][0]==comb[0][0] or comb[2][1]==comb[0][1])):
            key = comb[2]   
    else:
        key = False
        
    return key

def y_wing_cand_eliminate(key,comb,cands,rem,isrect,square_pos,board):
    comb = list(comb)
    comb.remove(key)
    ischanged = 0
    
    if isrect:
        for inx in [(comb[0][0],comb[1][1]),(comb[1][0],comb[0][1])]:
            if inx != key and board.iloc[inx] == ".":
                temp = cands.iloc[inx].tolist()
                try:
                    temp.remove(rem)
                    cands.iloc[inx] = np.array(temp)
                    print(f"R{inx[0]}C{inx[1]}     Y-Wing, removed {rem}")
                    ischanged = 1
                except:
                    pass 
    else:
        #loop box indexes one by one
        for wing in comb:
            wing2 = comb[0] if comb[0]!=wing else comb[1]
            inx_wing = list(square_pos[square_pos == square_pos.iloc[wing]].stack().index)
            inx_wing.remove(wing)
            try:
                inx_wing.remove(key)
            except:
                pass
            
            for inx in inx_wing:
                if board.iloc[inx] == "." and (inx[0]==wing2[0] or inx[1]==wing2[1]):
                    temp = cands.iloc[inx].tolist()
                    try:
                        temp.remove(rem)
                        cands.iloc[inx] = np.array(temp)
                        print(f"R{inx[0]}C{inx[1]}     Y-Wing, removed {rem}")
                        ischanged = 1
                    except:
                        pass  
    return ischanged

def y_wing(board,cands,square_pos):
    ischanged = 0
    #determine the number of candidates for each cell
    lenx = cands.apply(lambda x: x.str.len())
    #find the location of bivalue cells
    inxtwos = lenx[lenx == 2].stack().index
    
    #go through triple-combinations of bivalue cells
    for comb in itertools.combinations(inxtwos, 3):
        temp = []
        for co in comb:
            temp.extend(cands.iloc[co])
        valco = pd.Series(temp).value_counts()
        
        #check if the combination construct a AB,BC,AC formation
        if len(valco) == 3:
            if len(valco.unique()) == 1:
                #make sure that only 2 of the 3 cells are in the same column or row
                row = pd.Series(list(map(lambda x: x[0],comb)))
                col = pd.Series(list(map(lambda x: x[1],comb)))
                if 2 in row.value_counts().values or \
                    2 in col.value_counts().values:
                    # make sure that not all of them in the same box
                    box = list(map(lambda x: square_pos.iloc[x],comb))
                    if np.diff(box).any():
                        
                        #eliminate the ones which all corners are in different boxes and does not form a rectangular formation
                        rect_key = find_rect_key(comb)
                        if not (len(pd.Series(box).unique()) == 3 and rect_key == False):
                            key = find_key(comb,square_pos)
                            
                            if rect_key:
                                for ix in list(valco.index):
                                    if not ix in cands.iloc[rect_key]:
                                        rem = ix
                                # print(f"values = {list(valco.index)}, inx = {comb}, rect_key_cell = {rect_key}, rem = {rem} Rectangular")
                                #remove value from wing boxes
                                ischanged = y_wing_cand_eliminate(rect_key,comb,cands,rem,1,square_pos,board)
                                
                            if key:
                                #determine the value to be removed from candidates
                                for ix in list(valco.index):
                                    if not ix in cands.iloc[key]:
                                        rem = ix
                                
                                #determine the key cell
                                # print(f"values = {list(valco.index)}, inx = {comb}, key_cell = {key}, rem = {rem}")
                                
                                #remove value from wing boxes
                                ischanged = y_wing_cand_eliminate(key,comb,cands,rem,0,square_pos,board)
    if ischanged:
        solver.solver(board,cands,square_pos)           
