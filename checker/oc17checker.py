#-------------------------------------------------------------------------------
# Name:        oc17checker.py
# Purpose:     Check solution of OC17 challenge
#
# Author:      Adi Sarid
#
# Created:     23/02/2017
# Copyright:   (c) Adi Sarid 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


# The script is fairly simple:
# Read solution (reader aux function already sorts the input by resource and time)
# Validate each step of each resource (time, space, and skill)
# Raise violations if identified
# Calculate objective functions' values

# The script assumes that the first argument is location of files, and the rest are
# files' names (solution, resources, skills, tasks).
# if no argument is given, uses current directory and default names:
# solution.csv, Resources_v2.csv, Resources_Skills_v2.csv, Tasks_v2.csv
# if a single argument is given it asumes that the argument is the directory and uses these file names in the directory
# if more than one argument is given, it assumes that the first argument is dir and the rest are file names (must all appear)
# Here is the order of arguments for example, when reading the example files:
# "..\sample_files\" "example_solution_v2.csv" "Example_Resources.csv" "Example_Resources_Skills.csv" "Example_Tasks.csv"

# load required packages
from checker_aux import * # import auxiliary files from checker_aux file.
import sys # for command line parameters
import os # for current directory
from copy import copy, deepcopy # for creating copies of objects


sol_filename = 'solution.csv'
res_filename = 'Resources_v2.csv'
skl_filename = 'Resources_Skills_v2.csv'
tsk_filename = 'Tasks_v2.csv'

if len(sys.argv) == 1: #only the script no arguments given
    curdir = os.getcwd() + "\\"
elif len(sys.argv) == 2:
    curdir = sys.argv[1]
elif len(sys.argv) < 6:
    print "Not enough arguments specified. I have", len(sys.argv), "arguments. \nScript can run on:"
    print "0 arguments (assumes current dir);"
    print "1 argument (file location, default names assumed);"
    print "2 arguments (directory + solution file name + the rest are default names);"
    print "or 5 arguments (directory + all files' names)."
else:
    curdir = sys.argv[1]
    sol_filename = sys.argv[2]
    res_filename = sys.argv[3]
    skl_filename = sys.argv[4]
    tsk_filename = sys.argv[5]

# read instance
print 'reading solution from:', curdir+sol_filename
print 'reading resource from:', curdir+res_filename
print 'reading skills from:', curdir+skl_filename
print 'reading tasks from:', curdir+tsk_filename

sol_dat = read_sol_into_list(curdir + sol_filename)
res_dat = read_into_dict(curdir + res_filename)
skl_dat = read_into_dict(curdir + skl_filename)
tsk_dat = read_into_dict(curdir + tsk_filename, skipcols = [2,3])

# start the validation process:
# some constants
shift_start = 8*60.0
shift_end = 17*60.0
# init objective functions' values:
tasks_scheduled = list(set([r[1] for r in sol_dat])) # tasks allegedly fulfilled (before checking for violations), using "set" for unique values
if len(tasks_scheduled) != len(sol_dat):
    print 'WARNING: You are traversing some tasks more than once (omitting redundance, counting as unique).'

tot_travel_time = 0
tasks_safe_zone = 0
shift_end = dict() # going to hold data per resource and later compute the fairness objective
shift_duration = [] # a list going to hold shift duration for all resources
# record violations
violations = [['resource', 'task', 'violation type']] # the rest of sublists are going to be comprised of integers
# violation types:
# 1 = drive time/duration mismatch,
# 2 = task started outside time window,
# 3 = skill mismatch,
# 4 = shift hours violated

# extract all resources in the solution
res_used = list(set([r[0] for r in sol_dat])) # using "set" for unique values

for cur_res in res_used:
    # first, create the resource path
    cur_res_path = [r[0:3] for r in sol_dat if r[0] == cur_res] # isolate the path of the current resource, omit task end time
    last_step = [cur_res, 0, shift_start] # initialize origin as last step
    for next_step in cur_res_path:
        # compute travel time and duration
        if last_step[1] == 0:
            # starting from origin
            drive_time = calc_drive_time(res_dat[cur_res][0:2], tsk_dat[next_step[1]][1:3])
            treat_duration = 0 # no time spent treating the origin
        else:
            # mid path
            drive_time = calc_drive_time(tsk_dat[last_step[1]][1:3], tsk_dat[next_step[1]][1:3])
            treat_duration = max(1,round(tsk_dat[last_step[1]][3] / res_dat[cur_res][2],0)) # max(1, round(task duration / resource efficiency))
        # make sure travel time + duration is ok VIOLATION TYPE 1
        if (drive_time + treat_duration + last_step[2]) > next_step[2]:
            violations += [[cur_res, last_step[1], 1]]
            print 'Violation found. Resource:', cur_res, 'Task', last_step[1], 'Last stop start + treatment + drive time = ', str(drive_time + treat_duration + last_step[2]), ', but next start time = ', str(next_step[2])
        # make sure task starts within time window VIOLATION TYPE 2
        if (next_step[2] < tsk_dat[next_step[1]][4] or next_step[2] > tsk_dat[next_step[1]][5]):
            violations += [[cur_res, next_step[1], 2]]
            print 'Violation found. Resource:', cur_res, 'Task', next_step[1], 'not within window. Start=', next_step[2], 'Window=[', tsk_dat[next_step[1]][4], tsk_dat[next_step[1]][5] , ']'
        # check skill (make sure task can be treated by current resource) VIOLATION TYPE 3
        # (i.e., is the skill required for the current task is indeed in the resource's skill list)
        if not (tsk_dat[next_step[1]][0] in skl_dat[cur_res]):
            violations += [[cur_res, next_step[1], 3]]
            print 'Violation found. Resource:', cur_res, 'Task', next_step[1], 'not within skill. Task requires=', tsk_dat[next_step[1]][0], 'Resource skills', skl_dat[cur_res]
        # check if should be counted within safe time (at least 30 min before latest start time) - not mandatory, but for objective
        if (next_step[2] < tsk_dat[next_step[1]][5]-30):
            tasks_safe_zone += 1

        # update objective function values:
        tot_travel_time += drive_time

        # update last step to current step:
        last_step = copy(next_step)

    # make sure resource has enough time to return to origin (VIOLATION TYPE 4):
    drive_time = calc_drive_time(tsk_dat[last_step[1]][1:3], res_dat[cur_res][0:2])
    treat_duration = max(1,round(tsk_dat[last_step[1]][3] / res_dat[cur_res][2],0))
    tot_travel_time += (treat_duration + drive_time)
    shift_end[cur_res] = last_step[2] + treat_duration + drive_time
    if (shift_end[cur_res] > 17*60):
        violations += [[cur_res, 0, 4]]
    shift_duration += [shift_end[cur_res] - 8*60]



# Print summary
print "Validation complete."
if len(violations)-1==0:
    print "Solution feasible, no violations found"
else:
    print "WARNING: Solution is infeasible!"
    print "Checker found", len(violations)-1, "violations. See variable 'violations' for more information."
    print "Continuing to compute objective value even though the solution is infeasible"
print "Objective value (lexicographic order):"
print "(#tasks, tot travel time, #tasks in safe zone, max diff in shift duration)"
print "(", len(tasks_scheduled), "," , tot_travel_time, "," , tasks_safe_zone, "," , max(shift_duration) - min(shift_duration), ")"

























