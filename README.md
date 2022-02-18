# heuristic methods
Heuristic methods are approachs to problem solving that employs a method that is not guaranteed to find optimal solution. 

 Cheapest insertion: A tsp construction heuristic method that creates a feasible solution by inserting closest city to initial solution.
 
 Lagrangian relaxatian: A heuristic for the CPL problem. First it solves knapsack problem and finds Lowerbound values. By using lowerboundvalues code solves simplex and finds upperbound value. Then by iterating lowerbound values code terminate when epsilon ([ub-lb]/ub) is in desired value.
 
 Simulated Annealing: A metaheuristic method that introduce neighbor selection method, initial solution, initial temperature, cooling ratio, halting criterion and termination condition to solve tsp.
 
 Tabu search: It uses local search to mathematical optimization. We used static, recency based short-term memory to prevent revisiting previously visited solution.
 
 Genetic Algorithm for TSP: A population based meta-heuristic in which multiple pairs of solutions(parents) are modified to give rise to other solutions (children).


Cheapest instetion and simulated annealing solves tsp by using heuristic method, while genetic algorithm solves tsp by using metaheuristic method. 
Lagrangian which is heuistic method and tabu search which is a metaheuristic solve CPL.
