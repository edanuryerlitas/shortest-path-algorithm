# -*- coding: utf-8 -*-
"""
Created on Sun May 12 19:38:14 2019

@author: EDA NUR YERLİTAŞ
"""
import numpy as np
import matplotlib.pyplot as plt
import xlrd
#------------------------------------------------------------------------------
def get_coordinates():
    work2=xlrd.open_workbook(r'xxx.xls')
    sheet2=work2.sheet_by_index(0)
    
    cordinate=[]
    for n in range (81):
        for i in range(2):
            cor=sheet2.cell_value(n+1,i+2)
            cordinate.append(cor)               
    n_city=81
    matrix2=np.zeros((n_city,2))

    tk=np.arange(0,161,2)
    for n in range (81):
            for i in range (2):
                matrix2[n,i]=cordinate[tk[n]+i]
                      
    yy=matrix2[0:,0]#y coordinates of cities
    xx=matrix2[0:,1]#x  
    return sheet2, xx, yy
#------------------------------------------------------------------------------

def get_path(n):  #create random path(+Ankara)
    p = np.arange(n)
    np.random.shuffle(p)
    p = np.append(p, p[0])
    return p


def get_path_length(apath):#total distance
    
    d = np.genfromtxt('distancematrix.csv', dtype='str',
                      delimiter=',', encoding='utf-8')
    d[d==''] = 0
    def distance(i,j):
        return float(d[i+1, j+1])
    
    total_length = 0.0
    for i,j in zip(apath[:-1],apath[1:]):
        dist=distance(i,j)
        total_length = total_length+dist 
    return total_length

#------------------------------------------------------------------------------

def draw_path(path):#draw path

    for i,j in zip(path[:-1],path[1:]):#path = np.append(path,path[0]) 
        plt.plot([x[i],x[j]],[y[i],y[j]],'-o')#plt.plot(x[path],y[path],'-o')
    plt.show()
    
#------------------------------------------------------------------------------   
            
def crossover(path1, path2): #delete repeat ones
    path1 = path1[:-1]
    path2 = path2[:-1]
    s     = np.random.randint(0,n)# cross over location
    path3 = np.hstack((path1[:s], path2[s:]))
        
    
    unique, counts = np.unique(path3, return_counts=True)
    d = dict(zip(unique, counts))
    replacewith=[]
    for i in d:
        if d[i]==2:
            replacewith.append(i)
        
    if len(set(path3))!=len(set(path2)):
        missing = list(set(path1)-set(path3))
        for i,j in zip(replacewith,missing):
            if np.random.rand()>.5:
                index=np.where(path3==i)[0][0]
            else:
                index=np.where(path3==i)[0][1]            
            path3[index]=j
    
    if np.random.rand()>0.1:
        a,b = np.random.randint(0,n,2)
        path3[a], path3[b] = path3[b], path3[a]
        
    path3 = np.append(path3,path3[0]) #add first value
    return path3

#------------------------------------------------------------------------------
def create_initial_population(n):
    population = []
    l=len(x)
    for i in range(n):
        p = get_path(l)
        population.append(p)
    population=np.array(population)
    population = sort_population(population)    
    return population

#------------------------------------------------------------------------------

def get_population_performance(population):#PERFORMANCE
    perf = []
    for i in population:
        perf.append(get_path_length(i))
    return np.array(perf)

#------------------------------------------------------------------------------
def sort_population(population):
    performance = get_population_performance(population)
    i = np.argsort(performance)
    return population[i]

#------------------------------------------------------------------------------
def multiply(population,n):

    population=population[:n]
    newpop = []
    for i in population:
        for j in population:
            newpop.append(crossover(i,j))
    newpop = np.array(newpop)
    newpop = sort_population(newpop)
    return newpop    

###############################################################################
###############################################################################
###############################################################################
sheet2, x, y= get_coordinates()
n= len(x)
n_population=10
population  = create_initial_population(100)
shortest_dist = get_path_length(population[0])
shortest_path = population[0]

#------------------------------------------------------------------------------
performance_list = []
i = 0
try:
      while True:
          i += 1
          print('generation', i, 'best performance %5.2f'% get_path_length(population[0]))
          #draws the best, ie, shortest path
          draw_path(population[0])
          
          #append the performance of the best individual to the performance list.
          performance_list.append(get_path_length(population[0]))
          plt.plot(performance_list,'.-')
          plt.show()
#          
          population = multiply(population,10)
          if get_path_length(population[0]) < shortest_dist:
                shortest_dist = get_path_length(population[0])
                shortest_path = population[0]
except KeyboardInterrupt:
      a = np.where(sheet2=='Ankara') # starting point
      if shortest_path[0] != a[0]:
            shortest_path = np.delete(shortest_path,0)
            b = shortest_path[:int(np.where(shortest_path==a[0])[0])]
            c = shortest_path[int(np.where(shortest_path==a[0])[0])+1:]
            shortest_path = np.concatenate([np.array(a[0]), c, b, np.array(a[0])])
      pass
print("best genes",(shortest_path), '\nwith min distance=',shortest_dist)

