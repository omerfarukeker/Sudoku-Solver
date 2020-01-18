# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:20:58 2020

@author: omer.eker
"""

import pandas as pd

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

#validation check function
def check_valid(board):
    rcheck = row_check(board)
    ccheck = col_check(board)
    cucheck = square_check(board)
    
    return rcheck and ccheck and cucheck