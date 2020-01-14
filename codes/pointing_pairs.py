# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:12:25 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
from candidate_handler import candidates_update
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver

#%% POINTING PAIRS
def pointing_pairs(board,cands,square_pos):
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
                                # solver.solver(board,cands,square_pos)
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
                                # solver.solver(board,cands,square_pos)
                            except:
                                pass
                except:
                    pass
                    
    if ischanged:
        solver.solver(board,cands,square_pos)   
