# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 13:21:59 2018

@author: WIN  10
"""
from matplotlib.pyplot import bar
import matplotlib.pyplot as plt
import copy
import numpy as np
import math
def RR(processesVector,timeQuantum,contextSwitching):
    processes=copy.deepcopy(processesVector)
    
    currentTime=0
    processes = sorted(processes, key=lambda x: x.ArrivalTime, reverse=False)

    processes[0].set_firstStart(processes[0].ArrivalTime)
    if processes[0].BurstTime< timeQuantum:
        Slot=processes[0].BurstTime
    else:
        Slot=timeQuantum
    currentTime=Slot+contextSwitching
    
    for i in range(1, len(processes)):
        if processes[i].ArrivalTime < (currentTime):
            processes[i].set_firstStart(currentTime)
            
        else:
            processes[i].set_firstStart(processes[i].ArrivalTime)
        if processes[i].BurstTime< timeQuantum:
            Slot=processes[i].BurstTime
        else:
            Slot=timeQuantum
        currentTime=currentTime+contextSwitching+Slot

    maxIntervals=getmax_numOfintervals(processes,timeQuantum) 
    currentTime=0
    RR=copy.deepcopy(processes)
    plotRR(RR,timeQuantum,maxIntervals,contextSwitching)
    statistics(processes)
    return processes

def getmax_numOfintervals(processes,timeQuantum):
    maxBurstTime=max(processes, key=lambda item:item.BurstTime)
    maxBurstTime=maxBurstTime.BurstTime
    maxIntervals=math.ceil(maxBurstTime/timeQuantum)
    return maxIntervals

def plotRR(processes,timeQuantum,maxIntervals,contextSwitching):
    currentTime=0
    startArray=[]
    minimumArray=[]
    colorArray=[]
    IDArray=[]
    for j in range(maxIntervals):
        for i in range(len(processes)):
            if(processes[i].BurstTime <=0):
                minimum=min(timeQuantum,processes[i].BurstTime)
                if(j==0):
                    start=processes[i].firstStart
                    currentTime=start+minimum

                else:
                    start=currentTime+contextSwitching
                    currentTime=start+minimum
                startArray.append(start)
                minimumArray.append(minimum)
                colorArray.append(processes[i].Color)
                IDArray.append(processes[i].ID)
                
                processes[i].BurstTime=processes[i].BurstTime-minimum
                if(processes[i].BurstTime==0):
                   processes[i].set_lastEnd(currentTime)
    plt.bar(startArray,IDArray, width=(minimumArray), align='edge',color=colorArray)

    plt.ylabel('Processes')
    plt.xlabel('Time')
    plt.title('Round Robin')
 
    plt.show()
def statistics(processes):
    for i in range(len(processes)):
        processes[i].TurnaroundTime=processes[i].lastEnd - processes[i].ArrivalTime
        processes[i].WaitingTime=processes[i].TurnaroundTime - processes[i].BurstTime
        processes[i].WeightedTurnaroundTime=(processes[i].TurnaroundTime/processes[i].BurstTime)