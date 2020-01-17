# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 10:10:49 2020

@author: omer.eker
"""
import numpy as np
import pandas as pd
from candidate_handler import candidates_update
from select_group import select_group
from hidden_remove import hidden_remove
#interdependent modules, it has to be imported like below,otherwise it wont work
import solver as solver
import itertools
#%% HIDDEN TRIPLES
#find hidden triples in the candidates dataframe
def hidden_triples(board,cands,square_pos):
    ischanged = 0
    
    #for all
    for rowcolbox in ["row","col","box"]:
        for group_no in range(9):
            use = select_group(rowcolbox,cands,group_no,square_pos)

            vals = []
            for ix in use:
                vals.extend(ix)
            vals = pd.Series(vals).unique()
            #go through combinations (3 elements at a time)
            for comb in itertools.combinations(vals, 3):
                inxs = (use.apply(lambda x: comb[0] in x)) | (use.apply(lambda x: comb[1] in x)) | (use.apply(lambda x: comb[2] in x))
                
                #if it is a triple
                if sum(inxs) == 3:
                    no_of_hidden = sum(inxs)
                    #determine hidden triple indexes
                    triple_inx = inxs.index[inxs]

                    #remove the value from the specific cell of the candidates
                    cands = hidden_remove(rowcolbox,group_no,triple_inx,comb,cands,square_pos,no_of_hidden)

    if ischanged:
        solver.solver(board,cands,square_pos)    
     