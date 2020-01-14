# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 21:24:46 2020

@author: omerzulal
"""
import pandas as pd

#selects the group (row col or box)
def select_group(rowcolbox,cands,group_no,square_pos):
    if rowcolbox == "row":
        use = cands.loc[group_no].dropna()
    elif rowcolbox == "col":
        use = cands[group_no].dropna()
    elif rowcolbox == "box":
        inx = square_pos[square_pos==group_no+1].stack().index
        use = pd.Series([cands.iloc[i] for i in inx]).dropna()
    return use