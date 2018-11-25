from tkinter import filedialog
from tkinter import messagebox
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import Scheduler
import sys
import copy

class Process:
    def __init__(self,id,arrival,burst,p,color):
        self.ID=id
        self.ArrivalTime=arrival
        self.BurstTime=burst
        self.Priority=p
        self.WaitingTime=-1
        self.TurnaroundTime=-1
        self.WeightedTurnaroundTime=-1
        self.Color=color
        self.firstStart=-1
        self.lastEnd=-1
    def set_firstStart(self,firstStart):
        self.firstStart=firstStart
    def set_lastEnd(self,lastEnd):
        self.lastEnd=lastEnd

def printVector(ProcessesVector):
    for process in ProcessesVector:
        print("Process: "+str(process.ID)+"\tAT: "+str(process.ArrivalTime)+"\tBT: "+str(process.BurstTime)+
            "\tPriority: "+str(process.Priority))

def takeInputProcesses(OriginalProcessesVector):
    global InputFileName
    InputFile  = open(InputFileName,'r') 
    NumberOfProcesses=0
    cmap = plt.get_cmap('nipy_spectral')
    i=0
    MinStepBurstIndex=0
    MinStepArrivalIndex=0
    for line in InputFile:
        newProcess=line.split()
        if len(newProcess) == 1:
            NumberOfProcesses=int(newProcess[0])
            colors = cmap(np.linspace(0, 1, NumberOfProcesses))
            continue
        if len(newProcess) != 4:
            messagebox.showerror("ERROR", "Invalid data in line : "+str(i))
            sys.exit()

        OriginalProcessesVector.append(Process(int(newProcess[0]),float(newProcess[1]),float(newProcess[2]),int(newProcess[3]),colors[i]))
        i+=1

    MinStepBurst=min(OriginalProcessesVector,key=lambda item:item.BurstTime)
    MinStepArrival=min(OriginalProcessesVector,key=lambda item:item.BurstTime)
    MinStepArrival=MinStepArrival.ArrivalTime
    MinStepBurst=MinStepBurst.BurstTime
    MinStepArrival=MinStepArrival-int(MinStepArrival)
    MinStepBurst=MinStepBurst-int(MinStepBurst)
    
    return min(MinStepBurst,MinStepArrival)
   
def printOutputFile(ProcessesVectorResults):
    OutputFileName  =filedialog.asksaveasfilename(defaultextension=".txt",title = "Save file",filetypes = (("Text Files","*.txt"),))
    OutputFile= open(OutputFileName,'w');
    AVGWeightedTurnaroundTime=0
    AVGTurnaroundTime=0
    for process in ProcessesVectorResults:
        AVGTurnaroundTime+=process.TurnaroundTime
        AVGWeightedTurnaroundTime+=process.WeightedTurnaroundTime
        OutputFile.writelines('Process ID: '+str(process.ID)+'\tWaiting Time: '+max(0,str(process.WaitingTime))+
                                '\tTurnaround Time: '+str(process.TurnaroundTime)+'\tWeighted Turnaround Time :'+str(process.WeightedTurnaroundTime)+'\n')
    
    OutputFile.writelines('\n\nAverage Turnaround Time: '+str(AVGTurnaroundTime/len(ProcessesVectorResults))+'\nAverage Weighted Turnaround Time: '+
                            str(AVGWeightedTurnaroundTime/len(ProcessesVectorResults)))
    OutputFile.close()
    
#-----------------Callbacks-----------------#
def chooseInputFileButtonCallback(InputFileText):
    global InputFileName
    InputFileText.config(state=NORMAL)
    InputFileNameOld=InputFileName
    InputFileName= filedialog.askopenfilename(defaultextension='.txt',title = "Select file",filetypes = (("Text Files","*.txt"),))
    if(not InputFileName):
        InputFileName=InputFileNameOld
    InputFileText.delete(0,END)
    InputFileText.insert(0,InputFileName)
    InputFileText.config(state=DISABLED)

def drawButtonCallback():
    global var
    global OriginalProcessesVector
    global InputFileText

    ProcessesVector=[]
    ProcessesVectorResults=[]
    TimeStep=0.0
    #Take input from the generator file
    if(InputFileText.get()==''):
        messagebox.showerror("ERROR", "Please choose the input file first")
        return

    if(InputContextSwitching.get()== ''):
        messagebox.showerror("ERROR", "Please enter the context switching time first")
        return

    if not len(OriginalProcessesVector):
        TimeStep=takeInputProcesses(OriginalProcessesVector)
    if (TimeStep == 0 or TimeStep < 0.05):
        TimeStep=0.1
    ProcessesVector= copy.deepcopy(OriginalProcessesVector)
    if var.get() == 1:
        ProcessesVectorResults=Scheduler.HPF(ProcessesVector,float(InputContextSwitching.get()),TimeStep)
    elif var.get() == 2:
         ProcessesVectorResults=FCFS(ProcessesVector,float(InputContextSwitching.get()))
    elif var.get() == 3:
        if(InputTimeQuantum.get()== ''):
            messagebox.showerror("ERROR", "Please enter the time quantum to perform Round Robin algorithm")
            return
        else:
           ProcessesVectorResults=RR(ProcessesVector,float(InputTimeQuantum.get()),float(InputContextSwitching.get()))
    elif var.get() == 4:
        ProcessesVectorResults=Scheduler.SRTN(ProcessesVector,float(InputContextSwitching.get()),TimeStep)
    result = messagebox.askquestion("Save", "Do you wanna save statistics file?")
    if(result == "yes"):
        printOutputFile(ProcessesVectorResults)

#-----------------Text Validations-----------------#
def validate(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.':
            try:
                return True
            except ValueError:
                return False
        else:
            return False

#-----------------Initialize Window-----------------#
def initWindow():    
    root = Tk(className='welcome')
    global var
    var = IntVar()
    root.geometry("520x260")
    root.resizable(0,0)

    #Upper Frame
    L1= Label(root,text="File Directory: ")
    L1.place(relx = 0.05,rely=0.15)
    global InputFileText 
    InputFileText = Entry(root)
    InputFileText.place(relx=0.21,rely=0.16,width=300)
    InputFileText.config(state=DISABLED)
    ChooseInputFileButton= Button(root,text='Browse',command=lambda :chooseInputFileButtonCallback(InputFileText))
    ChooseInputFileButton.place(relx=0.82,rely=0.15)

    #Middle Frame
    Algos=[Radiobutton(root,text='Highest Priority First (HPF)',variable=var,value=1),
            Radiobutton(root,text='First Come First Serve (FCFS)',variable=var,value=2),
            Radiobutton(root,text='Round Robin (RR)',variable=var,value=3),
            Radiobutton(root,text='Shortest Running Time First (SRTF)',variable=var,value=4)]

    Algos[0].place(relx=0.12,rely=0.35)
    Algos[1].place(relx=0.5,rely=0.35)
    Algos[2].place(relx=0.12,rely=0.55)
    Algos[3].place(relx=0.5,rely=0.55)

    #Bottom Frame
    L2=Label(root,text="Context Switching: ")
    L2.place(relx=0.15,rely=0.71)

    global InputContextSwitching
    vcmd = (root.register(validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    InputContextSwitching = Entry(root,validate = 'key', validatecommand = vcmd)
    InputContextSwitching.place(relx=0.36,rely=0.72,width=50)

    L3=Label(root,text="Time Quantum: ")
    L3.place(relx=0.5,rely=0.71)
    global InputTimeQuantum
    InputTimeQuantum = Entry(root,validate = 'key', validatecommand = vcmd)
    InputTimeQuantum.place(relx=0.68,rely=0.71,width=50)

    DrawButton =Button(root,text='Draw',command=drawButtonCallback)
    DrawButton.place(relx=0.42,rely=0.85,width=80)
    return root

InputFileName=''
OutputFileName=''
OriginalProcessesVector=[]

root=initWindow()
root.mainloop()