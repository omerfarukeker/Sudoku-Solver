# -*- coding: utf-8 -*-
"""
SUDOKU SOLVER V17
-functions are separated into different files
-hidden triples for box added
@author: omerzulal
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import time

from print_board import print_board
from validation_check import check_valid
from candidate_handler import candidates, candidates_update
from cells_seen import cells_seen
from solver import solver
from init_board import init_board

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
# (SOLVED) board for hidden triple 
# grid="000000000231090000065003100008924000100050006000136700009300570000010843000000000"
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
# grid = "400800003006010409000005000010060092000301000640050080000600000907080100800009004"
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
#cracking the cryptic jjPp4LNbBH ***NEEDS*** x-cycles
# grid = "000005302006030900080009070000100800070000095001060200054000000002000000810000006"   
# (SOLVED) cracking the cryptic 7PD6nQ77hT hidden triple (box)
grid = "008390000010000000700012300500900040300000005040008006005670001000000060000021400"   


# from my sudoku book (***NEEDS*** XYZ wing, XY chain, WXYZ wing)
# grid = "410005000200401008800000103008000070070106050020000800302000005100904007000300086"
#sudoku book puzzle 18
# grid = "100978004090000080008000100900204008500000001700506002007000800060000040800652009"
#use following to convert board tables to single line string:
# grid = np.array2string(board.replace(".",0).values.flatten()).translate({ord(i): None for i in "[]\n "})

#%% user interface for the console
uinput = input("Enter the board in 81 digit format where empty cells are filled with zeros: ")
if len(uinput) == 81:
    grid = uinput
elif len(uinput) == 0:
    pass
else:
    print(f"Incorrect Sudoku Board (Entered {len(uinput)} digits only!)")


#%% RUN THE SOLVER       
t1 = time.time()
board,square_pos = init_board(grid)
print_board(board)

#check validity before solving it
if check_valid(board):
    cands = candidates(board)
    solver(board,cands,square_pos)
else:
    print("The board is not valid!")
   
#check validity after solving it
if check_valid(board):
    print(f"Solving took {round(time.time()-t1,2)} seconds")
    board.index = np.arange(1,10)
    board.columns = np.arange(1,10)
    print_board(board)
    print(f"{(board == '.').sum().sum()} Missing Elements Left in The Board!")
    
                
   