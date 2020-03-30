'''
This script reads data from data files
and counts APs. For now. 
Mercedes Gonzalez. March 2020. 
'''
# Import necessary libraries
from os import listdir
from os.path import isfile, join
import csv
import numpy as np
import scipy as sp
import pyabf
import matplotlib as plt
import axographio as axo
from patchAnalysis import * 

# Init variables
SHOW_PLOTS = False # Refers to individual sweep plots
SHOW_FINAL_PLOT = False
SHOW_HEAD = False
my_path = "C:/Users/mgonzalez91/Dropbox (GaTech)/Research/All Things Emory !/Emory-Patching/1-23-2020/"
csv_name = "Jan-23-Analysis.csv"
csv_file = join(my_path,csv_name)
cap = 26.1

# Read only abf files from directory 
abf_files = [f for f in listdir(my_path) if isfile(join(my_path, f)) & f.endswith(".abf")]
abf = pyabf.ABF((my_path+abf_files[0]))
if SHOW_HEAD: abf.headerLaunch()

# Analyze each file
for file_name in abf_files:
    full_file = join(my_path, file_name)
    abf = pyabf.ABF(full_file)

    input_cmd = np.empty((abf.sweepCount,1))
    AP_count = np.empty((abf.sweepCount,1))
    input_dur = np.empty((abf.sweepCount,1))
    
    # Plot membrane test if available
    # plotMembraneTest(abf)

    # Analyze traces
    for sweep_idx in range(abf.sweepCount):
        input_cmd[sweep_idx], AP_count[sweep_idx], input_dur[sweep_idx] = countAPs(abf,sweep_idx,SHOW_PLOTS) # x is time, y is data, c is command
        # print("input: %f, APs: %i\n" % (input_cmd[sweep_idx], AP_count[sweep_idx]))
    
    # Plot 
    if SHOW_FINAL_PLOT:
        plt.figure()
        plt.plot(input_cmd,AP_count,"o")

if SHOW_FINAL_PLOT:
    plt.xlabel("Input Current (pA)")
    plt.ylabel("Num Action Potentials")
    plt.show() 

step_time = input_dur[0]/abf.dataRate*1000 # convert from input duration in samples to input duration in seconds
# step_time = .2 # temp 
plt.figure()
plt.plot(input_cmd/cap,AP_count/step_time)
plt.plot(input_cmd/cap,AP_count/step_time,"o")
plt.xlabel("Current Density (pA/pF)")
plt.ylabel("Firing Frequency (Hz)")
plt.show()
# Save as csv
all_data = np.concatenate((input_cmd,AP_count),axis=1)
np.savetxt(csv_file, all_data, delimiter=',', fmt=['%f','%d'], header='Current (pA), Num APs')
