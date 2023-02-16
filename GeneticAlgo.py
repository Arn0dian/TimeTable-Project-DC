import csv
import itertools
import random
import time
import pandas as pd
import numpy as np
st = time.time()
fp = pd.read_csv('faculty.csv')
cp = pd.read_csv('courses.csv')
# print(cp)
# print(fp)

total_subject_list = []
total_teacher_list = []
total_batch_list = set()
day_timeslot_dict = {'mon': [1, 2, 3, 4, 5, 6], 'tue': [7, 8, 9, 10, 11, 12],
                     'wed': [13,14, 15, 16, 17, 18], 'thu': [19, 20, 21, 22, 23, 24],
                     'fri': [ 25, 28, 29, 30, 31, 32]}
lab_alloted = {2:6,4:7,6:7,8:6}
subject_lab_credithour_dict = {}
subject_credithour_dict = {}
subject_batch_dict = {}
no_class_hours_dict = {}
subject_batch_ind_dict = {}
subject_teacher_dict = {}
course_type_dict = {}
#--------------------------------------------#
# Initialize all table values

def initializeTables():
    global total_teacher_list, total_subject_list, total_batch_list
    global subject_lab_credithour_dict, subject_credithour_dict, subject_batch_dict
    global no_class_hours_dict, subject_batch_ind_dict, subject_teacher_dict, course_type_dict
    
    total_teacher_list = list(fp['Faculty_Name'])
    total_subject_list = list(cp['Course_Name'])
    total_batch_list = set(cp['Semester'])
    
    subject_lab_credithour_dict = dict(zip(cp.loc[cp['Type'] == 'L', 'Course_Code'], cp.loc[cp['Type'] == 'L', 'NOCW']))
    subject_credithour_dict = dict(zip(cp.loc[cp['Type'] == 'N', 'Course_Code'], cp.loc[cp['Type'] == 'N', 'NOCW']))
    
    subject_batch_dict = {i: list(tdf['Course_Code']) + ['NC'+str(i)]
                          for i, tdf in cp.groupby('Semester')}
    
    no_class_hours_dict = {'NC'+str(i): 30 - tdf['NOCW'].sum()
                           for i, tdf in cp.groupby('Semester')}
    course_type_dict = {'NC'+str(i): 'NC' for i in total_batch_list}
    
    for i, j in zip(cp['Course_Code'], cp['Semester']):
        subject_batch_ind_dict[i] = j
        
    subject_teacher_dict = dict(zip(cp['Course_Code'], cp['Faculty_id']))
    course_type_dict.update(dict(zip(cp['Course_Code'], cp['Type'])))
    
#---------------------------------------------------------#

# Intialization 

# Initialize a week chromosome 
# look into this later
# Chromosome skeleton
def initializeChromosome():
    initializeTables()
    week = []
    for i in range(5):
        day = []
        for j in range(6):
            slots = ['' for k in range(4)]
            day.append(slots)
        week.append(day)
        
    for day in week:
        for slot in day:
            for i in range(len(slot)):
                rn = random.randint(0, len(subject_batch_dict[(i*2)+2])-1)
                sub = subject_batch_dict[(i*2)+2][rn]
                if course_type_dict[sub] == 'NC':
                    if no_class_hours_dict[sub]>0:
                        slot[i] += ''
                        no_class_hours_dict[sub]-=1
                        if no_class_hours_dict[sub] == 0:
                            subject_batch_dict[(i*2)+2].remove(sub)
                elif course_type_dict[sub] == 'N':
                    if subject_credithour_dict[sub]>0:
                        slot[i] += sub
                        subject_credithour_dict[sub]-=1
                        if subject_credithour_dict[sub] == 0:
                            subject_batch_dict[(i*2)+2].remove(sub)
                elif course_type_dict[sub] == "L":
                    if subject_lab_credithour_dict[sub]>0:
                        slot[i] += sub
                        subject_lab_credithour_dict[sub]-=1 
                        if subject_lab_credithour_dict[sub] == 0:
                            subject_batch_dict[(i*2)+2].remove(sub)

    return week



def openChromosome(week):
    oweek = []
    for day in week:
            for slot in day:
                for sub in slot:
                    oweek.append(sub)
    return oweek

def closeChromosome(week):
    cweek = []
    slotting = []
    for i in range(0,len(week),4):
        slotting.append(week[i:i+4])
    for i in range(0,len(slotting),6):
        cweek.append(slotting[i:i+6])
    return cweek

def popenChromosome(week):
    poweek = []
    for day in week:
        for slot in day:
            poweek.append(slot)
    return poweek

def pcloseChromosome(slotting):
    pcweek = []
    for i in range(0,len(slotting),6):
        pcweek.append(slotting[i:i+6])
    return pcweek

# Create a population 
popz = 100
pop = []
for i in range(popz):
    pop.append(initializeChromosome())


# ---------------------------------------------------------------------#

# Fitness evaluation 

# No Faculty should have been assigned two different classes at same time ( in same slot of day )
# No Lab should be assigned to two different batches at same time

# We count the number of conflicts / Violations made in the chromosome and add 1/1+c score to the chromosome's final eval score
# if c is 0 the max value of 1 is added 
def returnFit(x):
    return sum([1/(1+i) for i in x])

def repairLost(chromosome):

    courseCred = dict(zip(cp['Course_Code'], cp['NOCW']))

    for day in chromosome:
            for slot in day:
                for sub in slot:
                    if sub!='' and sub in courseCred:
                        courseCred[sub]-=1
                        if courseCred[sub] == 0:
                            del courseCred[sub]
                    elif sub!='' and sub not in courseCred:
                        slot[slot.index(sub)] = ''
    
    # Create a dictionary of missing classes for each batch
    missing_class_batch = {}
    for sub, cred in courseCred.items():
        if subject_batch_ind_dict[sub] not in missing_class_batch:
            missing_class_batch[subject_batch_ind_dict[sub]] = [sub]
        else:
            missing_class_batch[subject_batch_ind_dict[sub]].append(sub)

    # Assign missing classes to empty slots
    for day in chromosome:
        for slot in day:
            for i, sub in enumerate(slot):
                if not sub:
                    if ((i*2)+2) in missing_class_batch:
                        sb = random.choice(missing_class_batch[(i*2)+2])
                        slot[i] = sb
                        courseCred[sb] -= 1
                        if courseCred[sb] == 0:
                            del courseCred[sb]
                            missing_class_batch[((i*2)+2)].remove(sb)
                            if not missing_class_batch[(i*2)+2]:
                                del missing_class_batch[(i*2)+2]
                
    


def fitnessFunction(chromosome):
    conflicts = []
    fitness_value = 0

    repairLost(chromosome)
    def hardConstraints(week):
        
        # No faculty should have two classes alloted in same slot of time
        # No two batches should have same lab alloted to them in same slot of time
        conflicts.append(0)
        for day in week:
            for slot in day:
                for sub, osub in itertools.combinations(slot, 2):
                    if sub and osub:
                        # Faculty clash check
                        if sub != osub and subject_teacher_dict[sub] == subject_teacher_dict[osub]:
                            conflicts[-1] += 1
                        # Lab clash check
                        if sub != osub and course_type_dict[sub] == 'L' and course_type_dict[osub] == 'L':
                            if lab_alloted[subject_batch_ind_dict[sub]] == lab_alloted[subject_batch_ind_dict[osub]]:
                                conflicts[-1] += 1

        # Faculty should get a slot off after teaching 2 hours continously ( not nessacary to same batch )  
        # for day in week:
        #     for i in range(5):
        #         print(day[i],day[i+1])
        #         for s1 in day[i]:
        #             # How to handle faculty conflicts and repeating classes ?
        #             for s2 in day[i+1]:


        # Every batch should have only one class of 2 continous classes 
        # Do this for the faculty

        # And no class should be repeated after later in day or should only be 2 hours class - done

        
        # We calculate these conflicts by calculating the total count of a subject in a day and the longest continous class of 
        # that subject ; then no. of conflict = (total class - longest class) + (longest class - 2)
        conflicts.append(0) # Blank class
        conflicts.append(0) # Repeated class
        conflicts.append(0) # lab second half
        for day in week:
            for j in range(4):
                day_classes = [day[i][j] for i in range(6)]

                # Blank class conflict 
                blank_class = day_classes.count('')
                if blank_class == 0:
                    conflicts[-3] += 0.1

                for sub in set(day_classes):
                    if sub != '':
                        tc = day_classes.count(sub)
                        c = 0
                        lc = 0
                        for i in range(len(day_classes)):
                            if day_classes[i] == sub:
                                c += 1
                            else:
                                lc = max(lc, c)
                                c = 0
                        lc = max(lc, c)

                        if lc == 1:
                            conflicts[-2] += (tc - lc)
                        else:
                            conflicts[-2] += (tc - lc) + (lc - 2)

                # Lab classes should be conducted in second half
                for i in range(3):
                    if day_classes[i]!='' and course_type_dict[day_classes[i]]=='L':
                        conflicts[-1] += 0.2

        # Class after lunch and before lunch should not be same                       
        conflicts.append(0)
        for day in week:
            if set(day[2]) == set(day[3]):
                conflicts[-1] += 1




        # number of occupied slots should not be more than 5
        

        
        return returnFit(conflicts)

    fitness_value += hardConstraints(chromosome)
    print(conflicts)
    return (fitness_value)


# Fitness Calculations

Fit_values = []
for chromosome in pop:
    Fit_values.append(fitnessFunction(chromosome))

# for i in range(len(pop)):
#     print(pop[i],Fit_values[i])
# print(pop[Fit_values.index(max(Fit_values))],max(Fit_values))

#---------------------------------------------------------------------------#

# Crossover 

# We use random or non-random multipoint crossover here 
# Random multipoint : two parents are chosen to crossover by roullete wheel selection , then a random value N (no. of points 
# of crossover) ranging from 1 to 119 is chosen. Following which the multipoint crossover is done. 

# Non-Random multipoint : We can fix the no. of points of crossover to suitable value


def crossoverIW(pop):

    # assume the population is a list of individuals with corresponding fitness values
    population = [(indiv, fitness) for indiv, fitness in zip(pop, Fit_values)]

    # select the first parent
    parent1 = random.choice(population)[0]
    # select the second parent
    while True:
        parent2 = random.choice(population)[0]
        if parent2 != parent1:
            break
        
    pop.remove(parent1)
    pop.remove(parent2)

    parent1 = openChromosome(parent1)
    parent2 = openChromosome(parent2)

    
    # Try crossover of slots only ---------------- #

    # Define the crossover probability
    crossProb = 0.8

    # Check if crossover should be performed
    if random.random() <= crossProb:
    # Perform crossover
    # N Multipoint crossover 
        N = 10
        cpoints = sorted(random.sample(range(1, 120), N-1))

        # Add the endpoints of the chromosome to the list of crossover points
        cpoints = [0] + cpoints + [120]
        
        # Extract segments from parents and create offspring
        offspring1 = []
        offspring2 = []
        for i in range(len(cpoints)-1):
            if i % 2 == 0:
                seg_length = cpoints[i+1] - cpoints[i]
                if len(offspring1) + seg_length <= 120:
                    offspring1 += parent1[cpoints[i]:cpoints[i+1]]
                else:
                    offspring1 += parent1[cpoints[i]:cpoints[i]+(120-len(offspring1))]
                seg_length = cpoints[i+1] - cpoints[i]
                if len(offspring2) + seg_length <= 120:
                    offspring2 += parent2[cpoints[i]:cpoints[i+1]]
                else:
                    offspring2 += parent2[cpoints[i]:cpoints[i]+(120-len(offspring2))]
            else:
                seg_length = cpoints[i+1] - cpoints[i]
                if len(offspring1) + seg_length <= 120:
                    offspring1 += parent2[cpoints[i]:cpoints[i+1]]
                else:
                    offspring1 += parent2[cpoints[i]:cpoints[i]+(120-len(offspring1))]
                seg_length = cpoints[i+1] - cpoints[i]
                if len(offspring2) + seg_length <= 120:
                    offspring2 += parent1[cpoints[i]:cpoints[i+1]]
                else:
                    offspring2 += parent1[cpoints[i]:cpoints[i]+(120-len(offspring2))]
               
        offspring1 = closeChromosome(offspring1)
        offspring2 = closeChromosome(offspring2)

        return [offspring1,offspring2]
    
    else:
        return []

#---------------------------#--------------------------------------------#    

def crossoverSW(pop):

    # assume the population is a list of individuals with corresponding fitness values
    population = [(indiv, fitness) for indiv, fitness in zip(pop, Fit_values)]

    # select the first parent
    parent1 = random.choice(population)[0]
    # select the second parent
    parent2 = random.choice(population)[0]

    if parent1==parent2:
        pop.remove(parent1)
    else:
        pop.remove(parent1)
        pop.remove(parent2)

    parent1 = popenChromosome(parent1)
    parent2 = popenChromosome(parent2)
    
    crossProb = 0.8
    # Check if crossover should be performed
    if random.random() <= crossProb:
        N = 5
        cpoints = sorted(random.sample(range(1, 30), N-1))

        # Add the endpoints of the chromosome to the list of crossover points
        cpoints = [0] + cpoints + [30]
        
        # Extract segments from parents and create offspring
        offspring1 = []
        offspring2 = []

        for i in range(0,len(cpoints)-1):
            if (i%2)==0:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring1.append(parent1[j])
            else:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring1.append(parent2[j])

        for i in range(0,len(cpoints)-1):
            if (i%2)==0:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring2.append(parent2[j])
            else:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring2.append(parent1[j])

        offspring1 = pcloseChromosome(offspring1)
        offspring2 = pcloseChromosome(offspring2)

        return [offspring1,offspring2]
    else:
        return []

#-------------------------------#-----------------------------------------#

def uniformCrossover(pop):
    # assume the population is a list of individuals with corresponding fitness values
    population = [(indiv, fitness) for indiv, fitness in zip(pop, Fit_values)]

    # select the first parent
    parent1 = random.choice(population)[0]
    # select the second parent
    while True:
        parent2 = random.choice(population)[0]
        if parent2 != parent1:
            break
        
    pop.remove(parent1)
    pop.remove(parent2)

    parent1 = openChromosome(parent1)
    parent2 = openChromosome(parent2)

    crossProb = 0.8

    # Check if crossover should be performed
    if random.random() <= crossProb:
        offspring1 = []
        offspring2 = []

        for i in range(120):
            rn = random.random()
            if rn<=0.3:
                offspring1.append(parent1[i])
                offspring2.append(parent2[i])
            else:
                offspring1.append(parent2[i])
                offspring2.append(parent1[i])

        offspring1 = closeChromosome(offspring1)
        offspring2 = closeChromosome(offspring2)

        return [offspring1,offspring2]
    
    else:
        return []




#----------------------------------------------------------------#

# New generation from crossover

# This will return a 100 sized new generation of childrens
# Sometimes it maybe good sometimes it maybe shit

generations = 100
gnc = 1
while generations!=0:
    generations -= 1
    # Will make new child population 
    childrenpop = []
    childFit_value = []

    temppop = pop.copy()
    while temppop!=[]:
        childrens = uniformCrossover(temppop)
        if childrens!=[]:
            o1,o2 = childrens[0],childrens[1]
            #print(len(temppop))
            childrenpop.append(o1)
            childFit_value.append(fitnessFunction(o1))
            childrenpop.append(o2)
            childFit_value.append(fitnessFunction(o2))


    pop += childrenpop
    Fit_values += childFit_value
    print(len(pop))
    spop = [val for (_, val) in sorted(zip(Fit_values, pop), key=lambda x: x[0],reverse=True)]
    pop = spop.copy()
    pop = pop[:popz]
    Fit_values.clear()
    for i in pop:
        Fit_values.append(fitnessFunction(i))
    

    print("Generation ",gnc," Max Fitness ",Fit_values[0])

    
    
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
                 
    

et = time.time()
print("time : ",et-st)
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
