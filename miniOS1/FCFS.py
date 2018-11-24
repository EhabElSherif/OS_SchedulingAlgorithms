# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 13:17:09 2018

@author: Esraa
"""
#import numpy
#%matplotlib inline
import matplotlib.pyplot as plt

from matplotlib.pyplot import bar
#from process import *
import numpy as np
import copy

def FCFS(processesVector,contextSwitching):
    processes=copy.deepcopy(processesVector)
    processes = sorted(processes, key=lambda x: x.ArrivalTime, reverse=False)
    
    processes[0].set_firstStart(processes[0].ArrivalTime)
    processes[0].set_lastEnd(processes[0].firstStart+processes[0].BurstTime)
    for i in range(1, len(processes)):
        if processes[i].ArrivalTime < (processes[i-1].lastEnd+contextSwitching):
            processes[i].set_firstStart(processes[i-1].lastEnd+contextSwitching)
        else:
            processes[i].set_firstStart(processes[i].ArrivalTime)
        processes[i].set_lastEnd(processes[i].firstStart+processes[i].BurstTime)

    plot(processes)
    statistics(processes)
    return processes

def plot(processes):
    start=[]
    burst=[]
    ID=[]
    coulor=[]
    for i in range(len(processes)):

        start.append(processes[i].firstStart)
        burst.append(processes[i].burstTime)
        ID.append(processes[i].id)
        coulor.append(processes[i].color)
    plt.bar(start,ID, width=(burst), align='edge',color=coulor )
        
         
    plt.ylabel('Processes')
    plt.xlabel('Time')
    plt.title('First come first serve')
 
    plt.show()
def statistics(processes):
    for i in range(len(processes)):
        processes[i].TurnaroundTime=processes[i].lastEnd - processes[i].ArrivalTime
        processes[i].WaitingTime=processes[i].TurnaroundTime - processes[i].BurstTime
        processes[i].WeightedTurnaroundTime=(processes[i].TurnaroundTime/processes[i].BurstTime)