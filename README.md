# Sudoku-Solver
Solves the user entered Sudoku boards with commonly known strategies* which are:
- Single candidates
- Hidden singles
- Naked pairs
- Hidden pairs
- Naked triples
- Hidden triples
- Pointing pairs
- Box/Line reduction
- X-wing
- Y-wing
- Simple colouring (Singles' chains)

_(*)Strategies are not complete yet, new ones will be added one by one once completed._

User enters the board in 81 digit string format where zeros represents empty cells in the board:
``` python
grid = "000000700000001080300020004090002060005000800080700050200070003060500000003000000"
```

Scrpit converts the string into 9x9 dataframe:

![plot2](https://github.com/omerfarukeker/Sudoku-Solver/blob/master/images/board_initial.JPG)

Candidates for cells are kept in a separate dataframe:

![plot4](https://github.com/omerfarukeker/Sudoku-Solver/blob/master/images/candidates.JPG)

Strategies are implemented in the listed order which is given above. Any changes in the board or candidates results in recursively calling the solver function again. Changes in the board are logged and displayed in Row&Column pair notation:

```python
R4C5=5 : Hidden Singles (row)
R5C2=3 : Hidden Singles (col)
R9C4=2 : Hidden Singles (col)
R3C6=7 : Hidden Singles (col)
R1C8=3 : Hidden Singles (col)
R1C6=5 : Hidden Singles (square)
R6C3=2 : Hidden Singles (square)
R4C4=8 : Hidden Singles (square)
R3C3=8 : Hidden Singles (row)
R4C7=3 : Hidden Singles (row)
R7C6=8 : Hidden Singles (row)
R2C4=3 : Hidden Singles (col)
R1C5=8 : Hidden Singles (col)
R0C0     Pointing Pairs (cols), 6 removed
R1C0     Pointing Pairs (cols), 6 removed
R1C1     X-Wing, removed 5 from rows
R8C1     X-Wing, removed 5 from rows
R1C6     X-Wing, removed 5 from rows
R8C6     X-Wing, removed 5 from rows
R0C3     X-Wing, removed 6 from rows
R4C3     X-Wing, removed 6 from rows
R1C6     X-Wing, removed 6 from rows
R8C6     X-Wing, removed 6 from rows
R8C0     Hidden Pairs (row), 1 removed
R8C0     Hidden Pairs (row), 4 removed
R8C0     Hidden Pairs (row), 7 removed
R8C0     Hidden Pairs (row), 9 removed
R8C8     Hidden Pairs (row), 1 removed
R8C8     Hidden Pairs (row), 6 removed
R8C8     Hidden Pairs (row), 7 removed
R8C8     Hidden Pairs (row), 9 removed
R2C6     Hidden Pairs (col), 1 removed
R2C6     Hidden Pairs (col), 9 removed
R6C6     Hidden Pairs (col), 1 removed
R6C6     Hidden Pairs (col), 4 removed
R6C6     Hidden Pairs (col), 9 removed
R7C7=6 : Hidden Singles (square)
R3C7=5 : Single Candidate
R3C2=1 : Single Candidate
R3C8=9 : Single Candidate
R2C7=2 : Single Candidate
R2C9=6 : Single Candidate
R3C4=6 : Single Candidate
R1C9=1 : Single Candidate
R4C9=7 : Single Candidate
R6C9=9 : Single Candidate
R5C9=2 : Single Candidate
R8C9=8 : Single Candidate
R9C9=5 : Single Candidate
R9C1=8 : Single Candidate
R1C3=6 : Hidden Singles (row)
R1C2=2 : Hidden Singles (row)
R2C1=5 : Hidden Singles (row)
R5C1=7 : Hidden Singles (row)
R7C2=5 : Hidden Singles (row)
R8C8=2 : Hidden Singles (row)
R6C1=6 : Hidden Singles (col)
R9C8=7 : Hidden Singles (col)
R8C3=7 : Hidden Singles (square)
R9C2=4 : Single Candidate
R2C2=7 : Single Candidate
R4C4     X-Wing, removed 1 from rows
R7C4     X-Wing, removed 1 from rows
R7C6     X-Wing, removed 1 from rows
R2C6     X-Wing, removed 1 from cols
R7C3=9 : Single Candidate
R8C1=1 : Single Candidate
R2C3=4 : Single Candidate
R2C5=9 : Single Candidate
R4C1=4 : Single Candidate
R4C3=1 : Single Candidate
R1C1=9 : Single Candidate
R1C4=4 : Single Candidate
R7C4=1 : Single Candidate
R7C8=4 : Single Candidate
R8C7=9 : Single Candidate
R9C5=6 : Single Candidate
R9C6=9 : Single Candidate
R9C7=1 : Single Candidate
R5C4=9 : Single Candidate
R5C5=4 : Single Candidate
R5C6=6 : Single Candidate
R5C8=1 : Single Candidate
R6C6=3 : Single Candidate
R6C7=4 : Single Candidate
R8C5=3 : Single Candidate
R8C6=4 : Single Candidate
R6C5=1 : Single Candidate
```

After solving the board, it shows the final look of it and how much time it took:

![plot3](https://github.com/omerfarukeker/Sudoku-Solver/blob/master/images/board_final.JPG)
