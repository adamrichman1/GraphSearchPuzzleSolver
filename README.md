# CS 1571 Project 1: Graph Search Puzzle Solver

## Project Setup
-	Python version: 2.7
-	Developed using: PyCharm for Mac

## To Run
<code>
python puzzlesolver.py {puzzle_config_file} {search_algorithm} {optional_heuristic}
</code>

## Config Files
All configuration files to run Puzzle Solver are located in the resources folder

## Search Algorithms
The following search algorithms are supported: bfs, dfs, unicost, greedy, astar

## Optional Heuristics
If greedy or astar search is selected as the algorithm, the following heuristics can be specified:

- Cities Puzzle: euclidean distance (eu), manhattan distance (md)
- Jugs Puzzle: distance from goal (d), misplaced jugs (mj)
- Tiles Puzzle: manhattan distance (md), misplaced tiles (mt), euclidean distance (eu)

## Notes
-	The report and all test outputs mentioned in the Report Specification are located in the report/ directory at the root of the project. There is a zip file for each puzzle containing output text files for the puzzles below.

-	All configuration files should be added to the resources/ directory at the root of the project.