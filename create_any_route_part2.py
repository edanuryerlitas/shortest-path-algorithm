# -*- coding: utf-8 -*-
"""
Created on Sun May 12 19:38:14 2019

@author: EDA NUR YERLİTAŞ
"""

import matplotlib.pyplot as plt
import numpy as np
import xlrd


work=xlrd.open_workbook(r'distancematrix.xls')
sheet1=work.sheet_by_index(0)

#------------------------------------------------------------------------------

citydis=[];
for i in range (81):
    city=sheet1.cell_value(8,i+2)
    citydis.append(city)
    
citydis.pop(5) #Ankara was deleted

b=np.argmin(citydis)




citydis2=[]
for i in range (81):
    city2=sheet1.cell_value(72,i+2)
    citydis2.append(city2)

citydis2.pop(69)
#print(citydis2)
c=np.argmin(citydis2)
#print(c)
#------------------------------------------------------------------------------


ciity=[]
for n in range (81):
    for i in range(81):
        ccitty=sheet1.cell_value(n+3,i+2)#excel file for onlydistances
        ciity.append(ccitty)

#print(ciity) #distances of cities 
      
z=81    
matrix=np.zeros((z,z))        
rs=np.arange(0,6481,81)  

list=[]
for i in range (81):
    h=int(rs[i])
    list.append(h)

 
for n in range (81):
        for i in range (81):
            ciity[81*i+i]=0   #strings equal to zero       
            matrix[n,i]=ciity[list[n]+i]
            ciity[81*i+i]=' ' #strings equal to string again  
            
print(matrix) #MATRIX FİLE for only distances
#------------------------------------------------------------------------------


#................................grapth with points............................

work2=xlrd.open_workbook(r'xxx.xls')
sheet2=work2.sheet_by_index(0)

cordinate=[]
for n in range (81):
    for i in range(2):
        cor=sheet2.cell_value(n+1,i+2)
        cordinate.append(cor)                
m=81
matrix2=np.zeros((m,2))


tk=np.arange(0,161,2)
for n in range (81):
        for i in range (2):
            matrix2[n,i]=cordinate[tk[n]+i]           
print(matrix2)


yy=matrix2[0:,0]#y coordinates of cities
xx=matrix2[0:,1]#x
plt.plot(xx,yy,'o')
#..............................................................................
#..............................................................................

#any route that starts in Ankara visits every other city and returns back
first_distance=matrix[5,0] #distance from Ankara
print('first distance:',first_distance)

alldistance=[first_distance]
for d in range(80): #distance from other cities
    distance=matrix[d,d+1]
    alldistance.append(distance)
    print(d+2,'nd distance',distance)
#calculate its length
print('all distances=',sum(alldistance))
#plot this route
for i in range(80):
    plt.plot([xx[i],xx[i+1]],[yy[i],yy[i+1]],'-o')
###############################################################################




