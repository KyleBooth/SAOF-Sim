## SAOFS: The Simple Autonomous Order Fulfillment Simulator 
## Author: Kyle E. C. Booth
## Email: kbooth@mie.utoronto.ca
## File description: Main function. Loads problem/simulation params and calls simulateFactory(). Outputs makespan.

import numpy as np
import pandas as pd
import pprint as pp
import time
from simulator import *

if __name__ == '__main__':

	## Adjust below parameters for your experiments
	problem_parameters = {"robot_num": 2, "max_subtasks": 5, "max_tasks": 50, "initial_percentage": 0.2, "horizon": 100, "max_distance": 300, "locations": 15}

	simulation_parameters = {"random_seed": 0, "rate": 1.5, "allocation_method": "random",  "min_available_robots": 1, "max_wait": 0}

	makespan = simulateFactory(problem_parameters, simulation_parameters)

	print ("\n|===|\n(COMPLETE) Execution Makespan: %d \n|===|" % (makespan))


