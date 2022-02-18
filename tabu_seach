# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 20:54:03 2021

@author: Teoman
"""

import time
import numpy as np
from scipy.optimize import linprog
import random

y=[80,90,110,120,100,120] #capacity list 

d_j=[36,42,34,50,27,30,43] #demand list

yi=[220,240,260,275,240,230] #fixed cost

#km cost list
d_ij=[[18,23,19,21,24,17,9],
      [21,18,17,23,11,18,20],
      [27,18,17,20,23,9,18],
      [16,23,9,31,21,23,10],
      [31,20,18,19,10,17,18],
      [18,17,29,21,22,18,8]]

daily=[0.15,0.18,0.20,0.18,0.15,0.17] #daily cost

def calculate_cij(): #finds Cij
    new_cij=np.zeros((6,7))
    for j in range (7):
        for i in range (6):
            new_cij[i][j]=(d_ij[i][j]*0.06*2*d_j[j]+daily[i]*d_j[j])
    return new_cij 

def create_solution():
    while True:
        solution=np.zeros(6)
        for i in range(6):
            solution[i]=random.choice([0, 1])
            if np.sum(np.array(y)*solution)>np.sum(d_j):
                break
        if np.sum(np.array(y)*solution)>np.sum(d_j):
            break
    random.shuffle(solution)
    opened_facilities=[]
    
    for i, j in enumerate(solution):
        if j == 1:
            opened_facilities.append(i)
    
    return(opened_facilities)


def simplex(opened_facilities,new_cij):    #simplexi çöz
    v1=opened_facilities
        
    c=[]  #objective function coeff
    coef_a=np.zeros((len(v1),len(v1)*7)) #capacity cons left side of equation
    a_esit=[] #capacity cons right side of equation
    coef_b=np.zeros((7,len(v1)*7)) #demand cons left side of equation
    b_esit=[1]*7 #capacity cons right side of equation    
    sabit=0 #for adding demands
    
    for i in range(len(v1)):
        j=i*7
        coef_a[i][j:j+7]=d_j   
    for i in range(7):
        coef_b[i][i::7]=[1]*len(v1)
    for i in v1:
        a_esit.append(y[i])      
    a_esit=np.array(a_esit)   
    for i in v1:
        c.append(new_cij[i])        
    c=np.concatenate(c).ravel().tolist()
    for i in v1:
        sabit=yi[i]+sabit #adding capacities

    #solving simplex    
    res=linprog(c,A_ub=coef_a,b_ub=a_esit,A_eq=coef_b,b_eq=b_esit,method='revised simplex')
    upper_b=round(res.fun, ndigits=2)+sabit
    x_ij=res.x
    x_ij=x_ij.round(3)
    x_ij=x_ij.reshape((len(opened_facilities) , len(d_j))) 
    return upper_b,x_ij
        
def find_new_solutions(TabuList,FeasibleSet,opened,new_cij):
    cost=10000
    closed_one=[]
    added_one=[]
    for i in opened:
        for j in FeasibleSet:
            open_cand=opened.copy()
            open_cand.remove(i)
            open_cand.append(j)
            
            new_cost,new_x_ij=simplex(open_cand,new_cij)
            if new_cost<cost:
                cost=new_cost
                x_ij=new_x_ij
                closed_one.append(i)
                added_one.append(j)
                
    TabuList.append(closed_one[-1])   #kapanan hareketi tabu olarak kaydet
    opened.remove(closed_one[-1])    #kapanan facilityi kaldır
    opened.append(added_one[-1])   #yeni facility ekle            
    return opened,cost,x_ij         

               
def main(maxSize):
    new_cij=calculate_cij()
    opened=create_solution()
    TabuList=[]
    open_cost,x_ij=simplex(opened,new_cij)
    CurrentBest=open_cost
    h=1
    
    print("--------------------------------")
    print("initial cost:",open_cost)
    print("initial facilties",opened)
    print("initial xij:")
    print(x_ij)
    
    while True:
        closed_facilities=[]
        for i in range(6):
             if i not in opened:
                 closed_facilities.append(i)
                 
        FeasibleSet=[]         
        for t in closed_facilities:
            if t not in TabuList:
                FeasibleSet.append(t)
                
        opened,open_cost,x_ij=find_new_solutions(TabuList,FeasibleSet,opened,new_cij)
        
        if len(TabuList)>maxSize:
            TabuList.pop(0)
        
        print("-------------------------")
        print("iteration:",h)
        print("opened facilities",opened)
        print("FeasibleSet:",FeasibleSet)
        print("tabu list:",TabuList)
        print("x_ij:")
        print(x_ij)
        print("iteration's cost:",open_cost)
        print("current best",CurrentBest)
        
            
        if open_cost==CurrentBest:
            break
        
        if open_cost < CurrentBest:
            CurrentBest = open_cost
        
        h+=1
        
    return(CurrentBest,opened)

main(2)


        