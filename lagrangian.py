# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 22:02:06 2021

@author: Teoman
"""
import time
import numpy as np
from scipy.optimize import linprog

start_time=time.time()

#matrixs
 
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

lb_lamda=np.zeros(6)

def calculate_new_cij(lamda): #finds Cij+λj
    new_cij=np.zeros((6,7))
    for j in range (7):
        for i in range (6):
            new_cij[i][j]=(d_ij[i][j]*0.06*2*d_j[j]+daily[i]*d_j[j])+lamda[j]
    return new_cij  

def calculate_cij_wolb(): #finds Cij
    new_cij_wolb=np.zeros((6,7))
    for j in range (7):
        for i in range (6):
            new_cij_wolb[i][j]=(d_ij[i][j]*0.06*2*d_j[j]+daily[i]*d_j[j])
    return new_cij_wolb 
                       
def Knapsack(lamda):
    new_cij= calculate_new_cij(lamda)
    x_ij=np.zeros((6,7))
    kısıt_y=y.copy()
    assigned_values=np.zeros((6,7))   #temporary list for solving lb

    for i in range (6):           #solves knapsack
        iliste=[m/n for m,n in zip(new_cij[i],d_j)]
        iliste=np.array(iliste)
        x=iliste.argsort()
        for j in x:
            if kısıt_y[i]>0:
                x_ij[i][j]=min((kısıt_y[i]/d_j[j]),1)
                kısıt_y[i]=kısıt_y[i]-d_j[j]
            else:
                break
            assigned_values[i][j]=new_cij[i][j]*x_ij[i][j]
            
    for i in range (6):     #calculate lamda values
        lb_lamda[i]=assigned_values[i].sum(axis=0)+yi[i]
        if lb_lamda[i]<=0:
            continue
        else:
            x_ij[i]=[0,0,0,0,0,0,0]
            lb_lamda[i]=0        
    new_lb=np.sum(lb_lamda)-np.sum(lamda)    #find lb
    return x_ij,lb_lamda,new_cij,new_lb

def simplex(lb_lamda): 
    new_cij_wolb=calculate_cij_wolb()
    sorted_lb=lb_lamda.argsort() 
    toplam=0
    v1=[]        #v1 is values that will go to equation
    
    for i in sorted_lb:
        if np.sum(d_j)>toplam:
            toplam=y[i]+toplam
            v1.append(i)
        else:
            break
        
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
        c.append(new_cij_wolb[i])        
    c=np.concatenate(c).ravel().tolist()
    for i in v1:
        sabit=yi[i]+sabit #adding capacities

    #solving simplex    
    res=linprog(c,A_ub=coef_a,b_ub=a_esit,A_eq=coef_b,b_eq=b_esit,method='revised simplex')
    upper_b=round(res.fun, ndigits=2)+sabit
    return upper_b

                
def subgradient(x_ij):
    s=np.zeros(7)
    x=x_ij.sum(axis=0)
    for j in range(7):
        s[j]=x[j]-1
    return s
          
def beta_calculate(s,lb_allamda,upper_b):
    alfa=0.2
    s_top=0
    for j in range(7):
        s_top=s[j]**2+s_top       
    beta=(alfa*(upper_b-lb_allamda))/s_top
    return beta

def lamda_calculate(beta,s,lamda):
    new_lamda=np.zeros(7)
    for j in range(7):
         new_lamda[j]=beta*s[j]+lamda[j]
    lamda=new_lamda
    return lamda

def calculator():
    epsilon=0.13
    h=0
    lb , ub = 0.00000000000001 , 100000000
    #lamda=np.array([-186,-170,-140,60,-115,-166,-112])
    lamda=np.zeros(7)
    while epsilon < ((ub - lb) / lb):
        x_ij,lb_lamda,new_cij,new_lb=Knapsack(lamda)
        ub_new=simplex(lb_lamda)
    
        if new_lb > lb: 
            lb = new_lb
            
        if ub_new < ub: 
            ub = ub_new
        
        s=subgradient(x_ij)
        beta=beta_calculate(s,lb,ub)
        lamda=lamda_calculate(beta,s,lamda)
        h=h+1
        print("Lb:",lb,"Ub:",ub,"Iteration:",h,"Epsilon:",(ub - lb) / lb)
    print("solution:",x_ij)
    print("lamdas:",lb_lamda)
    return  

print(calculator())

end_time=time.time()

print("Time:",end_time-start_time)


