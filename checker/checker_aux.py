#-------------------------------------------------------------------------------
# Name:        OC17' challenge - Checker auxiliary functions
# Purpose:     Auxiliary common functions for checker (solution validation)
#
# Author:      Adi Sarid
#
# Created:     22/02/2017
# Copyright:   (c) Adi Sarid 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from math import acos, cos, sin # for calculating distance
import csv # for importing files
from operator import itemgetter # for sorting with itemgetter

def calc_distance(Origin, Destination):
    '''
    Calculates distance according to pre-defined formula in competition
    Instructions. Distance =
                ACOS(SIN(Origin_Lat * 3.14159265358979 / 180.0) * SIN(Destination_Lat * 3.14159265358979 / 180.0) +
                COS(Origin_Lat * 3.14159265358979 / 180.0) * COS(Destination_Lat * 3.14159265358979 / 180.0) *
                COS((Destination_Long - Origin_Long) * 3.14159265358979 / 180.0)) * 6371
    Assumes first argument is Origin = [Lat, Lon],
    Second argument           Destination = [Lat, Lon]
    '''
    
    if Origin == Destination:
        return(0)
    else:
        Origin_Lat = Origin[0]
        Origin_Long = Origin[1]
        Destination_Lat = Destination[0]
        Destination_Long = Destination[1]
    
        distance = acos(sin(Origin_Lat * 3.14159265358979 / 180.0) * sin(Destination_Lat * 3.14159265358979 / 180.0) + \
        cos(Origin_Lat * 3.14159265358979 / 180.0) * cos(Destination_Lat * 3.14159265358979 / 180.0) * \
        cos((Destination_Long - Origin_Long) * 3.14159265358979 / 180.0)) * 6371
        return(distance)

def calc_drive_time(Origin, Destination, velocity = 50/60.0):
    dist = max(1, round(calc_distance(Origin, Destination)/velocity, 0)) # at least a minute and rounded to the nearest integer
    return(dist)

def read_into_dict(filename, skipcols = []):
    '''
    Read a csv file into a dictionary. First column of the csv becomes the key
    The rest becomes the list (value)
    The function converts the key into an integer instead of string
    This file doesn't read the solution format which requires a two-index key (first two fields)
    skipcols will skip columns. column number counted from 0.
    '''
    res_dict = dict()
    with open(filename, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter = ",")
        header = next(datareader)
        for row in datareader:
            cur_key = int(row.pop(0)) # get the key and pop out the first row element
            if cur_key in res_dict.keys():
                # Key already exists (many to one) -> add to current list. In our problem in this case input is a single number (Skill ID)
                res_dict[cur_key] += [float(row[0])] # add to list
            else:
                # Key doesn't exist in dictionary (first ocurrance / one-to-one)
                res_dict[cur_key] = [float(row[i]) for i in range(len(row)) if not i-1 in skipcols] # set the dict values as double *** FIX HERE COLUMN SKIP - index counted incorrectly ***
    return(res_dict)

def read_sol_into_list(filename, header = True):
    '''
    Reads a solution csv file into a list
    Assumes a header exists (otherwise use header = False)
    The function assumes Start_time is given in minutes after midnight
    As in example_solution v2.csv (and not the original version's hh:mm:ss AM/PM format)
    '''
    res_list = []
    with open(filename, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter = ",")
        if header:
            header_line = next(datareader)
        for row in datareader:
            res_list += [[int(i) for i in row]] # assumes that all strings can be converted to integers
    # sort the resulting list (of lists) by ascending order:
    # resource, then task start time
    # this is the easiest way to iterate on resource route
    sorted_list = sorted(res_list, key = itemgetter(0, 2))
    return(sorted_list)

# a = read_sol_into_list('../sample_files/Example_Solution v2.csv') # code for loading sample solution, just to check...