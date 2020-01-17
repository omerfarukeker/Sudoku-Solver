# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:40:39 2020

@author: omer.eker
"""

from single_candidate import single_cand
from hidden_singles import hidden_singles
from hidden_pairs_triples_quads import hidden_pairs_triples, hidden_quads
from naked_pairs_triples_quads import naked_pairs_triples, naked_quads
from pointing_pairs import pointing_pairs
from box_line import box_line
from x_wing import x_wing
from y_wing import y_wing
from singles_chains import singles_chains
from xyz_wing import xyz_wing


import sys

#%% SOLVER FUNCTION
def solver(board,cands,square_pos):
    #run strategies in listed order as long as the board has empty cells (".")
    if (board==".").any().any():
        single_cand(board,cands,square_pos)
        hidden_singles(board,cands,square_pos)
        naked_pairs_triples(board,cands,square_pos)
        hidden_pairs_triples(board,cands,square_pos)
        pointing_pairs(board,cands,square_pos)
        box_line(board,cands,square_pos)
        naked_quads(board,cands,square_pos)
        hidden_quads(board,cands,square_pos)
        x_wing(board,cands,square_pos)
        y_wing(board,cands,square_pos)
        singles_chains(board,cands,square_pos)
        xyz_wing(board,cands,square_pos)
    else:
        print("COMPLETE!!!!!")
        # break
        sys.exit(0)