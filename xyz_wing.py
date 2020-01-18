# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:18:16 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
from candidate_handler import candidates_update
from cells_seen import cells_seen
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver
import itertools

#%%fast starter, load data
# import pickle
# # pickle.dump([cands,board,grid,square_pos],open("for_xyz_wing2.sav","wb"))
# cands,board,grid,square_pos = pickle.load(open("for_xyz_wing2.sav","rb"))

#%% XYZ-WING
#eliminate the candidates from intersections
def xyz_wing_cand_eliminate(key,comb,cands,rem,square_pos,board):
    comb = list(comb)
    comb.remove(key)
    ischanged = 0
    
    #determine the wing cells
    for i in comb:
        if square_pos.iloc[i]==square_pos.iloc[key]:
            wing_key = i #the wing in the same box with the hinge
            comb.remove(i)
    #the other wing        
    wing2 = comb[0]
    wing_key_box = square_pos[square_pos == square_pos.iloc[wing_key]].stack().index

    seen_cells_wing_key = set(wing_key_box).intersection(cells_seen(wing2,square_pos))
    
    try:
        seen_cells_wing_key.remove(key)
        seen_cells_wing_key.remove(wing_key)
    except:
        pass
    
    for inx in seen_cells_wing_key:
        if board.iloc[inx] == ".":
            temp = cands.iloc[inx].tolist()
            try:
                temp.remove(rem)
                # cands.iloc[inx] = np.array(temp)
                cands.set_value(inx[0],inx[1],np.array(temp))
                print(f"R{inx[0]}C{inx[1]}     XYZ-Wing, removed {rem}")
                ischanged = 1
            except:
                pass  
    return ischanged,cands

def xyz_wing(board,cands,square_pos):
    ischanged = 0
    #determine the number of candidates for each cell (if else statement is necessary otherwise str.len() gives error when all column or row values are Nan)
    lenx = cands.apply(lambda x: x.str.len() if not x.isnull().all() else x)
    #find the location of bivalue and trivalue cells
    inxtwos = lenx[(lenx == 2)|(lenx == 3)].stack().index
    
    #go through triple-combinations of bivalue cells
    for comb in itertools.combinations(inxtwos, 3):
        lencounts = pd.Series([lenx.iloc[i] for i in comb]).value_counts()
        # print(comb)

        try:
            lencheck = lencounts[2] == 2 and lencounts[3] == 1
        except:
            lencheck = False
        
        if lencheck:
            temp = []
            for co in comb:
                temp.extend(cands.iloc[co])
            valco = pd.Series(temp).value_counts()
            
            #check if the combination construct a AB,BC,ABC formation
            if len(valco) == 3 and all(valco.sort_values().values == [2,2,3]):
                
                #find the hinge cell
                for i in comb:
                    if lenx.iloc[i] == 3:
                        key = i
                        
                #make sure that the hinge cell (with 3 values) sees the other 2 and in the same box with one of them
                seen_cells = cells_seen(key,square_pos)
                inters = set(seen_cells).intersection(comb)
  
                if len(inters)==3 and key:
                    key_box = square_pos[square_pos == square_pos.iloc[key]].stack().index
                    if len(set(key_box).intersection(comb)) == 2:
                        #determine the value to be removed from candidates
                        rem = valco.index[valco==3][0]
                        
                        #remove value from wing boxes
                        ischanged,cands = xyz_wing_cand_eliminate(key,comb,cands,rem,square_pos,board)
                        if ischanged:
                            solver.solver(board,cands,square_pos)           


# xyz_wing(board,cands,square_pos)
