**SAOF-Sim** The Simple Autonomous Order Fulfillment Simulator 
**Author:** Kyle E. C. Booth (kbooth@mie.utoronto.ca)  

### File descriptions:

*"main.py":* Main function. Loads problem/simulation params and calls simulateFactory(). Outputs makespan.

*"simulator.py":* Defines primary classes (robots, tasks, etc). Details simulateFactory() and simulateTimeStep() functions.

*"allocators.py":* Specify allocation logic. Define our own allocator/scheduler here (with appropriate adjustments in simulator.py). 

*"allocator_params.py":* Allocator supporting params. calculateCostMatrix() calculates cost of assigning a robot a particular task (currently unused in the allocation methods).

### Running the simulator:

Simply run "python main.py" in your terminal. Note that the simulator only works with Python 2 (at the moment). 
