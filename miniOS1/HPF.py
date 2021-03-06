import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import filedialog
import copy
import numpy as np

def HPF(ProcessesVector,Context,TimeStep):
    ProcessesVectorResult=copy.deepcopy(ProcessesVector)
    ProcessesVector = sorted(ProcessesVector, key=lambda process: (process.ArrivalTime))
    ReadyQueue=[]
    CurrentTime=0
    C=Context
    plt.title('Non-Preemptive Highest Priority First')
    plt.ylabel('Process ID')
    plt.xlabel('Time')
    Ticks=np.arange(0,len(ProcessesVector)+1,1)
    plt.yticks(Ticks)
    x =[]
    width_ =[]
    color_=[]
    y= []
    while (len(ReadyQueue)>0 or len(ProcessesVector) > 0):
        while(len(ProcessesVector)>0 and ProcessesVector[0].ArrivalTime<=CurrentTime):
            ReadyQueue.append(ProcessesVector.pop(0))

        if(len(ReadyQueue)>0):
            if(ReadyQueue[0].BurstTime>0 ):
                if(ReadyQueue[0].firstStart==-1):
                    ReadyQueue[0].set_firstStart(CurrentTime)
                ReadyQueue[0].BurstTime-=TimeStep
            elif(ReadyQueue[0].BurstTime<=0):
                ReadyQueue[0].set_lastEnd(CurrentTime)
                ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime=CurrentTime-ProcessesVectorResult[ReadyQueue[0].ID-1].ArrivalTime-TimeStep
                ProcessesVectorResult[ReadyQueue[0].ID-1].WeightedTurnaroundTime=ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime / ProcessesVectorResult[ReadyQueue[0].ID-1].BurstTime
                ProcessesVectorResult[ReadyQueue[0].ID-1].WaitingTime=ProcessesVectorResult[ReadyQueue[0].ID-1].TurnaroundTime - ProcessesVectorResult[ReadyQueue[0].ID-1].BurstTime
                
                x.append(ReadyQueue[0].firstStart)
                y.append(ReadyQueue[0].ID)
                color_.append(ReadyQueue[0].Color)
                width_.append(ReadyQueue[0].lastEnd-ReadyQueue[0].firstStart)

                ReadyQueue.pop(0)
                ReadyQueue = sorted(ReadyQueue, key=lambda process: (-1*process.Priority,process.ID))
                if len(ReadyQueue)>0:
                    CurrentTime+=Context
                continue
        CurrentTime+=TimeStep

    plt.xticks(np.arange(0,CurrentTime,50))
    plt.bar(x,height=y,width=width_,color=color_,align='edge',linewidth=0.5,edgecolor='k')
    plt.grid(axis='y',color='gray',linestyle='dashed')
    plt.show()
    return ProcessesVectorResult