# Sudoku-Solver
Solves the user entered Sudoku boards with commonly known strategies* which are:
- Single candidates
- Hidden singles
- Naked pairs
- Hidden pairs
- Naked triples
- Hidden triples
- Pointing pairs
- X-wing

(*)Strategies are not complete yet, new ones will be added one by one once completed.

User enters the board in 81 digit string format where 0s represents empty cells in the board:

![plot1](https://github.com/omerfarukeker/Sudoku-Solver/blob/master/board_input%20string.JPG)

Scrpit converts the string into 9x9 dataframe:

![plot2](https://github.com/omerfarukeker/Sudoku-Solver/blob/master/board_initial.JPG)

And starts applying the strategies in the listed order which is given above. Any changes in the board results in recursively calling the solver function again:

omer
faruk
eker


After solving the board, it shows the final look of it and how much time it took:
![plot3](https://github.com/omerfarukeker/Sudoku-Solver/blob/master/board_final.JPG)
