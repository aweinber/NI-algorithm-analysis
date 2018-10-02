# NI-algorithm-analysis
Project 1: Compare GA and PBIL

To run PBIL:
python EvolutionaryAlgorithm.py (problem_you_want.cnf) (number of individuals) (positive learning rate) (negative learning rate) (mutation percentage) (mutation amount) (number of iterations) p

For example:
python EvolutionaryAlgorithm.py problem-1.cnf 100 0.1 0.075 0.02 0.05 2000 p

To run the GA of the program:
python EvolutionaryAlgorithm.py (problem_you_want.cnf) (number of individuals) (selection method: ts for tournament selection, rs for ranking selection, bs for Boltzman selection) (crossover method: 1c for 1-point crossover, uc for uniform crossover) (crossover probability) (mutation probability) (number of iterations) g

For example:
python EvolutionaryAlgorithm.py problem-1.cnf 100 ts 1c 0.7 0.01 2000 g

The easiest problem as described in the report is problem-1.cnf. The medium problem is problem-2.cnf and the hardest problem is problem-3.cnf.