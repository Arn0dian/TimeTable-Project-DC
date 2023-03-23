import time
from initialization import *
from fitness import *
from crossover import *
import csv
st = time.time()


generations = 300
gnc = 1
while generations!=0:
    generations -= 1
    # Will make new child population 

    childrenpop = []
    childFit_value = []

    temppop = pop.copy()
    while temppop!=[]:

        if len(temppop)==2:
            temppop = []
            break

        childrens = crossoverIWSW(temppop)
        if childrens!=[]:
            o1,o2 = childrens[0],childrens[1]
            childrenpop.append(o1)
            childFit_value.append(fitnessFunction(o1))
            childrenpop.append(o2)
            childFit_value.append(fitnessFunction(o2))


    pop += childrenpop
    Fit_values += childFit_value
    spop = [val for (_, val) in sorted(zip(Fit_values, pop), key=lambda x: x[0],reverse=True)]
    pop = spop.copy()
    pop = pop[:popz]
    Fit_values.clear()
    for i in pop:
        Fit_values.append(fitnessFunction(i))
    
    
    # import os, psutil; print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)


def separateChromosome(chromosome):
    sem2 = {}
    sem4 = {}
    sem6 = {}
    sem8 = {}
    dayMap = {1:"Mon", 2:"Tue" , 3:"Wed" , 4:"Thurs" , 5:"Fri"}
    for i in range(len(chromosome)):
        
        sem2[dayMap[i+1]] = []
        sem4[dayMap[i+1]] = []
        sem6[dayMap[i+1]] = []
        sem8[dayMap[i+1]] = []
        for  slot in chromosome[i]:
            sem2[dayMap[i+1]].append(slot[0])
            sem4[dayMap[i+1]].append(slot[1])
            sem6[dayMap[i+1]].append(slot[2])
            sem8[dayMap[i+1]].append(slot[3])
    return sem2,sem4,sem6,sem8
                 
    


print("Max fitness achived : ",max(Fit_values))

y1 , y2 , y3 , y4 = separateChromosome(pop[0])

print("\n\n\n\nFirst year\n")
for k , v in y1.items():
    print(k,v)
print("\nSecond year\n")
for k , v in y2.items():
    print(k,v)
print("\nthird year\n")
for k , v in y3.items():
    print(k,v)
print("\nfourth year\n")
for k , v in y4.items():
    print(k,v)
print(fitnessFunction(pop[0]))
et = time.time()
print("time : ",et-st)

courseCred = dict(zip(cp['Course_Code'], cp['NOCW']))
chromosome = pop[0]
for day in chromosome:
        for slot in day:
            for sub in slot:
                if sub!='' and sub in courseCred:
                    courseCred[sub]-=1
                    if courseCred[sub] == 0:
                        del courseCred[sub]
                elif sub!='' and sub not in courseCred:
                        slot[slot.index(sub)] = ''


def convert_To_CSV(tt):
    
    final = [['Day','9:30-10:30','10:30-11:30',"11:30-12:30","2:00-3:00","3:00-4:00","4:00-5:00"]]     

    for day in tt.keys():
        tt[day].insert(0,day)
        final.append(tt[day])   
    return final 
     


with open('Year1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(convert_To_CSV(y1))

with open('Year2.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(convert_To_CSV(y2))

with open('Year3.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(convert_To_CSV(y3))

with open('Year4.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(convert_To_CSV(y4))
               

print(courseCred)