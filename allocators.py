## SAOFS: The Simple Autonomous Order Fulfillment Simulator 
## Author: Kyle E. C. Booth
## Email: kbooth@mie.utoronto.ca
## File description: Specify allocation logic. Define our own allocator/scheduler here (with appropriate adjustments in simulator.py). 

import numpy as np
from allocator_params import *

def allocateRandom(master_queue, available_robots, time): 
	robot_index = 0
	assigned = 0
	task_tracking = [] 
	assignment = []
	while robot_index < len(available_robots) and assigned < len(master_queue):
		task_index = np.random.random_integers(0, len(master_queue) - 1)
		if (task_index not in task_tracking):
			task_tracking.append(task_index)
			assignment.append([available_robots[robot_index].robot_details["ID"], master_queue[task_index].task_details["ID"]])
			robot_index = robot_index + 1
			assigned = assigned + 1
	return assignment

def allocateNaive(master_queue, available_robots, time):
	assignment_index = 0
	assignment = []
	for i in range(len(master_queue)):
		if assignment_index < len(available_robots):
			assignment.append([available_robots[assignment_index].robot_details["ID"], master_queue[i].task_details["ID"]])
		assignment_index = assignment_index + 1
	return assignment	
