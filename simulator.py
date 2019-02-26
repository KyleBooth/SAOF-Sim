## SAOF-Sim: The Simple Autonomous Order Fulfillment Simulator 
## Author: Kyle E. C. Booth
## Email: kbooth@mie.utoronto.ca
## File description: Defines primary classes (robots, tasks, etc). Details simulateFactory() and simulateTimeStep() functions.

import numpy as np
from allocators import *
import time as myTime

class robot:
    def __init__(self, i, locations):
        self.movement_speed = np.random.normal(3, 0.2, 1)
        self.failure_rate = np.random.normal(2, 0.5, 1)
        self.consumption_rate = np.random.normal(2, 0.5, 1)
        self.robot_details = {"ID": i, "assigned": -1, "goal_distance": -1, "location": np.random.random_integers(1, locations) - 1}
        self.task_completions = []

class task:
    def __init__(self, i, max_subtasks, locations):
        self.task_details = {"ID": i, "subtasks": -1, "robot": -1, "start": -1, "end": -1}
        self.task_details["subtasks"] = np.random.random_integers(2, max_subtasks)
        self.subtask_locations = [np.random.random_integers(1, locations) - 1 for subtask in range(self.task_details["subtasks"])]

def generateFacility(locations, max_distance):
    distance_matrix = [[np.random.random_integers(max_distance) for i in range(locations)] for i in range(locations)]
    return distance_matrix

def generateTaskArrivals(rate, initial_tasks, max_tasks):
    task_arrivals = [0 for i in range(initial_tasks)]
    for i in range(initial_tasks, max_tasks):
            interarrival = np.random.poisson(rate)
            task_arrivals.append(task_arrivals[i-1] + interarrival)
    return task_arrivals

def generateMasterQueue(max_tasks, task_arrivals, task_list, time):
    master_queue = []
    for i in range(max_tasks):
        if task_arrivals[i] <= time and task_list[i].task_details["robot"] == -1 and task_list[i].task_details["end"] < 0:
            master_queue.append(task_list[i])
    return master_queue

def generateAvailableRobots(robot_num, robot_list):
    available_robots = []
    for i in range(robot_num):
        if robot_list[i].robot_details["assigned"] == -1:
            available_robots.append(robot_list[i])
    return available_robots

def simulateFactory(problem_parameters, simulation_parameters):

	for key,val in problem_parameters.items():
		exec(key + '=val')
	for key,val in simulation_parameters.items():
		exec(key + '=val')    

	np.random.seed(random_seed)

	initial_tasks = int(round(max_tasks * initial_percentage))
	distance_matrix = generateFacility(locations, max_distance)
	task_arrivals = generateTaskArrivals(rate, initial_tasks, max_tasks)
	task_list = [task(i, max_subtasks, locations) for i in range(max_tasks)]
	robot_list = [robot(i, locations) for i in range(robot_num)]

	master_queue = []
	available_robots = []
	makespan = 0
	tasks_completed = 0
	time = 0
	
	iterations = 0
	
	while tasks_completed < max_tasks:
		        
		master_queue = generateMasterQueue(max_tasks, task_arrivals, task_list, time)
		available_robots = generateAvailableRobots(robot_num, robot_list) 
	
		waitFlag = False
		
		goal_distance_vector = [round(float(robot_list[i].robot_details["goal_distance"]), 2) for i in range(len(robot_list))]
		
		## Immediate Assignment
		for item in goal_distance_vector:
			if item >= 0 and item < max_wait:
				waitFlag = True
		
		## Batch Assignment
		#freeCount = 0
		#for i in range(len(robot_list)):
		#	if (robot_list[i].robot_details["assigned"] != -1):
		#		freeCount += 1
		#if freeCount != 0:
		#	waitFlag = True
		
		assignment = []
	
		## Conditions for allocation 
		if (len(available_robots) >= min_available_robots and len(master_queue) >= 1 and waitFlag == False):
			print ("\n |=== Allocating ===| \n")
			print ("Tasks: %d | Robots: %d" % (len(master_queue), len(available_robots)))
			if allocation_method == "random":
				assignment = allocateRandom(master_queue, available_robots, time)			
			elif allocation_method == "naive":
				assignment = allocateNaive(master_queue, available_robots, time)
			else:
				print ("Specified allocation method invalid.")
				break

			if len(assignment) != 0:
				for i in range(len(available_robots)):
					if (i < len(master_queue)):
						robot_list[assignment[i][0]].robot_details["assigned"] = assignment[i][1]
						task_list[assignment[i][1]].task_details["robot"] = assignment[i][0]
						task_list[assignment[i][1]].task_details["start"] = time
		
			iterations += 1
					
		robot_list, task_list, tasks_completed = simulateTimeStep(robot_list, task_list, distance_matrix, time, tasks_completed)
		
		goal_distance_vector = [round(float(robot_list[i].robot_details["goal_distance"]), 2) for i in range(len(robot_list))]
		print ("Time step: %d, Distance vector: [%s]" % (time, ', '.join(map(str, goal_distance_vector))))
		
		time += 1
		
	makespan = time
	
	return makespan

def simulateTimeStep(robot_list, task_list, distance_matrix, time, tasks_completed):
	for i in range(len(robot_list)):
		if robot_list[i].robot_details["assigned"] != -1: 
			if robot_list[i].robot_details["goal_distance"] == 0: 
				print ("Time step: %d, Task %d completed!" % (time, task_list[robot_list[i].robot_details["assigned"]].task_details["ID"]))
				task_list[robot_list[i].robot_details["assigned"]].task_details["end"] = time 
				task_list[robot_list[i].robot_details["assigned"]].task_details["robot"] = -1
				tasks_completed = tasks_completed + 1 
				robot_list[i].robot_details["location"] = task_list[robot_list[i].robot_details["assigned"]].subtask_locations[-1]
				robot_list[i].robot_details["assigned"] = -1 
				robot_list[i].robot_details["goal_distance"] = -1
			else:
				robot_list[i].robot_details["goal_distance"] = distance_matrix[robot_list[i].robot_details["location"]][task_list[robot_list[i].robot_details["assigned"]].subtask_locations[0]]
				for j in range(task_list[robot_list[i].robot_details["assigned"]].task_details["subtasks"] - 1): 
					robot_list[i].robot_details["goal_distance"] += distance_matrix[task_list[robot_list[i].robot_details["assigned"]].subtask_locations[j]][task_list[robot_list[i].robot_details["assigned"]].subtask_locations[j+1]]
				robot_list[i].robot_details["goal_distance"] = max((robot_list[i].robot_details["goal_distance"] - robot_list[i].movement_speed * (time - task_list[robot_list[i].robot_details["assigned"]].task_details["start"])), 0)

	return robot_list, task_list, tasks_completed

