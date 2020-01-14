# -*- coding: utf-8 -*-
"""
SUDOKU SOLVER V18
-new remove functions are made for naked/hidden pairs,triples and quads

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

###################################
#GRIDS FROM ANDREW STUART'S WEBSITE
###################################
#(SOLVED)
# grid = "000004028406000005100030600000301000087000140000709000002010003900000507670400000"
#(SOLVED) moderate in Andrew Stuart website, naked triple
# grid = "720096003000205000080004020000000060106503807040000000030800090000702000200430018"
# (SOLVED) board for naked pairs, X-wing, Y-wing
# grid = "309000400200709000087000000750060230600904008028050041000000590000106007006000104"
# (SOLVED) board for hidden pairs
# grid = "000000000904607000076804100309701080008000300050308702007502610000403208000000000"
# board for pointing pairs, X-wing, simple colouring, ***NEEDS*** XYZ wing
# grid = "000704005020010070000080002090006250600070008053200010400090000030060090200407000"
# (SOLVED) board for X-wing example, y-wing, simple colouring
# grid = "093004560060003140004608309981345000347286951652070483406002890000400010029800034"
# (SOLVED) board for hidden triples 
# grid="300000000970010000600583000200000900500621003008000005000435002000090056000000001"
# (SOLVED) board for hidden triples
# grid="000000000231090000065003100008924000100050006000136700009300570000010843000000000"
# (SOLVED) board for pointing pairs, box/line reduction, simple coloring
# grid="000921003009000060000000500080403006007000800500700040003000000020000700800195000"
# (SOLVED) board for pointing pairs, Y-wing (multiply y-wings at different locations)
# grid = "900240000050690231020050090090700320002935607070002900069020073510079062207086009"
# (SOLVED) pointing pairs, simple coloring
# grid = "007083600039706800826419753640190387080367000073048060390870026764900138208630970"
# simple coloring, pointing pairs, ***NEEDS*** x-cycles
# grid = "200041006400602010016090004300129640142060590069504001584216379920408165601900482"
# (SOLVED) simple coloring
# grid = "062900000004308000709000400600801000003000200000207003001000904000709300000004120"
# (SOLVED) simple coloring
# grid = "000000070000090810500203004800020000045000720000000003400308006072010000030000000"
# (SOLVED) simple coloring
# grid = "090200350012003000300008000000017000630000089000930000000700002000300190078009030"
# (SOLVED) simple coloring
# grid = "400800003006010409000005000010060092000301000640050080000600000907080100800009004"


###################################
#GRIDS FROM GITHUB AARON FREDERICK
###################################
# # https://github.com/sok63/sudoku-1/blob/master/sample/p096_sudoku.txt
# Grid 01 Simple colouring, pointing pairs ***NEEDS*** x-cycles
# grid = "200000006000602000010090004300009600040000090009500001500010370000408000600000002"
# Grid 02 ***NEEDS*** 3D medusa
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
# (SOLVED) Grid 48 pointing pairs, box/line reduction
# grid = "001007090590080001030000080000005800050060020004100000080000030100020079020700400"

###################################
#GRIDS FROM ANDREW CRACKING THE CRYPTIC
###################################
# (SOLVED)cracking the cryptic LGFL83r67M X-wing, hidden quads
# grid = "000000010210003480039800200060304900000000000001607040008002170026700098090000000"
#cracking the cryptic mgp6LprDM8, pointing pairs, X-wing, simple colouring, ***NEEDS*** swordfish
# grid = "800000100010790560007108040570020400008010795103050080701003006000000010002001900"
# (SOLVED) cracking the cryptic 3gLbRPQ42d  pointing pairs, box/line reduction, X-wing, naked quads
grid = "000000700000001080300020004090002060005000800080700050200070003060500000003000000"
#cracking the cryptic JDFGD8p2m3 box/line reduction, simple colouring, ***NEEDS***  diabolic strategies
# grid = "800000300040001000200470000400000000010002070003090005000685000008000120000009003"   
# (SOLVED) cracking the cryptic RRf6bgb9GG hidden triples
# grid = "609102080000000400502000000000020304100005000020000506000801000000000009805907040"   
#cracking the cryptic BHBjPFJJP4 ***NEEDS*** swordfish
# grid = "040300600001002090000000000000000000030600900007001020060400300700000008002007010"   
#cracking the cryptic jjPp4LNbBH pointing pairs, box/line reduction, simple colouring, ***NEEDS*** x-cycles
# grid = "000005302006030900080009070000100800070000095001060200054000000002000000810000006"   
# (SOLVED) cracking the cryptic 7PD6nQ77hT hidden triple (box), pointing pairs, X-wing, 
# grid = "008390000010000000700012300500900040300000005040008006005670001000000060000021400"   
# cracking the cryptic 497rhdJp27 ***NEEDS*** swordfish
# grid = "004700003030060090900001800800002500020070080001400007009500001050010030200006700"  
# cracking the cryptic jHFDQq6BtT ***NEEDS*** Gurth's Theorem (Diagonal Symmetric)
# grid = "000001002003000040050060700000800070007003800900050001006080200040600007200009060"  

###################################
#GRIDS FROM MY SUDOKU BOOKS
###################################
# (SOLVED) maxi sudoku book (zor 115) pointing pairs
# grid = "000904002080070600037000100500340000079000540000095007003000980001050020200809000"
# (SOLVED) maxi sudoku book (zor 129)  
# grid = "600103089000000000800005100000008905058406730402700000003500004000000000570904001"
# (SOLVED) maxi sudoku book (zor 147) pointing pairs
# grid = "070100000000065481000090200036000004700010005500000730005070000987540000000008060"
# maxi sudoku book (cok zor 70) simple colouring, ***NEEDS***  X-cycles, 
# grid = "000980100900001780000002060301007040002000600040200908080700000023100007005096000"
# maxi sudoku book (cok zor 73) ***NEEDS*** XYZ-Wing, X-Cycles, XY-Chain
# grid = "302040000000600903000700010006400302053000790409002500020007000507004000000010405"
# maxi sudoku book (cok zor 93) ***NEEDS*** XYZ-Wing, XY-Chain, WXYZ Wing,
# grid = "000910500000800067804050000582000040009000800060000259000020301320006000008073000"
# maxi sudoku book (cok zor 123) ***NEEDS*** X-cycles, WXYZ wing, Altern Inference Chains, XY-Chain, 
# grid = "003740860008500100600080007090000000800604001000000020500010004002009700049036200"
# maxi sudoku book (cok zor 127) ***NEEDS*** Hidden Unique Rectangles, Aligned Pair Exclusion, Altern Inference Chains, Y-wing, 3D Medusa,XY-Chain
# grid = "100005000500000603023106000780010000000932000000080042000203970305000006000700005"
# (SOLVED) maxi sudoku book (cok zor 130)  pointing pairs, simple colouring
# grid = "720000000030020019109804000280000300000090000003000027000309102490060070000000065"
# (SOLVED) maxi sudoku book (cok zor 131)  Y-wing
# grid = "000809000075000000082400031056080000109000504000090210710002890000000120000901000"
# maxi sudoku book (cok zor 135)  pointing pairs, ***NEEDS*** X-cycles
# grid = "020700100008050003001020060800145006000000000600298005040010900500070600007004050"
# (SOLVED) maxi sudoku book (cok zor 142)  pointing pairs, simple colouring
# grid = "190580700007001050500090000010020007009000600600030080000040003070100900006073045"
# maxi sudoku book (cok zor 150) pointing pairs, ***NEEDS*** XYZ wing, XY chain, WXYZ wing
# grid = "410005000200401008800000103008000070070106050020000800302000005100904007000300086"
# (SOLVED) sudoku book 3 zor puzzle 18
# grid = "100978004090000080008000100900204008500000001700506002007000800060000040800652009"
# (SOLVED) sudoku book 3 cok zor puzzle 2 pointing pairs
# grid = "400000005060000010002306900008050200000704000007030500003902400020000080600000001"
# (SOLVED) sudoku book 3 imkansiz puzzle 2 pointing pairs, X-wing
# grid = "009004003030070090800900600001008007040010020600400500005002008080030070400700100"

#use following to convert board tables to single line string:
# grid = np.array2string(board.replace(".",0).values.flatten()).translate({ord(i): None for i in "[]\n "})

#%% user interface for the console
# uinput = input("Enter the board in 81 digit format where empty cells are filled with zeros: ")
# if len(uinput) == 81:
#     grid = uinput
# elif len(uinput) == 0:
#     pass
# else:
#     print(f"Incorrect Sudoku Board (Entered {len(uinput)} digits only!)")


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
    
                
   