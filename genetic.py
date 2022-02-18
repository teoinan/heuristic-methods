# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 19:38:17 2021

@author: Teoman
"""

import pandas as pd
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import random
coord=pd.read_csv("tsp.csv",names=["x","y"],header= None, )

def calculate_distance(coord,city1,city2):
    distance=math.sqrt(np.sum((coord.iloc[city1]-coord.iloc[city2])**2))
    return distance


def create_dist_matrix(coord):
    distance = np.zeros((len(coord),len(coord)))
    for city1 in range(51):
        for city2 in range(51):
            if city1 != city2:
                distance[city1 ,city2] = calculate_distance(coord, city1, city2)
    return distance

def find_distance(v_current,distance):
    mesafe=0
    for i in range(49):
        mesafe=mesafe+distance[v_current[i],v_current[i+1]]
    mesafe=mesafe+distance[v_current[0],v_current[50]]
    return mesafe

def generate_randomsolution():
    res = random.sample(range(0, 51),51)
    return res

def sorting_index(population,F_population):
    zipped_lists = zip(F_population, population)
    sorted_lists = sorted(zipped_lists)
    sorted_population = [i for _, i in sorted_lists]
    return sorted_population
    
def initialization(population_count,distance):
    population=[]
    F_population=[]
    for i in range(population_count):
        res=generate_randomsolution()
        population.append(res)
    for i in population:
        F_population.append(find_distance(i,distance))
    sorted_population=sorting_index(population,F_population)
    return sorted_population

def replacement(sorted_population):
    popsize=len(sorted_population)/2
    for i in range(int(popsize)):
        del sorted_population[-1]
    return sorted_population
 
def pairing(sorted_population):
    pairings=[]
    pairing=len(sorted_population)/2
    weight=[]
    sum_of_list_index=np.sum(list(range(len(sorted_population)+1)))
    for i in range(len(sorted_population)):
        weight_item=(i+1)/sum_of_list_index
        weight.append(weight_item)
    weight.reverse()
    for i in range(int(pairing)):
        pairings.append(random.choices(population=sorted_population,weights=weight,k=2))
    return pairings

def crossover(pairings):
    children=[]
    for pairing in pairings:
        u1=random.randint(0,50)
        u2=random.sample(list(range(0, 51)), u1)
        new_child = [1000] * 51
        for i in u2:
            new_child[i]=pairing[0][i]
        paring2 = [x for x in pairing[1] if x not in new_child]
        h=0
        for i in range(51): 
            if new_child[i]==1000:
                new_child[i]=paring2[h]
                h+=1
        children.append(new_child)
    return children
                
def mutaion(children):
    h=0
    for i in children:
        element=random.randint(0,50)
        element2=random.randint(0,49)
        mutated=i.copy()
        mutated.remove(i[element])
        mutated.insert(element2,i[element])
        children[h]=mutated
        h+=1
    return children

def main(population_count,genaration):
    
    start=time.time()
    distance=create_dist_matrix(coord)
    sorted_population=initialization(population_count,distance)
    genarationcount=[]
    bestF_solutions=[]
    
    for i in range(genaration):
        genarationcount.append(i+1)
        pairings=pairing(sorted_population)
        children=crossover(pairings)
        children=mutaion(children)
        population=replacement(sorted_population)
        population=population+children
        F_population=[]
        
        for i in population:
            F_population.append(find_distance(i,distance))
            sorted_population=sorting_index(population,F_population)
            
        bestF_solutions.append(min(F_population))
    end=time.time()
    
    plt.figure(dpi=150)
    plt.plot(genarationcount,bestF_solutions)
    plt.title("title")
    plt.xlabel("genarations")
    plt.ylabel("best solution")
    plt.show()
    
    print("population:")
    print(sorted_population)
    print("----------------------")
    print("avarage distance",np.mean(F_population))
    print("best genetic:",sorted_population[0])
    print("best genetic distnace:", min(F_population))
    print("runtime:",end-start)
    print("----------------------")
            
    return sorted_population,sorted_population[0], min(F_population)

main(20,4000)
main(50,4000)
