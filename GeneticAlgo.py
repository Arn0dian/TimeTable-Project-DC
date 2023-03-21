import time
import json
from initialization import *
from fitness import *
from crossover import *
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

        childrens = crossoverIW(temppop)
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
    
    
    print("Generation ",gnc)
    gnc+=1
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

output = y1 
# for key in y2:
#     for i in range(len(y2[key])):
#         if y2[key][i]!='':
#             output[key][i]+=(" / "+y2[key][i])

# for key in y3:
#     for i in range(len(y3[key])):
#         if y3[key][i]!='':
#             output[key][i]+=(" / "+y3[key][i])

# for key in y4:
#     for i in range(len(y4[key])):
#         if y4[key][i]!='':
#             output[key][i]+=(" / "+y4[key][i])

with open("output.json", "w") as outfile:
    json.dump(output, outfile)

# import time
# from initialization import *
# from fitness import *
# from crossover import *
# st = time.time()

# generations = 300
# gnc = 1
# elitism_percent = .6
# maxfitch = ()
# maxfitval = -1

# while generations!=0:
#     generations -= 1


#     # Will make new child population 
#     childrenpop = {}
#     temppop = pop.copy()

#     while temppop!={}:
#         childrens = uniformCrossover(temppop)
#         if childrens!=[]:
#             o1,o2 = tuple(childrens[0]),tuple(childrens[1])
#             childrenpop[o1] = fitnessFunction(o1)
#             childrenpop[o2] = fitnessFunction(o1)

    
#     pop = pop | childrenpop
#     next_generation = dict(sorted(pop.items(), key=lambda item: item[1], reverse=True)[:int(elitism_percent*popz)])

#     while len(next_generation) < popz:
#         chromosome = random.choice(list(pop.keys()))
#         if chromosome not in next_generation:
#             next_generation[chromosome] = pop[chromosome]

#     # # calculate the total fitness of the population
#     # total_fitness = sum(fitness for fitness in pop.values())

#     # # create a list of tuples containing each individual and their corresponding selection probability
#     # selection_probs = [(chromosome, fitness/total_fitness) for chromosome, fitness in pop.items()]

#     # while len(next_generation) < popz:
#     #     # select an individual using roulette wheel selection
#     #     rand_num = random.uniform(0, 1)
#     #     cumulative_prob = 0
#     #     for chromosome, selection_prob in selection_probs:
#     #         cumulative_prob += selection_prob
#     #         if cumulative_prob >= rand_num:
#     #             # add the selected individual to the next generation
#     #             if chromosome not in next_generation:
#     #                 next_generation[chromosome] = pop[chromosome]
#     #                 break

#     # # if less than 100 unique individuals were selected, randomly add individuals until there are 100
#     # while len(next_generation) < 100:
#     #     chromosome = random.choice(list(pop.keys()))
#     #     if chromosome not in next_generation:
#     #         next_generation[chromosome] = pop[chromosome]

#     pop = next_generation


 
#     gnc+=1
#     for i in pop:
#         if pop[i]>maxfitval:
#             maxfitval = pop[i]
#             maxfitch = i
        


#     # elitism and selection of the next generation , not the best only 
#     # pop += childrenpop
#     # Fit_values += childFit_value
#     # spop = [val for (_, val) in sorted(zip(Fit_values, pop), key=lambda x: x[0],reverse=True)]
#     # pop = spop.copy()
#     # pop = pop[:popz]
#     # Fit_values.clear()
#     # for i in pop:
#     #     Fit_values.append(fitnessFunction(i))
#     # import os, psutil; print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)


# def separateChromosome(chromosome):
#     sem2 = {}
#     sem4 = {}
#     sem6 = {}
#     sem8 = {}
#     dayMap = {1:"Mon", 2:"Tue" , 3:"Wed" , 4:"Thurs" , 5:"Fri"}
#     for i in range(len(chromosome)):
        
#         sem2[dayMap[i+1]] = []
#         sem4[dayMap[i+1]] = []
#         sem6[dayMap[i+1]] = []
#         sem8[dayMap[i+1]] = []
#         for  slot in chromosome[i]:
#             sem2[dayMap[i+1]].append(slot[0])
#             sem4[dayMap[i+1]].append(slot[1])
#             sem6[dayMap[i+1]].append(slot[2])
#             sem8[dayMap[i+1]].append(slot[3])
#     return sem2,sem4,sem6,sem8
                 
    


# # print("Max fitness achieved : ",max(Fit_values))

# y1 , y2 , y3 , y4 = separateChromosome(substoweek(maxfitch))
# print("\n\n\n\nFirst year\n")
# for k , v in y1.items():
#     print(k,v)
# print("\nSecond year\n")
# for k , v in y2.items():
#     print(k,v)
# print("\nthird year\n")
# for k , v in y3.items():
#     print(k,v)
# print("\nfourth year\n")
# for k , v in y4.items():
#     print(k,v)
# print("maximum fitness : "+str(maxfitval))
# et = time.time()
# print("time : ",et-st)