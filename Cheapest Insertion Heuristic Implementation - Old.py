import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import time
start=time.time()

coord=pd.read_csv("tsp.csv",header= None, names=['x','y'],index_col=0)
coord.head()


def plot(coord):
    plt.figure(dpi = 500)
    plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    plt.plot(coord.loc[:,"x"], coord.loc[:,"y"], ".")

    for i in coord.index:
        plt.annotate("City" + str(i), (coord.loc[i,"x"] , coord.loc[i,"y"]))
        
    plt.show()

plot(coord)

#CALCULATE all DİSTANCEs find minumum
def calculate_distance(coord,city1,city2):
    distance=math.sqrt(np.sum((coord.iloc[city1]-coord.iloc[city2])**2))
    return distance

#tyi hesaplayacak kod oluştur
def create_dist_matrix(coord):
    distance = np.zeros((len(coord),len(coord)))
    for city1 in range(51):
        for city2 in range(51):
            if city1 != city2:
                distance[city1 ,city2] = calculate_distance(coord, city1, city2)
    return distance
print(create_dist_matrix(coord))
def c_a_k_b_solver(matrix,a,k,b):
    c_a_k_b=matrix[a,k]+matrix[b,k]-matrix[a,b]
    return c_a_k_b
    
def find_short(coord):
    s_dist=create_dist_matrix(coord)
    flat = s_dist.flatten()
    minu= flat[flat != 0].min()
    i=np.where(s_dist == minu)[0]
    return i

def set_first_t(coord):
    road=np.array(find_short(coord))
    last_Digit=road[0]
    road=np.append(road,last_Digit)
    return road

def create_K(coord):
    list1=np.arange(0,51)
    T=set_first_t(coord)
    K= np.setdiff1d(list1,T)
    return T, K

print(create_K(coord))

def objective_func(coord):
    matrix=create_dist_matrix(coord)
    T, K = create_K(coord)
    T=T.tolist()
    K=K.tolist()
    while len(K)>1:
        min1=1000
        mink=None 
        for t in (1,len(T)-1):
            for k in range(len(K)-1):
                short_dis=matrix[T[t],K[k]]
                if short_dis<min1:
                    min1=short_dis
                    mink=k 
        for a in (1,len(T)-1):
            b=a+1
            min2=1000
            c_a_k_b = c_a_k_b_solver(matrix,T[a],K[mink],T[b])
            if c_a_k_b < min2:
                min2=c_a_k_b
                min_a=a
            T.insert(min_a,K[mink])
            K.pop(mink)
     
    return T, matrix

def result(coord):
    T , matrix =objective_func(coord)
    distance=0
    for a in range(len(T)-1):
        distance=distance+matrix[a,a+1]
    return distance,T

print("result:",result(coord))
   
end=time.time()

print("runtime:",end-start)   
 
#kyi bul
#def id_k()


