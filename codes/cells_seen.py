# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:31:40 2020

@author: omer.eker
"""
import pandas as pd

def cells_seen(inx,square_pos):
    cells = []
    #box
    cells.extend(square_pos[square_pos == square_pos.iloc[inx]].stack().index)
    #rows
    cells.extend(square_pos.iloc[[inx[0]],:].stack().index)
    #cols
    cells.extend(square_pos.iloc[:,[inx[1]]].stack().index)
    cells = pd.Series(cells).unique()
    return cells