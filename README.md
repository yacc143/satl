Get all solutions for the sudokos
========================================

You need two external files to use this:

* the limboole executable for your platform from http://fmv.jku.at/limboole/index.html

Installation
------------

Standard python rules, e.g. pip install .

Usage
-----

solve_sudoku [-s 4]

to show you the variables of the grid.

solve_sudoku [-s 4] a=3 v=2 e=3

to try to solve a sudoku with constraints.

If limboole is available on the path with the *standard* name for your platform, 
you do not need to specify it via an option. 
