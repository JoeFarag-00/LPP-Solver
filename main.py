from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from decimal import *
import math as mth
import matplotlib.pyplot as pl
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import pandas as pd
import openpyxl as Excel
import numpy as np
import random as rnd
import os
np.seterr(divide='ignore')
class LPP_Solver:
    
    def __init__(self, root):
        self.root = root
        self.root.geometry("1460x700")
        self.root.title("LPP Solver")
        title = Label(self.root, text="Linear Programming Problem Solver", font=('arial', 30, 'bold'), pady=2, bd=12, bg="#00C10C", fg="Black", relief=GROOVE)
        self.root.configure(bg='black')
        title.pack(fill=X)
    #--------------Initialization-------------#
        self.TypeMM=StringVar()
        MM=('Max','Min')
        self.str_Obj_Size=IntVar()
        self.str_Const_ct=IntVar()
        self.Begin = False
        self.DoOnce = False
        
        User_Entry_Frame = LabelFrame(root, text="Requirments", font=('arial', 14, 'bold'), bd=10, fg="Black", bg="#00C10C")
        User_Entry_Frame.place(x=0, y=80, relwidth=1)

        TypeMM_Lb = Label(User_Entry_Frame, text="Problem Type:", bg="#00C10C", font=('arial', 15, 'bold'))
        TypeMM_Lb.grid(row=0, column=0, padx=5, pady=5)
        self.TypeMM = ttk.Combobox(User_Entry_Frame, width=10,textvariable=self.TypeMM, font='arial 15')
        self.TypeMM['values']= MM
        self.TypeMM['state']= 'readonly'
        self.TypeMM.grid(row=0, column=1, pady=5, padx=10)

        Obj_Size_Lb = Label(User_Entry_Frame, text="Obj-Func Term Size:", bg="#00C10C", font=('arial', 15, 'bold'))
        Obj_Size_Lb.grid(row=0, column=2, padx=5, pady=5)
        self.str_Obj_Size = Spinbox(User_Entry_Frame, width=10,textvariable=self.str_Obj_Size, font='arial 15', bd=7, relief=GROOVE, from_=2,to=5)
        self.str_Obj_Size.grid(row=0, column=3, pady=5, padx=10)

        ConstAmount_Lb = Label(User_Entry_Frame, text="Amount of Constraints:", bg="#00C10C", font=('arial', 15, 'bold'))
        ConstAmount_Lb.grid(row=0, column=4, padx=5, pady=5)
        self.str_Const_ct = Spinbox(User_Entry_Frame, width=10,textvariable=self.str_Const_ct, font='arial 15', bd=7, relief=GROOVE, from_=1,to=6)
        self.str_Const_ct.grid(row=0, column=5, pady=5, padx=10)
            
        def Intialize_Requirements():
            if self.TypeMM.get() == "" :
                TypeMM_Lb.config(fg="Red")
            else:
                TypeMM_Lb.config(fg="#000000")
                self.Const_ct=int(self.str_Const_ct.get())
                self.Obj_Size=int(self.str_Obj_Size.get())
                GenerateConstBoxs()
                ShowSolveBtn()
        
        
        Start_Btn = Button(User_Entry_Frame, text="Start",command=Intialize_Requirements, width=10, bd=7, font=('arial', 12, 'bold'), relief=GROOVE)
        Start_Btn.grid(row=0, column=6, pady=5, padx=95)

        # ===================Objective Function & Constraints====================================
        Obj_Sec_Frame = LabelFrame(root, text="Objective Function & Constraints", font=('arial', 12, 'bold'), bd=10, fg="Black", bg="#FF8000")
        Obj_Sec_Frame.place(x=0, y=169, width=440, height=410)

        Obj_Lb = Label(Obj_Sec_Frame, text="Z=", font=('arial', 16, 'bold'), bg="#FF8000", fg="black")
        Obj_Lb.grid(row=0, column=0, padx=2, pady=10, sticky='W')
        Obj = Entry(Obj_Sec_Frame, width=18,  font=('arial', 16, 'bold'), bd=5, relief=GROOVE)
        Obj.grid(row=0, column=1, padx=0, pady=10)
        
        def GetObj():
            iB=''
            self.Obj_List = [0 for c in range(self.Obj_Size+(self.Obj_Size-1))]
            ObjFilter_List = Obj.get()
            for i in ObjFilter_List:
                if i.isalpha() and iB == "":
                    ObjFilter_List=ObjFilter_List.replace(i,'1')
                elif i.isalpha():
                    ObjFilter_List=ObjFilter_List.replace(i,"")
                iB=i
                
            ObjFilter_List = ObjFilter_List.split()
            for i in range(len(ObjFilter_List)):
                
                if i%2 == 0:
                    self.Obj_List[i]=float(ObjFilter_List[i])
                elif i%2 ==1 :
                    self.Obj_List[i]=ObjFilter_List[i]
            
            print("Objective Function:" , self.Obj_List)
            
        self.Const_List = []
        
        def GenerateConstBoxs():
            Ci=1
            Const_txt="Contraint #"
            for i in range(self.Const_ct):
                Const_Lb = Label(Obj_Sec_Frame, text=Const_txt + str(Ci), font=('arial', 16, 'bold'), bg="#FF8000", fg="black")
                Const_Lb.grid(row=i+1, column=0, padx=10, pady=5, sticky='W')
                Const = Entry(Obj_Sec_Frame, width=15, font=('arial', 16, 'bold'), bd=5, relief=GROOVE)
                Const.grid(row=i+1, column=1, padx=10, pady=5)
                self.Const_List.append(Const)
                Ci+=1
        
        def GetConstraints():
            iB=""
            self.Const_Mtrx = [[0 for c in range((self.Obj_Size+(self.Obj_Size-1))+2)]for r in range(len(self.Const_List))]
            F=0
            for r in range(len(self.Const_Mtrx)):
               
                ConstFilter_List = self.Const_List[r].get()
                iB = ""
                for i in ConstFilter_List:
                        
                    if i.isalpha() and iB == "":
                        ConstFilter_List=ConstFilter_List.replace(i,'1')
                    elif i.isalpha() and iB == " ":
                        ConstFilter_List=ConstFilter_List.replace(i,'1')                 
                    elif i.isalpha():
                        ConstFilter_List=ConstFilter_List.replace(i,"")
                    
                    iB = i

                ConstFilter_List=ConstFilter_List.split()
                
                for c in range(len(self.Const_Mtrx[r])):
                    
                    if c%2 == 0:
                       self.Const_Mtrx[r][c]=float(ConstFilter_List[c])
                    
                    elif c%2 == 1 :
                        self.Const_Mtrx[r][c]=ConstFilter_List[c]

            print("Constraints" ,self.Const_Mtrx)
            
        def SolveGraphicalMethod():
            self.ConstXY_List = [[0 for i in range(4)] for j in range(self.Const_ct)]
            BPoint1=[0,0]
            BPoint2=[0,0]
            isintersect=False
            intct=0
            for c in range(self.Const_ct):
                try:
                    self.ConstXY_List[c][0]=0
                    self.ConstXY_List[c][1]=self.Const_Mtrx[c][4]/self.Const_Mtrx[c][2]
                    self.ConstXY_List[c][2]=self.Const_Mtrx[c][4]/self.Const_Mtrx[c][0]
                    self.ConstXY_List[c][3]=0
                except ZeroDivisionError:
                    self.ConstXY_List[c][1]=0
                    self.ConstXY_List[c][2]=0
                
            for i in range(self.Const_ct):
                BPoint1=[self.ConstXY_List[i][0],self.ConstXY_List[i][1]]
                BPoint2=[self.ConstXY_List[i][2],self.ConstXY_List[i][3]]
                if(BPoint1[0] == 0 and BPoint1[1] == 0 and BPoint2[0] == 0 and BPoint2[1] == 0 and self.Const_Mtrx[i][0] == 0):
                    gplt.axhline(self.Const_Mtrx[i][4])
                elif(BPoint1[0] == 0 and BPoint1[1] == 0 and BPoint2[0] == 0 and BPoint2[1] == 0 and self.Const_Mtrx[i][2] == 0):
                    gplt.axvline(self.Const_Mtrx[i][4])
                else: 
                    gplt.plot(BPoint1,BPoint2,linestyle="-")
                    
                print("Constraint #",i,": ","P1: ",BPoint1,"\t", "P2: ",BPoint2)
                
            self.TempCvar_List = [[0 for c in range(2)] for r in range(self.Const_ct)]
            self.TempRhs_List = []
            self.insterPt = []
            
            if(self.TypeMM.get() == 'Max'):
                for r in range(self.Const_ct):
                     self.TempCvar_List[r][0] = self.Const_Mtrx[r][0]
                     self.TempCvar_List[r][1] = self.Const_Mtrx[r][2]
                     self.TempRhs_List.append(self.Const_Mtrx[r][4])
                
                print("\n")
                print("Fit Constraints: ",self.TempCvar_List)
                print("RHS: ",self.TempRhs_List)
                print("\n")   
                print("Points: ",self.ConstXY_List)
                if(self.Obj_Size == 2):

                    for ir in range(self.Const_ct):
                        TryInter_List = [0 for c in range(2)]
                        TryRhs_List = [0,0]                        
                        TryInter_List[0]=self.TempCvar_List[ir]
                        TryRhs_List[0]=self.TempRhs_List[ir]
                        ic=ir+1
                        for ic in range(ic,self.Const_ct):
                            TryInter_List[1]=self.TempCvar_List[ic]
                            TryRhs_List[1]=self.TempRhs_List[ic]
                            try:
                                SysSol = np.linalg.solve(TryInter_List, TryRhs_List)
                                self.insterPt.append(SysSol)
                            except:
                                print("No Intersections")
                    
                    print("Intersection Points: ",self.insterPt)
                    
                    self.ZTable = [[0 for c in range(2)] for r in range(len((self.ConstXY_List)*2)+len(self.insterPt))]
                         
                    r=0                
                    for n in range(len(self.ConstXY_List)):
                        self.ZTable[r]=[self.ConstXY_List[n][0],self.ConstXY_List[n][1]]
                        r+=1
                        self.ZTable[r]=[self.ConstXY_List[n][2],self.ConstXY_List[n][3]]
                        r+=1    
                    strp=r-1  
                    n=0
                
                    print("\n")         
                    print("Adjusted Data Points")      
                    
                    #CLEAN INTERCEPT
                    maxIt=0
                    IntShelve_List=[]
                    CleanInt_List=self.insterPt
                    for i in range(len(CleanInt_List)):
                        IntShelve_List.append(CleanInt_List[i][0]+CleanInt_List[i][1])

                    if(len(CleanInt_List)==3):
                        maxIt=max(IntShelve_List)
                        for i in range(len(IntShelve_List)):
                            if(IntShelve_List[i]==maxIt):
                                del CleanInt_List[i]
                            
                    print("\n")
                    print("Valid intersections: ",CleanInt_List) 
                    
                    #CLEAN POIUNTS
                    self.CleanPoints_List=self.ZTable
                    print("Valid Points: ", self.CleanPoints_List)
                    catchmaxp=0
                    rp=0
                    for i in range(len(self.insterPt)):
                        self.CleanPoints_List.pop()
            
                    SortCleanPoints_List = sorted(self.CleanPoints_List, key=lambda x: sum(x))
                    
                    tp=int(len(SortCleanPoints_List)/2)
                    
                    for i in range(tp):
                        SortCleanPoints_List.pop()
                    
                    #reset
                    self.CleanPoints_List=[]
                    for n in self.CleanPoints_List:
                        if sum(n) not in [sum(x) for x in self.CleanPoints_List]:
                            self.CleanPoints_List.append(n)
                
                    IntBridge=[[0 for c in range(2)] for r in range(len(CleanInt_List))]
                    
                    n=0
                    for z in range(len(CleanInt_List)):
                        IntBridge[z]=[CleanInt_List[n][0],CleanInt_List[n][1]]
                        self.CleanPoints_List.append(IntBridge[z])
                        n+=1

                    print("Possible Optimal Points ", self.CleanPoints_List) 
                    
                    self.MaxZ_List=[]
                    self.FinalMaxZ=None
                    if(self.Obj_List[1] == "+"):
                        for n in range(len(self.CleanPoints_List)):
                           objsave=[self.Obj_List[0],self.Obj_List[2]]
                           objsave[0]=self.Obj_List[0]*self.CleanPoints_List[n][0]
                           objsave[1]=self.Obj_List[2]*self.CleanPoints_List[n][1]
                           
                           self.MaxZ_List.append(objsave[0]+objsave[1])
                    elif(self.Obj_List[1] == "-"):
                        for n in range(len(self.CleanPoints_List)):
                           objsave=[self.Obj_List[0],self.Obj_List[2]]
                           objsave[0]=self.Obj_List[0]*self.CleanPoints_List[n][0]
                           objsave[1]=self.Obj_List[2]*self.CleanPoints_List[n][1]
                           
                           self.MaxZ_List.append(objsave[0]-objsave[1])
                    
                    self.FinalMaxZ=max(self.MaxZ_List)
                    catchp=self.MaxZ_List.index(self.FinalMaxZ)
                    
                    
                    
                    
                    print("Optimal Point:",catchp)
                    print("Optimal Solution: ",self.FinalMaxZ)
                    # ZResult.set(self.FinalMaxZ)
                    # PResult.set(self.CleanPoints_List)
            
            if(self.TypeMM.get() == 'Min'):
                for r in range(self.Const_ct):
                     self.TempCvar_List[r][0] = self.Const_Mtrx[r][0]
                     self.TempCvar_List[r][1] = self.Const_Mtrx[r][2]
                     self.TempRhs_List.append(self.Const_Mtrx[r][4])
                
                print("\n")
                print("Fit Constraints: ",self.TempCvar_List)
                print("RHS: ",self.TempRhs_List)
                print("\n")   
                print("Points: ",self.ConstXY_List)
                if(self.Obj_Size == 2):

                    for ir in range(self.Const_ct):
                        TryInter_List = [0 for c in range(2)]
                        TryRhs_List = [0,0]                        
                        TryInter_List[0]=self.TempCvar_List[ir]
                        TryRhs_List[0]=self.TempRhs_List[ir]
                        ic=ir+1
                        for ic in range(ic,self.Const_ct):
                            TryInter_List[1]=self.TempCvar_List[ic]
                            TryRhs_List[1]=self.TempRhs_List[ic]
                            try:
                                SysSol = np.linalg.solve(TryInter_List, TryRhs_List)
                                self.insterPt.append(SysSol)
                            except:
                                print("No Intersections")
                    
                    print("Intersection Points: ",self.insterPt)
                    
                    self.ZTable = [[0 for c in range(2)] for r in range(len((self.ConstXY_List)*2)+len(self.insterPt))]
                         
                    r=0                
                    for n in range(len(self.ConstXY_List)):
                        self.ZTable[r]=[self.ConstXY_List[n][0],self.ConstXY_List[n][1]]
                        r+=1
                        self.ZTable[r]=[self.ConstXY_List[n][2],self.ConstXY_List[n][3]]
                        r+=1    
                    strp=r-1  
                    n=0
                
                    print("\n")         
                    print("Adjusted Data Points")      
                    
                    #CLEAN INTERCEPT
                    maxIt=0
                    IntShelve_List=[]
                    CleanInt_List=self.insterPt
                    for i in range(len(CleanInt_List)):
                        IntShelve_List.append(CleanInt_List[i][0]+CleanInt_List[i][1])

                    if(len(CleanInt_List)==3):
                        maxIt=min(IntShelve_List)
                        for i in range(len(IntShelve_List)):
                            if(IntShelve_List[i]==maxIt):
                                del CleanInt_List[i]
                            
                    print("\n")
                    print("Valid intersections: ",CleanInt_List) 
                    
                    #CLEAN POIUNTS
                    self.CleanPoints_List=self.ZTable
                    print("Valid Points: ", self.CleanPoints_List)
                    catchmaxp=0
                    rp=0
                    for i in range(len(self.insterPt)):
                        self.CleanPoints_List.pop()
            
                    SortCleanPoints_List = sorted(self.CleanPoints_List, key=lambda x: sum(x))
                    
                    tp=int(len(SortCleanPoints_List)/2)
                    
                    for i in range(tp):
                        SortCleanPoints_List.pop()
                    
                    #reset
                    self.CleanPoints_List=[]
                    for n in self.CleanPoints_List:
                        if sum(n) not in [sum(x) for x in self.CleanPoints_List]:
                            self.CleanPoints_List.append(n)
                
                    IntBridge=[[0 for c in range(2)] for r in range(len(CleanInt_List))]
                    
                    n=0
                    for z in range(len(CleanInt_List)):
                        IntBridge[z]=[CleanInt_List[n][0],CleanInt_List[n][1]]
                        self.CleanPoints_List.append(IntBridge[z])
                        n+=1

                    print("Cross-Section Optimal Points ", self.CleanPoints_List) 
                    
                    self.MaxZ_List=[]
                    self.FinalMaxZ=None
                    if(self.Obj_List[1] == "+"):
                        for n in range(len(self.CleanPoints_List)):
                           objsave=[self.Obj_List[0],self.Obj_List[2]]
                           objsave[0]=self.Obj_List[0]*self.CleanPoints_List[n][0]
                           objsave[1]=self.Obj_List[2]*self.CleanPoints_List[n][1]
                           
                           self.MaxZ_List.append(objsave[0]+objsave[1])
                    elif(self.Obj_List[1] == "-"):
                        for n in range(len(self.CleanPoints_List)):
                           objsave=[self.Obj_List[0],self.Obj_List[2]]
                           objsave[0]=self.Obj_List[0]*self.CleanPoints_List[n][0]
                           objsave[1]=self.Obj_List[2]*self.CleanPoints_List[n][1]
                           
                           self.MaxZ_List.append(objsave[0]-objsave[1])
                    
                    self.FinalMaxZ=min(self.MaxZ_List)
                    catchp=self.MaxZ_List.index(self.FinalMaxZ)
                    
                    print("Optimal Point:",catchp)
                    print("Optimal Solution: ",self.FinalMaxZ)
                    # ZResult.set(self.FinalMaxZ)
                    # PResult.set(self.CleanPoints_List)

        def Load_AllOC():
            self.Begin = True
            GetObj()
            GetConstraints()
            print('\n')
            if(self.Obj_Size<=2):
                SolveGraphicalMethod()
                Permit_Simplex()
                Get_FR()
                
            elif(self.Obj_Size>=2):
                
                SolveSimplexMethod()
            
        def Get_FR():
            if(self.Obj_Size <= 2):
                Dlook = np.linspace(-2,16,300)
                X,Y = np.meshgrid(Dlook,Dlook)
                if(self.Const_Mtrx[0][1] == "+" and self.Const_Mtrx[1][1] == "+" and self.Const_Mtrx[0][3] == "<=" and self.Const_Mtrx[1][3] == "<="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X+self.Const_Mtrx[0][2]*Y<=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X+self.Const_Mtrx[1][2]*Y<=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)
                
                if(self.Const_Mtrx[0][1] == "+" and self.Const_Mtrx[1][1] == "+" and self.Const_Mtrx[0][3] == "<=" and self.Const_Mtrx[1][3] == ">="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X+self.Const_Mtrx[0][2]*Y<=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X+self.Const_Mtrx[1][2]*Y>=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)
                
                if(self.Const_Mtrx[0][1] == "+" and self.Const_Mtrx[1][1] == "+" and self.Const_Mtrx[0][3] == ">=" and self.Const_Mtrx[1][3] == "<="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X+self.Const_Mtrx[0][2]*Y>=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X+self.Const_Mtrx[1][2]*Y<=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "+" and self.Const_Mtrx[1][1] == "+" and self.Const_Mtrx[0][3] == ">=" and self.Const_Mtrx[1][3] == ">="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X+self.Const_Mtrx[0][2]*Y>=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X+self.Const_Mtrx[1][2]*Y>=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "+" and self.Const_Mtrx[1][1] == "-" and self.Const_Mtrx[0][3] == "<=" and self.Const_Mtrx[1][3] == "<="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X+self.Const_Mtrx[0][2]*Y<=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X-self.Const_Mtrx[1][2]*Y<=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "+" and self.Const_Mtrx[1][1] == "-" and self.Const_Mtrx[0][3] == "<=" and self.Const_Mtrx[1][3] == ">="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X+self.Const_Mtrx[0][2]*Y<=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X-self.Const_Mtrx[1][2]*Y>=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "+" and self.Const_Mtrx[1][1] == "-" and self.Const_Mtrx[0][3] == ">=" and self.Const_Mtrx[1][3] == "<="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X+self.Const_Mtrx[0][2]*Y>=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X-self.Const_Mtrx[1][2]*Y<=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "+" and self.Const_Mtrx[1][1] == "-" and self.Const_Mtrx[0][3] == ">=" and self.Const_Mtrx[1][3] == ">="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X+self.Const_Mtrx[0][2]*Y>=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X-self.Const_Mtrx[1][2]*Y>=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       

                if(self.Const_Mtrx[0][1] == "-" and self.Const_Mtrx[1][1] == "+" and self.Const_Mtrx[0][3] == "<=" and self.Const_Mtrx[1][3] == "<="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X-self.Const_Mtrx[0][2]*Y<=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X+self.Const_Mtrx[1][2]*Y<=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "-" and self.Const_Mtrx[1][1] == "+" and self.Const_Mtrx[0][3] == "<=" and self.Const_Mtrx[1][3] == ">="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X-self.Const_Mtrx[0][2]*Y<=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X+self.Const_Mtrx[1][2]*Y>=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "-" and self.Const_Mtrx[1][1] == "+" and self.Const_Mtrx[0][3] == ">=" and self.Const_Mtrx[1][3] == "<="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X-self.Const_Mtrx[0][2]*Y>=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X+self.Const_Mtrx[1][2]*Y<=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "-" and self.Const_Mtrx[1][1] == "+" and self.Const_Mtrx[0][3] == ">=" and self.Const_Mtrx[1][3] == ">="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X-self.Const_Mtrx[0][2]*Y>=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X+self.Const_Mtrx[1][2]*Y>=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "-" and self.Const_Mtrx[1][1] == "-" and self.Const_Mtrx[0][3] == "<=" and self.Const_Mtrx[1][3] == "<="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X-self.Const_Mtrx[0][2]*Y<=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X-self.Const_Mtrx[1][2]*Y<=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "-" and self.Const_Mtrx[1][1] == "-" and self.Const_Mtrx[0][3] == "<=" and self.Const_Mtrx[1][3] == ">="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X-self.Const_Mtrx[0][2]*Y<=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X-self.Const_Mtrx[1][2]*Y>=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "-" and self.Const_Mtrx[1][1] == "-" and self.Const_Mtrx[0][3] == ">=" and self.Const_Mtrx[1][3] == "<="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X-self.Const_Mtrx[0][2]*Y>=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X-self.Const_Mtrx[1][2]*Y<=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
                
                if(self.Const_Mtrx[0][1] == "-" and self.Const_Mtrx[1][1] == "-" and self.Const_Mtrx[0][3] == ">=" and self.Const_Mtrx[1][3] == ">="):
                    gplt.imshow( ((self.Const_Mtrx[0][0]*X-self.Const_Mtrx[0][2]*Y>=self.Const_Mtrx[0][4]) & (self.Const_Mtrx[1][0]*X-self.Const_Mtrx[1][2]*Y>=self.Const_Mtrx[1][4])).astype(int) , extent=(X.min(),X.max(),Y.min(),Y.max()),origin="lower", cmap="Greys", alpha = 0.3)                                                       
            
                print("\n")
                pl.show()
            
        # ===========Graphical Visualization================================
        Graph_Frame = LabelFrame(root, text="Graphical Visualization", font=('Arial', 15, 'bold'), bd=10, fg="Black", bg="#AAAAAA")
        Graph_Frame.place(x=440, y=169, width=360, height=410)
        
        plt = Figure(figsize = (5.4, 3.4),dpi = 100)
        gplt = plt.add_subplot(111)
        canvas = FigureCanvasTkAgg(plt,Graph_Frame)  
        toolbar = NavigationToolbar2Tk(canvas,Graph_Frame)
        toolbar.update()
        canvas.get_tk_widget().pack()
        # =================Simplex Tab======================
        Simplex_txtarea_Frame = Frame(self.root, bd=10, relief=GROOVE,bg="#AAAAAA")
        Simplex_txtarea_Frame.place(x=800, y=170, width=660, height=410)
        
        Simplex_Lb = Label(Simplex_txtarea_Frame, text="Simplex Tableau", font='arial 15 bold', bd=7,bg="#AAAAAA", relief=GROOVE)
        Simplex_Lb.pack(fill=X)
        scroll_y = Scrollbar(Simplex_txtarea_Frame, orient=VERTICAL)
        Simplex_txtarea = Text(Simplex_txtarea_Frame, yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=Simplex_txtarea.yview)
        Simplex_txtarea.pack(fill=BOTH, expand=1)
        
        Simplex_txtarea.insert(END, "\t Simplex Method Not Available")
        Simplex_txtarea.insert(END, f"\n")
        Simplex_txtarea.insert(END, f"\nObjective Function: Error")
        Simplex_txtarea.insert(END, f"\nConstraints: Error")
        Simplex_txtarea.insert(END, f"\n=============================================================================")
        
        def SolveSimplexMethod():
            
            Simplex_txtarea.delete("1.0", "end")
            Simplex_txtarea.insert(END, "\t\tSimplex is Available...")
            Simplex_txtarea.insert(END, f"\n")
            Simplex_txtarea.insert(END, f"\nObjective Function: Z = {Obj.get()}")
            for i in range(self.Const_ct):
                Simplex_txtarea.insert(END, f"\nConstraint {i}: {self.Const_List[i].get()}")
            Simplex_txtarea.insert(END, f"\n=========================================================================")
            Simplex_txtarea.insert(END, f"\n\t\tIntial Tableau")
            
            SimplexObj=[0 for c in range(self.Obj_Size+self.Const_ct)]
            
            Tableau=[[0 for c in range(self.Const_ct+self.Obj_Size)]for r in range(self.Const_ct)]
            Cb = [0 for c in range(self.Const_ct)]
            Quant = [0 for c in range(self.Const_ct)]
            Zj = [0 for c in range((self.Const_ct+self.Obj_Size)+1)]
            Cj_Zj = [0 for c in range(self.Const_ct+self.Obj_Size)]
            Ratio = [0 for c in range(len(Quant))]
            self.isDone = True
            
            self.SimplexCvar_List = [[0 for c in range(self.Obj_Size)] for r in range(self.Const_ct)]
            self.SimplexRhs_List = []
        
            for r in range(self.Const_ct):
                inc=0
                for c in range(len(self.Const_Mtrx[0])-1):
                    if c%2 == 0:
                        self.SimplexCvar_List[r][inc] = self.Const_Mtrx[r][c]
                        inc+=1
                        
                self.SimplexRhs_List.append(self.Const_Mtrx[r][len(self.Const_Mtrx[r])-1])
            
            inciden = 0
            r=0
            for c in range(self.Obj_Size,len(SimplexObj)):   
                Tableau[r][c] = 1     
                r+=1
            
            j=0
            for i in range(len(self.Obj_List)):
                if i%2 == 0:
                    SimplexObj[j]=self.Obj_List[i]
                    j+=1
            dist=j
            for k in range(self.Const_ct):
                SimplexObj[dist]=0
                dist=j+1

            cr2=0 
            for n in range(self.Const_ct):
                cr2=0
                for i in range(self.Obj_Size):
                    
                    Tableau[n][cr2]=self.SimplexCvar_List[n][i]
                    cr2+=1

            for r in range(self.Const_ct):
                Quant[r]=self.SimplexRhs_List[r]

            for i in range(len(Cb)):
                Cb[i]=0          

            for i in range(len(Zj)):
                Zj[i]=0                
            
            Iteration=0

            j=0
            for i in range(len(self.Obj_List)):
                if i%2 == 0:
                    Cj_Zj[j]=self.Obj_List[i]
                    j+=1
                
            for i in range(len(Ratio)):
                Ratio[i]=0   
            
            Simplex_txtarea.insert(END, f"\n\n")
            Simplex_txtarea.insert(END, f"\n \t {SimplexObj}")
            Simplex_txtarea.insert(END, f"\n    ======================================")
            for i in range(self.Const_ct):
                Simplex_txtarea.insert(END, f"\n {Cb[i]} | {Tableau[i]} | {Quant[i]} {Ratio[i]}")
            Simplex_txtarea.insert(END, f"\n    ======================================")
            Simplex_txtarea.insert(END, f"\n Zj|{Zj}")
            Simplex_txtarea.insert(END, f"\n Zj-Cj|{Cj_Zj}")
            
            self.isDone=False
            while(self.isDone == False):
                Zj_CjMax=max(Cj_Zj)
                ICpivot=Cj_Zj.index(Zj_CjMax)
                
                for r in range(len(Ratio)):
                    try:
                        Ratio[r]=(Quant[r]/Tableau[r][ICpivot])
                    except:
                        Ratio[r]=0
                    
                
                Rmin=min(Ratio)
                IRpivot=Ratio.index(Rmin)
                
                Cb[IRpivot]=SimplexObj[ICpivot]
                
                FinalKey=Tableau[IRpivot][ICpivot]
                
                for r in range(len(Tableau[0])):
                    Tableau[IRpivot][r]/=FinalKey
                        
                Quant[IRpivot]/=FinalKey

                for r in range(self.Const_ct):
                    niga=Tableau[r][ICpivot]*-1
                    if(r!=IRpivot):
                        Quant[r]+=Quant[IRpivot]*niga
                        for c in range(len(Tableau[0])):
                            Tableau[r][c]+=Tableau[IRpivot][c]*niga
                
                
                for c in range(len(Zj)):
                    TmpZj=0
                    for r in range(self.Const_ct):
                        if(c == len(Zj)-1):
                            TmpZj+=Quant[r]*Cb[r]
                        else:
                           TmpZj+=Cb[r]*Tableau[r][c]
                    Zj[c]=TmpZj
                
                for c in range(len(Cj_Zj)):
                    Cj_Zj[c]=SimplexObj[c]-Zj[c]
                
                Iteration+=1
                print("\n") 
                print("Iteration:", Iteration)
                print(Tableau)
                Simplex_txtarea.insert(END, f"\n \n \n \n \n Iteration: {Iteration}")
                Simplex_txtarea.insert(END, f"\n \t {SimplexObj}")
                Simplex_txtarea.insert(END, f"\n    ======================================")
                for i in range(self.Const_ct):
                    Simplex_txtarea.insert(END, f"\n {Cb[i]} | {Tableau[i]} | {Quant[i]} {Ratio[i]}")
                Simplex_txtarea.insert(END, f"\n    ======================================")
                Simplex_txtarea.insert(END, f"\n Zj|{Zj}")
                Simplex_txtarea.insert(END, f"\n Zj-Cj|{Cj_Zj}")
                
                self.isDone=True
                for i in range(len(Cj_Zj)):
                    if(Cj_Zj[i] > 0):
                        self.isDone = False
            
            print("Optimal Solution: ", len(Zj)-1 )
            

        def Permit_Simplex():
    
            Simplex_txtarea.delete("1.0", "end")
            Simplex_txtarea.insert(END, "\t\tSimplex is Available...")
            Simplex_txtarea.insert(END, f"\n")
            Simplex_txtarea.insert(END, f"\nObjective Function: Z = {Obj.get()}")
            for i in range(self.Const_ct):
                Simplex_txtarea.insert(END, f"\nConstraint {i}: {self.Const_List[i].get()}")
            Simplex_txtarea.insert(END, f"\n====================================================")
        
        # =======================ButtonFrame=============
        Result_Lb = LabelFrame(self.root, text="Results", font=('arial', 14, 'bold'), bd=10, fg="Black", bg="#13B10F")
        Result_Lb.place(x=0, y=578, relwidth=1, height=120)

        Result1_Lb = Label(Result_Lb, text="Z", font=('Arial', 14, 'bold'), bg="#13B10F", fg="black")
        Result1_Lb.grid(row=0, column=0, padx=20, pady=1, sticky='W')
        ZResult = Entry(Result_Lb, width=40,  font='arial 10 bold', bd=7, relief=GROOVE)
        ZResult.grid(row=0, column=1, padx=18, pady=5)
        
        
        Result2_Lb = Label(Result_Lb, text="Points", font=('Arial', 14, 'bold'), bg="#13B10F", fg="black")
        Result2_Lb.grid(row=1, column=0, padx=20, pady=1, sticky='W')
        PResult = Entry(Result_Lb, width=40 ,font='arial 10 bold', bd=7, relief=GROOVE)
        PResult.grid(row=1, column=1, padx=18, pady=5)
        #------------------solve Frame----------------------------
        def Reset_LPP():
            root.destroy()
            os.system('Main.py')
       
        def ShowSolveBtn():      
            FinalRun_Frame = Frame(Result_Lb, bd=7,bg="black", relief=GROOVE)
            FinalRun_Frame.place(x=900, width=435, height=90)
        
            Solve_Btn = Button(FinalRun_Frame, text="Solve", bg="#13B10F",command=Load_AllOC, bd=2, fg="black", pady=15, width=12, font='arial 13 bold')
            Solve_Btn.grid(row=0, column=0, padx=5, pady=5)
            
            Simplex_Btn = Button(FinalRun_Frame, text="Run Simplex", command=SolveSimplexMethod, bd=2, bg="#FF9300", fg="black", pady=12, width=12, font='arial 13 bold')
            Simplex_Btn.grid(row=0, column=1, padx=5, pady=5)

            Exit_Btn = Button(FinalRun_Frame, text="Reset", command=Reset_LPP,bd=2, bg="red", fg="black", pady=15, width=12, font='arial 13 bold')
            Exit_Btn.grid(row=0, column=3, padx=5, pady=5)
                
        
root = Tk()
obj=LPP_Solver(root)
root.mainloop()