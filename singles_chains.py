# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:22:15 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
from candidate_handler import candidates_update
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver
from cells_seen import cells_seen
import itertools

#%% Simple Colouring (Singles Chains)
# finds and returns conjugate pairs (strong links)
def conjugate_pairs(cands,board):
    # find strong links for each value
    strlinx_rows = []
    strlinx_cols = []
    strlinx_boxs = []
    for val in range(1,10):
        
        #go through all rows
        strlinx_row = []
        for row in range(9):
            use = cands.loc[row].dropna()
            temp = []
            for i in use:
                temp.extend(i)
            
            valco = pd.Series(temp).value_counts()
            try:
                if valco.loc[val] == 2:
                    inx_temp = use.apply(lambda x: val in x)
                    inx = inx_temp.index[inx_temp == True]
                    # print(f"value: {val} row: {row} strong link columns: {inx}")
                    strlinx_row.append([(row,inx[0]),(row,inx[1])])
                    
            except:
                pass
        strlinx_rows.append(strlinx_row)
    
        #go through all cols
        strlinx_col = []
        for col in range(9):
            use = cands[col].dropna()
            temp = []
            for i in use:
                temp.extend(i)
            
            valco = pd.Series(temp).value_counts()
            try:
                if valco.loc[val] == 2:
                    inx_temp = use.apply(lambda x: val in x)
                    inx = inx_temp.index[inx_temp == True]
                    # print(f"value: {val} col: {col} strong link indexes: {inx}")
                    strlinx_col.append([(inx[0],col),(inx[1],col)])
                    
            except:
                pass
        strlinx_cols.append(strlinx_col)
        
        #go through all boxes
        strlinx_box = []
        for i in [[0,1,2],[3,4,5],[6,7,8]]:
            for j in [[0,1,2],[3,4,5],[6,7,8]]:
                use_box = cands.iloc[i,j]
                use = pd.Series(use_box.values.flatten()).dropna()
                
                temp = []
                for ix in use:
                    temp.extend(ix)
                
                valco = pd.Series(temp).value_counts()
                try:
                    if valco.loc[val] == 2:
                        tempinx = []
                        for ir in use_box.index:
                            for ic in use_box.columns:
                                if board.iloc[ir,ic] == ".":
                                    if val in use_box.loc[ir][ic]:
                                        # print(f"value: {val} strong link indexes: R{ir}C{ic}")
                                        tempinx.append((ir,ic))
                        strlinx_box.append(tempinx)
                except:
                    pass
        strlinx_boxs.append(strlinx_box)
        
    return strlinx_rows,strlinx_cols,strlinx_boxs

#auxiliary function used by the recursive function
def colour_cell(boxrowcol,i,search,match_matrix,val,sl_uniq,strlinx_rows,strlinx_cols,strlinx_boxs):
    i = pd.Series(i)
    inx = i.index[i == search]
    
    try:
        pair = i[abs(inx-1)].tolist()[0]
        if len(pair) and pd.isnull(match_matrix.iloc[pair]):
            # print(f"{boxrowcol}: Connection from {search} to {pair} for {val+1}")
            
            #colour conjugate pairs with the same group but different colour
            group = match_matrix.iloc[search][1]
            colour = colours[abs(colours.index[match_matrix.iloc[search][0] == colours][0]-1)]+str(group)
            match_matrix.iloc[pair] = colour
            
            match_matrix = simple_colouring(val,pair,strlinx_rows,strlinx_cols,strlinx_boxs,sl_uniq,match_matrix)
    except:
        pass
    return match_matrix
    
#the recursive function searches for the cell
def simple_colouring(val,search,strlinx_rows,strlinx_cols,strlinx_boxs,sl_uniq,match_matrix):
    #first start searching it in the boxes
    for i in strlinx_boxs[val]:
        match_matrix = colour_cell("box",i,search,match_matrix,val,sl_uniq,strlinx_rows,strlinx_cols,strlinx_boxs)
    
    #then rows
    for i in strlinx_rows[val]:
        match_matrix = colour_cell("row",i,search,match_matrix,val,sl_uniq,strlinx_rows,strlinx_cols,strlinx_boxs)
    
    #then cols
    for i in strlinx_cols[val]:
        match_matrix = colour_cell("col",i,search,match_matrix,val,sl_uniq,strlinx_rows,strlinx_cols,strlinx_boxs)
    
    return match_matrix
    
def singles_chains_eliminate(sl_uniq,match_matrix,rem,cands,square_pos):
    ischanged = 0
    for rows in cands.index:
        for cols in cands.columns:
            use = cands.iloc[rows,cols]
            
            try:
                chk = not pd.isnull(use).all()
            except:
                chk = False
            
            #locate candidate cells for elimination
            if chk:
                if rem+1 in use:
                # if pd.isnull(match_matrix.iloc[rows,cols]) and rem+1 in use:
                    #locate all seen cells
                    seen_cells = cells_seen((rows,cols),square_pos)
                    #find intersection between seen cells and the conjugate pairs 
                    inters = list(set(seen_cells) & set(sl_uniq))
                    
                    #remove the cell of interest from the intersection cells, if any
                    try:
                        inters.remove((rows,cols))
                    except:
                        pass
                    
                    #if these cells intersect
                    if len(inters):
                        #obtain colours of the seen conjugate paris
                        inter_colours = pd.Series([match_matrix.iloc[i] for i in inters]).unique()
                        # print(f"val:{rem+1}, cell:{(rows,cols)}, intersection cells: {inters}, intersection colours: {inter_colours}")
                        
                        if len(inter_colours) == 2:
                            if inter_colours[0][1] == inter_colours[1][1] and \
                                inter_colours[0][0] != inter_colours[1][0]:
                                    temp = use.tolist()
                                    try:
                                        temp.remove(rem+1)
                                        # cands.iloc[rows,cols] = np.array(temp)
                                        cands.set_value(rows,cols,np.array(temp))
                                        print(f"R{rows}C{cols}     Singles-Chains, removed {rem+1}")
                                        ischanged = 1
                                    except:
                                        pass 
                        elif len(inter_colours) >= 3:
                            # print("Inter Len >= 3")
                            for combs in itertools.combinations(inter_colours,2):
                                # print(combs)
                                if combs[0][1] == combs[1][1] and combs[0][0] != combs[1][0]:
                                    temp = use.tolist()
                                    try:
                                        temp.remove(rem+1)
                                        # cands.iloc[rows,cols] = np.array(temp)
                                        cands.set_value(rows,cols,np.array(temp))
                                        print(f"R{rows}C{cols}     Singles-Chains, removed {rem+1}")
                                        ischanged = 1
                                    except:
                                        pass 
                            
    return ischanged,cands                       

#call single chain functions
def singles_chains(board,cands,square_pos):
    ischanged = 0

    #select the value before finding conjugate pairs
    for val in range(9):
        #find unique strong links for a value
        strlinx_rows,strlinx_cols,strlinx_boxs=conjugate_pairs(cands,board) 
        
        sl = strlinx_rows[val].copy()
        sl.extend(strlinx_cols[val])
        sl.extend(strlinx_boxs[val])
        temp = []
        for i in sl:
            temp.extend(i)
        sl_uniq = pd.Series(temp).unique()
        
        #construct empty matrix for conjugate pairs
        match_matrix = pd.DataFrame(np.full((9,9),np.nan))
        
        #start cell
        group = 0
        for init_cell in sl_uniq:
            # print(f"Start Cell: {init_cell}")
            
            if pd.isnull(match_matrix.iloc[init_cell]):
                match_matrix.iloc[init_cell] = colours[0]+str(group)
                group+=1
            
            #call recursive function
            match_matrix = simple_colouring(val,init_cell,strlinx_rows,strlinx_cols,strlinx_boxs,sl_uniq,match_matrix)   

        #call single chains elimination function
        ischanged,cands = singles_chains_eliminate(sl_uniq,match_matrix,val,cands,square_pos)
        if ischanged:
            solver.solver(board,cands,square_pos) 
     
#colours for the simple colouring strategy
colours = pd.Series(["B","R"]) 

    
    