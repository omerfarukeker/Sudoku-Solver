# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:07:16 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver
#%% NAKED TRIPLES (squares missing)
import itertools

def naked_triples(board,cands,square_pos):
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
        solver.solver(board,cands,square_pos) 