import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import filedialog
import copy
import numpy as np
def HPF(ProcessesVector,Context,TimeStep):
    TimeStep=0.1
    #Sort the list by (Arrival Time in ascending order AND Priority in descending order)
    ProcessesVector = sorted(ProcessesVector, key=lambda process: (process.ArrivalTime))
    ReadyQueue=[]
    ProcessesVectorResult=copy.deepcopy(ProcessesVector)
    CurrentTime=0
    C=Context
    plt.title('Non-Preemptive Highest Priority First')
    plt.ylabel('Process ID')
    plt.xlabel('Time')
    plt.grid(True)
    Ticks=np.arange(0,len(ProcessesVector)+1,1)
    plt.yticks(Ticks)
    i=0
    while (len(ReadyQueue)>0 or len(ProcessesVector) > 0):
        while(len(ProcessesVector)>0 and ProcessesVector[0].ArrivalTime<=CurrentTime):
            ReadyQueue.append(ProcessesVector.pop(0))

        if(len(ReadyQueue)>0):
            if(ReadyQueue[0].BurstTime>0 ):
                #plt.pause(0.0001)
                plt.plot([CurrentTime,CurrentTime],[0,ReadyQueue[0].ID],color=ReadyQueue[0].Color)
                ReadyQueue[0].BurstTime-=TimeStep
            elif(ReadyQueue[0].BurstTime<=0):
                ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime=CurrentTime-ProcessesVectorResult[ReadyQueue[0].ID-1].ArrivalTime-TimeStep
                ProcessesVectorResult[ReadyQueue[0].ID-1].WeightedTurnaroundTime=ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime / ProcessesVectorResult[ReadyQueue[0].ID-1].BurstTime
                ProcessesVectorResult[ReadyQueue[0].ID-1].WaitingTime=ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime - ProcessesVectorResult[ReadyQueue[0].ID-1].BurstTime
                ReadyQueue.pop(0)
                ReadyQueue = sorted(ReadyQueue, key=lambda process: (-1*process.Priority,process.ID))
                if len(ReadyQueue)>0:
                    CurrentTime+=Context
                i+=1
                continue
        CurrentTime+=TimeStep
    plt.show()
    return ProcessesVectorResult

def findFasterProcess(ProcessesVector,CurrentTime):
    MinProcess=0
    i=1
    for i in range(1,len(ProcessesVector)):
        if (ProcessesVector[i].BurstTime<ProcessesVector[MinProcess].BurstTime and ProcessesVector[i].ArrivalTime<CurrentTime) :
            MinProcess=i
    return MinProcess

def SRTN(ProcessesVector,Context,TimeStep):
    ProcessesVector=sorted(ProcessesVector,key=lambda process: ([process.ArrivalTime]))
    ProcessesVectorResult=copy.deepcopy(ProcessesVector)
    CurrentTime=0
    ReadyQueue=[]
    i=-1
    plt.title('Shortest Remaining Time Next')
    plt.ylabel('Process ID')
    plt.xlabel('Time')
    plt.grid(True)
    Ticks=np.arange(0,len(ProcessesVector)+1,1)
    plt.yticks(Ticks)
    
    while (len(ReadyQueue)>0 or len(ProcessesVector) > 0):
         while(len(ProcessesVector)>0 and ProcessesVector[0].ArrivalTime<=CurrentTime):
                ReadyQueue.append(ProcessesVector.pop(0))
                ReadyQueue = sorted(ReadyQueue, key=lambda process: (process.BurstTime))

         if(len(ReadyQueue)>0):
            if not (i==-1 or i == ReadyQueue[0].ID):
                CurrentTime+=Context
                i= ReadyQueue[0].ID
                continue
            if(ReadyQueue[0].BurstTime<=0):
                ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime=CurrentTime-ProcessesVectorResult[ReadyQueue[0].ID-1].ArrivalTime-TimeStep
                ProcessesVectorResult[ReadyQueue[0].ID-1].WeightedTurnaroundTime=ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime / ProcessesVectorResult[ReadyQueue[0].ID-1].BurstTime
                ProcessesVectorResult[ReadyQueue[0].ID-1].WaitingTime=ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime - ProcessesVectorResult[ReadyQueue[0].ID-1].BurstTime
                ReadyQueue.pop(0)
                ReadyQueue = sorted(ReadyQueue, key=lambda process: (process.BurstTime))
                if len(ReadyQueue)>0:
                    CurrentTime+=Context
                continue
            ReadyQueue[0].BurstTime-=TimeStep
            plt.plot([CurrentTime,CurrentTime],[0,ReadyQueue[0].ID],color=ReadyQueue[0].Color)
         CurrentTime+=TimeStep
    plt.show()
    return ProcessesVectorResult
    
#def FCFS(ProcessesVector,Context):
#    ProcessesVector = sorted(ProcessesVector, key=lambda process: (process.ArrivalTime))
#    ProcessesVectorResult=copy.deepcopy(ProcessesVector)
#    CurrentTime=0
#    plt.title('First Come First Serve')
#    plt.ylabel('Process ID')
#    plt.xlabel('Time')
#    plt.grid(True)
#    Ticks=np.arange(0,len(ProcessesVector)+1,1)
#    plt.yticks(Ticks)
#    i=0
#    while len(ProcessesVector) > 0:
#        if(ProcessesVector[0].BurstTime>0 and ProcessesVector[0].ArrivalTime<=CurrentTime):
#            if(ProcessesVector[0].WaitingTime==-1):
#                ProcessesVectorResult[ReadyQueue[0].ID-1].WaitingTime=CurrentTime-ProcessesVectorResult[ReadyQueue[0].ID-1].ArrivalTime
#            plt.plot([CurrentTime,CurrentTime],[0,ProcessesVector[0].ID],color=ProcessesVector[0].Color)
#            #plt.pause(0.001)
#            ProcessesVector[0].BurstTime-=TimeStep
#        elif(ProcessesVector[0].BurstTime<=0):
#            ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime=CurrentTime-ProcessesVectorResult[ReadyQueue[0].ID-1].ArrivalTime-TimeStep
#            ProcessesVectorResult[ReadyQueue[0].ID-1].WeightedTurnaroundTime=ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime / ProcessesVectorResult[ReadyQueue[0].ID-1].BurstTime
#            ProcessesVector.pop(0)
#            i+=1
#            continue
#        CurrentTime+=TimeStep
#    plt.show()
#    return ProcessesVectorResult

#def RR(ProcessesVector,Quantum,Context):
#    ProcessesVector = sorted(ProcessesVector, key=lambda process: (process.ArrivalTime))
#    ProcessesVectorResult=copy.deepcopy(ProcessesVector)
#    CurrentTime=0
#    plt.title('Round Robin')
#    plt.ylabel('Process ID')
#    plt.xlabel('Time')
#    Ticks=np.arange(0,len(ProcessesVector)+1,1)
#    plt.yticks(Ticks)
#    plt.grid(True)
#    q=Quantum
#    i=0
#    j=0
#    ReadyQueue=[]
#    while (len(ReadyQueue)>0 or len(ProcessesVector) > 0):
#        if(len(ReadyQueue)>0):
#            if (q<=0):
#                ReadyQueue.append(ReadyQueue.pop(0))
#                q=Quantum
#                continue
#            elif(ReadyQueue[0].BurstTime<=0):
#                ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime=CurrentTime-ProcessesVectorResult[ReadyQueue[0].ID-1].ArrivalTime-0.1
#                ProcessesVectorResult[ReadyQueue[0].ID-1].WeightedTurnaroundTime=ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime / ProcessesVectorResult[ReadyQueue[0].ID-1].BurstTime
#                ReadyQueue.pop(0)
#                i+=1
#            elif(ReadyQueue[0].BurstTime>0 and q>0):
#                if(ReadyQueue[0].WaitingTime==-1):
#                    ProcessesVectorResult[ReadyQueue[0].ID-1].WaitingTime=CurrentTime-ProcessesVectorResult[ReadyQueue[0].ID-1].ArrivalTime
#                q-=0.1
#                plt.plot([CurrentTime,CurrentTime],[0,ReadyQueue[0].ID],color=ReadyQueue[0].Color)
#                ReadyQueue[0].BurstTime-=0.1
#        if(len(ProcessesVector)>0):
#            if(ProcessesVector[0].ArrivalTime<=CurrentTime):
#                ReadyQueue.append(ProcessesVector.pop(0))
#        CurrentTime+=0.1
#    plt.show()
#    return ProcessesVectorResult