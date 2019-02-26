## SAOF-Sim: The Simple Autonomous Order Fulfillment Simulator 
## Author: Kyle E. C. Booth
## Email: kbooth@mie.utoronto.ca
## File description: Allocator supporting params. calculateCostMatrix() calculates cost of assigning a robot a particular task (currently unused in the allocation methods).

def calculateCostMatrix(master_queue, available_robots, distance_matrix):
	cost_matrix = []; M = 99999
	if (len(master_queue) >= len(available_robots)):
		for i in range(len(master_queue)): 
		    robot_cost = []
		    for j in range(len(master_queue)): 
		        total_cost = 0
		        if i < len(available_robots): 
		            total_cost = distance_matrix[available_robots[i].robot_details["location"]][master_queue[j].subtask_locations[0]]
		            for k in range(master_queue[j].task_details["subtasks"] - 1): # Remaining components
		                total_cost += distance_matrix[master_queue[j].subtask_locations[k]][master_queue[j].subtask_locations[k+1]]
		            #total_cost /= available_robots[i].movement_speed # TODO: If we move away from homogenous robots, include again.
		        else:
		            total_cost = M
		        robot_cost.append(total_cost)
		    cost_matrix.append(robot_cost)
	elif (len(master_queue) < len(available_robots)):
		for i in range(len(available_robots)):
		    robot_cost = []
		    for j in range(len(available_robots)):
		        total_cost = 0
		        if j < len(master_queue):
		            total_cost = distance_matrix[available_robots[i].robot_details["location"]][master_queue[j].subtask_locations[0]]
		            for k in range(master_queue[j].task_details["subtasks"] - 1): # Remaining components
		                total_cost += distance_matrix[master_queue[j].subtask_locations[k]][master_queue[j].subtask_locations[k+1]]
		            #total_cost /= available_robots[i].movement_speed
		        else:
		            total_cost = M
		        robot_cost.append(total_cost)
		    cost_matrix.append(robot_cost)
	
	#for i in range(len(available_robots)):
	#	print "Robot %d, Cost: %s" %  (i, cost_matrix[i])
		
	return cost_matrix
