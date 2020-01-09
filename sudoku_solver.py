# -*- coding: utf-8 -*-
"""
SUDOKU SOLVER V15
- simple colouring enhancements in the algorithm
- terminates when the board is complete (faster)
- candidate updates function is enhanced
@author: omerzulal
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import time
import sys
         
            
#%% validation check functions
def row_check(board,isprint=False):
    check = True
    for row in range(9):
        a = board.iloc[row,:].value_counts()
        try:
            a = a.drop(".")
        except:
            pass
        
        check = check and not any(a>1)
     
    if isprint:
        if check:
            print("Row Check: Passed")
        else:
            print("Row Check: Failed")
        
    return check

def col_check(board,isprint=False):
    check = True
    for col in  range(9):
        a = board.iloc[:,col].value_counts()
        try:
            a = a.drop(".")
        except:
            pass
        
        check = check and not any(a>1)
    
    if isprint:
        if check:
            print("Column Check: Passed")
        else:
            print("Column Check: Failed")
        
    return check

def square_check(board,isprint=False):
    check = True
    for i in [[0,1,2],[3,4,5],[6,7,8]]:
        for j in [[0,1,2],[3,4,5],[6,7,8]]:
            a = pd.Series(board.iloc[i,j].values.flatten()).value_counts()
            try:
                a = a.drop(".")
            except:
                pass
        
        check = check and not any(a>1)
        
    if isprint:     
        if check:
            print("Square Check: Passed")
        else:
            print("Square Check: Failed")
        
    return check

def check_valid():
    rcheck = row_check(board)
    ccheck = col_check(board)
    cucheck = square_check(board)
    
    return rcheck and ccheck and cucheck

#%% PRINT THE SUDOKU BOARD
#print the board
def print_board(board):
    boardprint = board.copy()
    boardprint.columns = range(1,10)
    boardprint.index = ["A","B","C","D","E","F","G","H","I"]
    # sns.heatmap(board,annot=True,linecolor="k")
    print(boardprint)
    
#%% INITIALISE CANDIDATES
def candidates(board):
    # board_copy = board.copy()
    cands = pd.DataFrame(np.full((9,9),np.nan))
    for row in range(9):
        for col in range(9):
            temp = []
            if board.iloc[row,col] == ".":
                temp.extend(board.iloc[row,:])
                temp.extend(board.iloc[:,col])
                temp.extend(board.loc[board.index[row]][board.columns[col]].values.flatten())
                temp = pd.Series(temp)
                drops = temp[temp!="."].unique()
                cand = pd.Series(np.arange(1,10),index=np.arange(1,10)).drop(drops).values.astype("O")
                
                #this part is for handling the "ValueError: setting an array element as a sequence"
                if len(cand) == 1:
                    if cand%1 == 0.0:
                        temp = cand.tolist()
                        temp.append(99)
                        cands[col][row] = np.array(temp).astype("O")
                        temp.remove(99)
                        cands[col][row] = np.array(temp).astype("O")
                else:
                    cands[col][row] = cand

    return cands

#%% UPDATE CANDIDATES
def candidates_update(cands,row,col,val):
    #remove the value from candidate matrix first
    cands.iloc[row,col] = np.nan
    
    #locate the cells seen by the key cell
    seen_cells = cells_seen((row,col))
    
    #remove the value from the seen cells
    for i in seen_cells:
        try:
            if val in cands.iloc[i]:
                cands.loc[i[0]][i[1]] = np.delete(cands.iloc[i],np.where(cands.iloc[i]==val))
        except:
            pass
    
    return cands

#%% SINGLE CANDIDATES
def single_cand(board,cands):
    ischanged = 0
    for row in range(9):
        for col in range(9):
            if board.iloc[row,col] == ".":
                cand = cands.iloc[row,col]
                # cand = int(cands.iloc[row,col][0])
                try:
                    lenx = len(cand)
                    if lenx == 1:
                        ischanged = 1
                        print(f"R{row+1}C{col+1}={cand[0]} : Single Candidate")
                        board.iloc[row,col] = cand[0]
                        cands = candidates_update(cands,row,col,cand[0])
                except:
                    ischanged = 1
                    print(f"R{row+1}C{col+1}={cand} : Single Candidate (except)")
                    board.iloc[row,col] = cand
                    cands = candidates_update(cands,row,col,cand)
    if ischanged:
        solver(board,cands)               
    

#%% HIDDEN SINGLES
def hidden_singles(board,cands):
    is_changed = 0
    #check rows
    for row in range(9):
        temp = []
        for col in range(9):
            if board.iloc[row,col] == ".":
                temp.extend(cands.iloc[row,col])
        valco = pd.Series(temp).value_counts()
        for valun in valco.index[valco == 1].values: #????? there can be 1 and only 1 single candidate in a row..
            temp1 = cands.loc[row].dropna().apply(lambda x: valun in x)
            inx = temp1.index[temp1 == True]
            if len(inx):
                is_changed = 1
                for inxt in inx:
                    print(f"R{row+1}C{inxt+1}={valun} : Hidden Singles (row)")
                    board.iloc[row,inxt] = valun
                    cands = candidates_update(cands,row,inxt,valun)
    
    #check columns
    for col in range(9):
        temp = []
        for row in range(9):
            if board.iloc[row,col] == ".":
                temp.extend(cands.iloc[row,col])
        valco = pd.Series(temp).value_counts()
        for valun in valco.index[valco == 1].values:
            temp1 = cands.iloc[:,col].dropna().apply(lambda x: valun in x)
            inx = temp1.index[temp1 == True]
            if len(inx):
                is_changed = 1
                for inxt in inx:
                    print(f"R{inxt+1}C{col+1}={valun} : Hidden Singles (col)")
                    board.iloc[inxt,col] = valun
                    cands = candidates_update(cands,inxt,col,valun)        

    #check squares
    for i in [[0,1,2],[3,4,5],[6,7,8]]:
        for j in [[0,1,2],[3,4,5],[6,7,8]]:
            a = cands.iloc[i,j]
            a_flat = pd.Series(a.values.flatten()).dropna()
            temp = []
            for ix in a_flat: 
                temp.extend(ix)
            valco = pd.Series(temp).value_counts()
            
            if any(valco == 1):
                to_change_all = valco.index[valco == 1].values
                for to_change in to_change_all: #loop all values to be changed (sometimes multiple changes needed in a single box)
                    for rowx in a.index:
                        for colx in a.columns:
                            try: 
                                if board.iloc[rowx,colx] == ".":
                                    if to_change in a.loc[rowx][colx]:
                                        print(f"R{rowx+1}C{colx+1}={to_change} : Hidden Singles (square)")
                                        board.iloc[rowx,colx] = to_change
                                        cands = candidates_update(cands,rowx,colx,to_change)
                                        is_changed = 1
                            except:
                                print("except")
    if is_changed:
        solver(board,cands)                       
    

#%% HIDDEN PAIRS
def hidden_pairs(board,cands):
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
        solver(board,cands)
        
      

#%% HIDDEN TRIPLES (squares is missing)
    
def hidden_triples(board,cands):
    ischanged = 0
    
    # ROWS
    for rows in range(9):
        use = cands.loc[rows].dropna()
        vals = []
        for ix in use:
            vals.extend(ix)
        vals = pd.Series(vals).unique()
        #go through combinations (3 elements at a time)
        for comb in itertools.combinations(vals, 3):
            inxs = (use.apply(lambda x: comb[0] in x)) | (use.apply(lambda x: comb[1] in x)) | (use.apply(lambda x: comb[2] in x))
            if sum(inxs) == 3:
                #determine hidden triple indexes
                triple_inx = inxs.index[inxs]
                
                #remove values other than the triple
                for colx in triple_inx: #go through column indexes
                    temp = cands.loc[rows][colx].tolist()
                    val_to_remove = set(comb).symmetric_difference(temp)
                    for rem in val_to_remove:
                        try:
                            temp.remove(rem)
                            print(f"R{rows}C{colx}     Hidden Triple (rows), {rem} removed, Triple: {comb}")
                            ischanged = 1
                        except:
                            pass
                    cands.loc[rows][colx] = np.array(temp)
                    
    # COLUMNS
    for col in range(9):
        use = cands[col].dropna()
        vals = []
        for ix in use:
            vals.extend(ix)
        vals = pd.Series(vals).unique()
        #go through combinations (3 elements at a time)
        for comb in itertools.combinations(vals, 3):
            inxs = (use.apply(lambda x: comb[0] in x)) | (use.apply(lambda x: comb[1] in x)) | (use.apply(lambda x: comb[2] in x))
            if sum(inxs) == 3:
                #determine hidden triple indexes
                triple_inx = inxs.index[inxs]
                
                #remove values other than the triple
                for rowx in triple_inx:
                    temp = cands[col][rowx].tolist()
                    val_to_remove = set(comb).symmetric_difference(temp)
                    for rem in val_to_remove:
                        try:
                            temp.remove(rem)
                            print(f"R{rowx}C{col}     Hidden Triple (cols), {rem} removed, Triple: {comb}")
                            ischanged = 1
                        except:
                            pass
                    cands[col][rowx] = np.array(temp)

    if ischanged:
        solver(board,cands)    
     

#%% NAKED PAIRS
def naked_pairs(board,cands):
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
        solver(board,cands)
        
    

#%% NAKED TRIPLES (squares missing)
import itertools

def naked_triples(board,cands):
    ischanged = 0
    
    #rows
    for row in range(9):
        use = cands.loc[row].dropna()
        
        #go through combinations (3 elements at a time)
        for comb in itertools.combinations(use, 3):
            comb = [i.tolist() for i in comb]
            temp = []
            for i in comb:
                temp.extend(i)
            naked_triple = pd.Series(temp).unique()
            if len(naked_triple) == 3:

                #remove naked triple elements from the rest of the row
                for j in use.index:
                    try:
                        used = use[j].tolist()
                        if not used in comb:
                            temp1 = used
                            for nt in naked_triple:
                                try:
                                    temp1.remove(nt)
                                    use[j] = np.array(temp1)
                                    print(f"R{row}C{j}     Naked Triple (rows), {nt} removed, Triple: {naked_triple}")
                                    ischanged = 1
                                except:
                                    pass
                    except:
                        pass
                        
                cands.loc[row] = use 

    #cols
    for col in range(9):
        use = cands[col].dropna()
        
        #go through combinations (3 elements at a time)
        for comb in itertools.combinations(use, 3):
            comb = [i.tolist() for i in comb]
            temp = []
            for i in comb:
                temp.extend(i)
            naked_triple = pd.Series(temp).unique()
            if len(naked_triple) == 3:

                #remove naked triple elements from the rest of the column
                for j in use.index:
                    try:
                        used = use[j].tolist()
                        if not used in comb:
                            temp1 = used
                            for nt in naked_triple:
                                try:
                                    temp1.remove(nt)
                                    use[j] = np.array(temp1)
                                    print(f"R{j}C{col}     Naked Triple (columns), {nt} removed, Triple: {naked_triple}")
                                    # print(f"Column{col} Naked triples removed {nt}, {comb}")
                                    ischanged = 1
                                except:
                                    pass
                    except:
                        pass
                        
                cands[col] = use 
                
    if ischanged:
        solver(board,cands)

#%% POINTING PAIRS
def pointing_pairs(board,cands):
    # print("Pointing Pairs")
    ischanged = 0
    
    for i in [[0,1,2],[3,4,5],[6,7,8]]:
        for j in [[0,1,2],[3,4,5],[6,7,8]]:
            use = cands.iloc[i,j]
            use_flat = pd.Series(use.values.flatten()).dropna()
            
            temp = []
            for ix in use_flat:
                temp.extend(ix)
            
            valco = pd.Series(temp).value_counts()
            # try:
            pair_vals = valco.index[(valco == 2) | (valco == 3)]
            
            for pair_val in pair_vals:
                pointrows, pointcols = [],[]
                for ii in use.index:
                    for jj in use.columns:
                        try:
                            if pair_val in use.loc[ii][jj].tolist():
                                pointrows.extend([ii])
                                pointcols.extend([jj])
                        except:
                            pass
                        
                #pairs point in the column direction
                try:
                    if not any(np.diff(pointcols)):
                        change_col = cands[pointcols[0]].dropna().drop(pointrows)
                        for rows in change_col.index:
                            temp = change_col[rows].tolist()
                            try:
                                temp.remove(pair_val)
                                cands.iloc[rows,pointcols[0]] = np.array(temp)
                                print(f"R{rows}C{pointcols[0]}     Pointing Pairs (cols), {pair_val} removed")
                                ischanged = 1
                            except:
                                pass
                except:
                    pass
                    
                #pairs point in the row direction
                try:
                    if not any(np.diff(pointrows)):
                        change_col = cands.loc[pointrows[0]].dropna().drop(pointcols)
                        for cols in change_col.index:
                            temp = change_col[cols].tolist()
                            try:
                                temp.remove(pair_val)
                                cands.iloc[pointrows[0],cols] = np.array(temp)
                                print(f"R{pointrows[0]}C{cols}     Pointing Pairs (rows), {pair_val} removed")
                                ischanged = 1
                            except:
                                pass
                except:
                    pass
                    
    if ischanged:
        solver(board,cands)  

    

#%% BOX/LINE REDUCTION

def box_line(board,cands):
    ischanged = 0
    
    #rows
    for rows in range(9):
        use = cands.loc[rows].dropna()
        for val in range(1,10):
            inxs = use.apply(lambda x: val in x)
            if len(inxs) == 0:
                break
            inxs = list(inxs.index[inxs])
            
            #find locations of the box/line reduction candidates
            if len(inxs) == 2 or len(inxs) == 3:
                board_pos = square_pos.loc[rows][inxs]
                if np.diff(board_pos).sum() == 0:
                    square = board_pos.iloc[0]
                    inx = pd.Series(square_pos[square_pos == square].stack().index.tolist())
                    
                    #go through the square cells except the box/line
                    for ix in inx:
                        if ix[0] != rows:
                        # if ix != (rows,board_pos.index[0]) and ix != (rows,board_pos.index[1]) and ix != (rows,board_pos.index[2]):
                            try:
                                temp = cands.iloc[ix].tolist()
                                temp.remove(val)
                                cands.iloc[ix] = np.array(temp)
                                ischanged = 1
                                print(f"R{ix[0]}C{ix[1]}     Box/Line (row) reduction value {val} removed")
                            except:
                                pass
        
        #columns
        for cols in range(9):
            use = cands[cols].dropna()
            for val in range(1,10):
                inxs = use.apply(lambda x: val in x)
                if len(inxs) == 0:
                    break
                inxs = list(inxs.index[inxs])
                
                #find locations of the box/line reduction candidates
                if len(inxs) == 2 or len(inxs) == 3:
                    board_pos = square_pos[cols][inxs]
                    if np.diff(board_pos).sum() == 0:
                        square = board_pos.iloc[0]
                        inx = pd.Series(square_pos[square_pos == square].stack().index.tolist())
                        
                        #go through the square cells except the box/line
                        for ix in inx:
                            if ix[1] != cols:
                            # if ix != (board_pos.index[0],cols) and ix != (board_pos.index[1],cols):
                                try:
                                    temp = cands.iloc[ix].tolist()
                                    temp.remove(val)
                                    cands.iloc[ix] = np.array(temp)
                                    ischanged = 1
                                    print(f"R{ix[0]}C{ix[1]}     Box/Line (col) reduction value {val} removed")
                                except:
                                    pass
        
        
    if ischanged:
        solver(board,cands)  
            
#%% X-WING  
def x_wing(board,cands):
    #check xwings for both rows and columns
    for rowcol in ["rows","cols"]:
        if rowcol == "cols":
            cands = cands.T
        ischanged = 0
        #construct candidate table
        wings = []
        for i in range(1,10):
            wing = []
            for rows in cands.index:
                use = cands.loc[rows].dropna()
                temp = []
                for cols in use.index:
                    if i in use[cols]:
                        temp.append(cols)
                wing.append(temp)
            wings.append(wing)      
        
        #loop through the candidates and eliminate
        for wing in range(len(wings)):
            # print(wings[wing])
            for i in range(9):
                for j in range(i+1,9):
                    if (len(wings[wing][i]) == 2) & (len(wings[wing][j]) == 2):
                        # print(f"pair_r{i}c{j}")
                        if wings[wing][i] == wings[wing][j]:
                            #remove candidates in the columns
                            for rem in wings[wing][i]:
                                use = cands[rem].dropna()
                                for ix in use.index:
                                    if not((ix == i) | (ix == j)):
                                        temp = use[ix].tolist()
                                        try:
                                            temp.remove(wing+1)
                                            print(f"R{ix}C{rem}     X-Wing, removed {wing+1} from {rowcol}")
                                            ischanged = 1
                                        except:
                                            pass
                                        use[ix] = np.array(temp)
                                cands[rem] = use
    cands = cands.T
    if ischanged:
        solver(board,cands)           

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
def is_same_box(a,b):
    box = False
    if square_pos.iloc[a[0],a[1]] == square_pos.iloc[b[0],b[1]]:
        # box = square_pos.iloc[a[0],a[1]]
        box = True
    return box

#find if there is a key cell in "not rectangular formation y-wing"
def find_key(comb):
    #check if comb[0] is the key
    if (is_same_box(comb[0], comb[1]) and (comb[0][0]==comb[2][0] or comb[0][1]==comb[2][1])) or\
        (is_same_box(comb[0], comb[2]) and (comb[0][0]==comb[1][0] or comb[0][1]==comb[1][1])):
            key = comb[0]
    #check if comb[1] is the key
    elif (is_same_box(comb[1], comb[0]) and (comb[1][0]==comb[2][0] or comb[1][1]==comb[2][1])) or\
        (is_same_box(comb[1], comb[2]) and (comb[1][0]==comb[0][0] or comb[1][1]==comb[0][1])):
            key = comb[1]      
    #check if comb[2] is the key
    elif (is_same_box(comb[2], comb[0]) and (comb[2][0]==comb[1][0] or comb[2][1]==comb[1][1])) or\
        (is_same_box(comb[2], comb[1]) and (comb[2][0]==comb[0][0] or comb[2][1]==comb[0][1])):
            key = comb[2]   
    else:
        key = False
        
    return key

def y_wing_cand_eliminate(key,comb,cands,rem,isrect):
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

def y_wing(board,cands):
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
                            key = find_key(comb)
                            
                            if rect_key:
                                for ix in list(valco.index):
                                    if not ix in cands.iloc[rect_key]:
                                        rem = ix
                                # print(f"values = {list(valco.index)}, inx = {comb}, rect_key_cell = {rect_key}, rem = {rem} Rectangular")
                                #remove value from wing boxes
                                ischanged = y_wing_cand_eliminate(rect_key,comb,cands,rem,1)
                                
                            if key:
                                #determine the value to be removed from candidates
                                for ix in list(valco.index):
                                    if not ix in cands.iloc[key]:
                                        rem = ix
                                
                                #determine the key cell
                                # print(f"values = {list(valco.index)}, inx = {comb}, key_cell = {key}, rem = {rem}")
                                
                                #remove value from wing boxes
                                ischanged = y_wing_cand_eliminate(key,comb,cands,rem,0)
    if ischanged:
        solver(board,cands)         

#%% Simple Colouring (Singles Chains)
# finds and returns conjugate pairs (strong links)
def conjugate_pairs():
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

def cells_seen(inx):
    cells = []
    #box
    cells.extend(square_pos[square_pos == square_pos.iloc[inx]].stack().index)
    #rows
    cells.extend(square_pos.iloc[[inx[0]],:].stack().index)
    #cols
    cells.extend(square_pos.iloc[:,[inx[1]]].stack().index)
    cells = pd.Series(cells).unique()
    return cells
    

def singles_chains_eliminate(sl_uniq,match_matrix,rem):
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
                    seen_cells = cells_seen((rows,cols))
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
                                        cands.iloc[rows,cols] = np.array(temp)
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
                                        cands.iloc[rows,cols] = np.array(temp)
                                        print(f"R{rows}C{cols}     Singles-Chains, removed {rem+1}")
                                        ischanged = 1
                                    except:
                                        pass 
                            
    return ischanged                       

#call single chain functions
def singles_chains(board,cands):
    ischanged = 0
    
    #find unique strong links for a value
    strlinx_rows,strlinx_cols,strlinx_boxs=conjugate_pairs() 

    #select the value before finding conjugate pairs
    for val in range(9):
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
        for group,init_cell in enumerate(sl_uniq):
            # print(f"Start Cell: {init_cell}")
            
            if pd.isnull(match_matrix.iloc[init_cell]):
                match_matrix.iloc[init_cell] = colours[0]+str(group)
            
            #call recursive function
            match_matrix = simple_colouring(val,init_cell,strlinx_rows,strlinx_cols,strlinx_boxs,sl_uniq,match_matrix)   

        #call single chains elimination function
        ischanged = singles_chains_eliminate(sl_uniq,match_matrix,val)
        if ischanged:
            # print("changed")
            solver(board,cands)
     
#colours for the simple colouring strategy
colours = pd.Series(["B","R"]) 
#%% SOLVER FUNCTION
def solver(board,cands):
    if (board==".").any().any():
        single_cand(board,cands)
        hidden_singles(board,cands)
        naked_pairs(board,cands)
        hidden_pairs(board,cands)
        naked_triples(board,cands)
        hidden_triples(board,cands)
        pointing_pairs(board,cands)
        box_line(board,cands)
        x_wing(board,cands)
        y_wing(board,cands)
        singles_chains(board,cands)
    else:
        print("COMPLETE!!!!!")
        # break
        sys.exit(0)
    
    
    

#%% Alternative grids from the internet

# grids from Andrew Stuart's website
#(SOLVED)
# grid = "000004028406000005100030600000301000087000140000709000002010003900000507670400000"
#(SOLVED) moderate in Andrew Stuart website, naked triple
# grid = "720096003000205000080004020000000060106503807040000000030800090000702000200430018"
# (SOLVED) board for naked pairs, Y-wing
# grid = "309000400200709000087000000750060230600904008028050041000000590000106007006000104"
# board for pointing pairs, simple colouring, ***NEEDS*** XYZ wing
# grid = "000704005020010070000080002090006250600070008053200010400090000030060090200407000"
# (SOLVED) board for xwing example, y-wing, simple colouring
# grid = "093004560060003140004608309981345000347286951652070483406002890000400010029800034"
# (SOLVED) board for hidden triple 
# grid="300000000970010000600583000200000900500621003008000005000435002000090056000000001"
# (SOLVED) board for box/line reduction, simple coloring
# grid="000921003009000060000000500080403006007000800500700040003000000020000700800195000"
# (SOLVED) board for Y-wing (multiply y-wings at different locations)
# grid = "900240000050690231020050090090700320002935607070002900069020073510079062207086009"
# (SOLVED) simple coloring
# grid = "007083600039706800826419753640190387080367000073048060390870026764900138208630970"
# simple coloring, ***NEEDS*** x-cycles
# grid = "200041006400602010016090004300129640142060590069504001584216379920408165601900482"
# (SOLVED) simple coloring
# grid = "062900000004308000709000400600801000003000200000207003001000904000709300000004120"
# (SOLVED) simple coloring
# grid = "000000070000090810500203004800020000045000720000000003400308006072010000030000000"
# (SOLVED) simple coloring
# grid = "090200350012003000300008000000017000630000089000930000000700002000300190078009030"
# (SOLVED) simple coloring
grid = "400800003006010409000005000010060092000301000640050080000600000907080100800009004"
# sadfasdf
# grid = "016007803090800000870001260048000300650009082039000650060900020080002936924600510"


# # grids from github
# # https://github.com/sok63/sudoku-1/blob/master/sample/p096_sudoku.txt
# Grid 01 Simple colouring, ***NEEDS*** x-cycles
# grid = "200000006000602000010090004300009600040000090009500001500010370000408000600000002"
# Grid 02 (3D medusa needed)
# grid = "000050000300284000010000408086003200400000009005700140507000030000637001000020000"
# (SOLVED) Grid 03 
# grid = "000000907000420180000705026100904000050000040000507009920108000034059000507000000"
# (SOLVED) Grid 05
# grid = "020810740700003100090002805009040087400208003160030200302700060005600008076051090"
# (SOLVED) Grid 06 
# grid = "840000000000000000000905001200380040000000005000000000300000820009501000000700000"
# (SOLVED) Grid 07, Y Wing
# grid = "007000400060070030090203000005047609000000000908130200000705080070020090001000500"
# (SOLVED) Grid 26 
# grid = "500400060009000800640020000000001008208000501700500000000090084003000600060003002"
# (SOLVED) Grid 48 
# grid = "001007090590080001030000080000005800050060020004100000080000030100020079020700400"

#cracking the cryptic LGFL83r67M X-wing, ***NEEDS*** hidden quads
# grid = "000000010210003480039800200060304900000000000001607040008002170026700098090000000"
#cracking the cryptic mgp6LprDM8, simple colouring, ***NEEDS*** swordfish
# grid = "800000100010790560007108040570020400008010795103050080701003006000000010002001900"
# (SOLVED) cracking the cryptic 3gLbRPQ42d 
# grid = "000000700000001080300020004090002060005000800080700050200070003060500000003000000"
#cracking the cryptic JDFGD8p2m3 ***NEEDS***  diabolic strategies
# grid = "800000300040001000200470000400000000010002070003090005000685000008000120000009003"   
# (SOLVED) cracking the cryptic RRf6bgb9GG
# grid = "609102080000000400502000000000020304100005000020000506000801000000000009805907040"   
#cracking the cryptic BHBjPFJJP4 ***NEEDS*** swordfish
# grid = "040300600001002090000000000000000000030600900007001020060400300700000008002007010"   


# from my sudoku book (needs XYZ wing, XY chain, WXYZ wing)
# grid = "410005000200401008800000103008000070070106050020000800302000005100904007000300086"

#use following to convert board tables to single line string:
# grid = np.array2string(board.replace(".",0).values.flatten()).translate({ord(i): None for i in "[]\n "})

#%% user interface for console
uinput = input("Enter the board in 81 digit format where empty cells are filled with zeros: ")
if len(uinput) == 81:
    grid = uinput
elif len(uinput) == 0:
    pass
else:
    print(f"Incorrect Sudoku Board (Entered {len(uinput)} digits only!)")
#%% construct the board from 81 digit grid string
def init_board(grid):
    board = []
    
    for i in range(81):
        board.append(int(grid[i]))
    
    board = pd.Series(board).replace(0,".")
    board = pd.DataFrame(board.values.reshape((9,9)))
    
    board.index = ["A","A","A","B","B","B","C","C","C"]
    board.columns = ["A","A","A","B","B","B","C","C","C"]
    
    #helps finding the boxes when (row,col) pair is known
    square_pos = pd.DataFrame([ [1,1,1,2,2,2,3,3,3],
                                [1,1,1,2,2,2,3,3,3],
                                [1,1,1,2,2,2,3,3,3],
                                [4,4,4,5,5,5,6,6,6],
                                [4,4,4,5,5,5,6,6,6],
                                [4,4,4,5,5,5,6,6,6],
                                [7,7,7,8,8,8,9,9,9],
                                [7,7,7,8,8,8,9,9,9],
                                [7,7,7,8,8,8,9,9,9]])
    return board,square_pos

#%% RUN THE SOLVER       
t1 = time.time()
board,square_pos = init_board(grid)
print_board(board)

#check validity before solving it
if check_valid():
    cands = candidates(board)
    solver(board,cands)
else:
    print("The board is not valid!")
   
#check validity after solving it
if check_valid():
    print(f"Solving took {round(time.time()-t1,2)} seconds")
    board.index = np.arange(1,10)
    board.columns = np.arange(1,10)
    print_board(board)
    print(f"{(board == '.').sum().sum()} Missing Elements Left in The Board!")
    
                
   