import csv
import random
import pandas as pd
import numpy as np



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
    for i in fp['Faculty_Name']:
        total_teacher_list.append(i)

    for i in cp['Course_Name']:
        total_subject_list.append(i)
        
    for i in cp['Semester']:
        total_batch_list.add(i)

    tdf = cp.loc[cp['Type'] == 'L'] # Temporary dataframe to just search for course with type L 
    for i, j in zip(tdf['Course_Code'], tdf['NOCW']):
        subject_lab_credithour_dict[i] = j

    tdf = cp.loc[cp['Type'] == 'N'] # Same as above
    for i, j in zip(tdf['Course_Code'], tdf['NOCW']):
        subject_credithour_dict[i] = j

    for i in total_batch_list:
        tdf = cp.loc[cp['Semester'] == i]
        for j in tdf['Course_Code']:
            if i not in subject_batch_dict:
                subject_batch_dict[i] = [j]
            else:
                subject_batch_dict[i].append(j)
    
    #adding no class to each sem
    for i in total_batch_list:
        tdf = cp.loc[cp['Semester'] == i]
        sch = 0
        for j in tdf['NOCW']:
            sch+=j
        subject_batch_dict[i].append('NC'+str(i))
        no_class_hours_dict['NC'+str(i)] = 30-sch # How many classes are free for each batch
        course_type_dict['NC'+str(i)] = 'NC'
        
    for i, j in zip(cp['Course_Code'], cp['Semester']):
        subject_batch_ind_dict[i] = j # Subject to its batch mapping

    for i, j in zip(cp['Course_Code'], cp['Faculty_id']):
        subject_teacher_dict[i] = j

    for i, j in zip(cp['Course_Code'], cp['Type']):
        course_type_dict[i] = j
    
#---------------------------------------------------------#

# Intialization 

# Initialize a week chromosome 
# look into this later
# Chromosome skeleton
def initializeChromosome():
    initializeTables()
    week = []
    day = []
    slot = []
    for i in range(5):
        day = []
        for i in range(6):
            slot = []
            for i in range(4):
                slot.append('')
            day.append(slot)
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

def fitnessFunction(chromosome):

    fitness_value = 0
    hconflicts = 0
    def hardConstraints(week):
        
        # No faculty should have two classes alloted in same slot of time
        # No two batches should have same lab alloted to them in same slot of time
        c1 = 0
        for day in week:
            for slot in day:
                for sub in slot:
                    for osub in slot:
                        if sub!='' and osub!='':   
                            # Faculty clash check
                            if sub!=osub and subject_teacher_dict[sub]==subject_teacher_dict[osub]:
                                c1+=1
                            # Lab clash check
                            if sub!=osub and course_type_dict[sub]=='L' and course_type_dict[osub]=='L':   
                                if lab_alloted[subject_batch_ind_dict[sub]] == lab_alloted[subject_batch_ind_dict[osub]]:
                                    c1+=1   
        c1 = c1//2

        # Faculty should get a slot off after teaching 2 hours continously ( not nessacary to same batch )  
        # for day in week:
        #     for i in range(5):
        #         print(day[i],day[i+1])
        #         for s1 in day[i]:
        #             # How to handle faculty conflicts and repeating classes ?
        #             for s2 in day[i+1]:


        # Every batch should have only one class of 2 continous classes 
        # Do this for the faculty
        # And no class should be repeated after later in day or should only be 2 hours class

        
        # We calculate these conflicts by calculating the total count of a subject in a day and the longest continous class of 
        # that subject ; then no. of conflict = (total class - longest class) + (longest class - 2)
        c2 = 0
        two_class_day = set()
        day_classes = []
        classes_in_day = set()
        for day in week:
            for j in range(4):
                for i in range(6):
                    day_classes.append(day[i][j])
                # We apply the checks here on each day classes of each batch
                for sub in day_classes:
                    if sub!='' and sub not in classes_in_day:
                        classes_in_day.add(sub)
                        tc = day_classes.count(sub)
                        c = 0
                        lc = 0
                        for i in range(len(day_classes)):
                            if day_classes[i] == sub:
                                c+=1
                            else:
                                lc = max(lc,c)
                                c = 0
                        lc = max(lc,c)
                        
                        if lc>=2:
                            two_class_day.add(sub)
                        if lc == 1:
                            c2+= (tc-lc)
                        else:
                            c2+= (tc-lc)+(lc-2)

                if len(two_class_day)>1:
                    c2+= len(two_class_day)-1
                two_class_day.clear()
                classes_in_day.clear()
                day_classes = []

        return 1/(1+(c1+c2))

    fitness_value += hardConstraints(chromosome)

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

def crossover(pop):
    # Selection ( of parents )
    roullete_pool = []
    for i in range(len(pop)):
        for j in range(int(Fit_values[i]*1000)):
            roullete_pool.append(pop[i])

    # Roullete Wheel selection of parents
    p1 = random.randint(0,len(roullete_pool)-1)
    parent1 = roullete_pool[p1]
    while parent1 in roullete_pool:
        roullete_pool.remove(parent1)
    pop.remove(parent1)

    p2 = random.randint(0,len(roullete_pool)-1)
    parent2 = roullete_pool[p2]
    while parent2 in roullete_pool:
        roullete_pool.remove(parent2)
    pop.remove(parent2)

    parent1 = openChromosome(parent1)
    parent2 = openChromosome(parent2)

    # Will crossover happen.? A probability

    # Crossover probability calculation / test
    crossProb = 0.6
    if random.randint(0,100)<=(crossProb*100):
        # Perform crossover
        # N Multipoint crossover 
        N = 15
        cpoints = [0]
        for i in range(N):
            cpoints.append(random.randint(1,119))
        cpoints = sorted(list(set(cpoints)))
        cpoints.append(120)

        offspring1 = []
        for i in range(0,len(cpoints)-1):
            if (i%2)==0:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring1.append(parent1[j])
            else:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring1.append(parent2[j])

        offspring2 = []
        for i in range(0,len(cpoints)-1):
            if (i%2)==0:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring2.append(parent2[j])
            else:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring2.append(parent1[j])

        offspring1 = closeChromosome(offspring1)
        offspring2 = closeChromosome(offspring2)
    
        # Mutation --------------------------------------------#
        # We perform swap or scramble mutation
        # Go within the slot and change the randomly chosen batch classes
        





        return [offspring1,offspring2]
    else:
        return []
    # print(parent1,fitnessFunction(closeChromosome(parent1)))
    # print(parent2,fitnessFunction(closeChromosome(parent2)))
    # print(offspring1,fitnessFunction(offspring1))
    # print(offspring2,fitnessFunction(offspring2))

#----------------------------------------------------------------#

# New generation from crossover

# This will return a 100 sized new generation of childrens
# Sometimes it maybe good sometimes it maybe shit

generations = 10

while generations!=0:
    generations -= 1
    # Will make new child population 
    childrenpop = []
    childFit_value = []
    temppop = pop.copy()


    while temppop!=[]:
        childrens = crossover(temppop)
        if childrens!=[]:
            o1,o2 = childrens[0],childrens[1]
            #print(len(temppop))
            childrenpop.append(o1)
            childFit_value.append(fitnessFunction(o1))
            childrenpop.append(o2)
            childFit_value.append(fitnessFunction(o2))
    pop = pop+childrenpop
    Fit_values = Fit_values+childFit_value
    #print(len(pop),len(Fit_values))
    # Will select the best 100 from initial pop and children 

    pop.sort(key=fitnessFunction,reverse=True)
    Fit_values.sort(reverse=True)

    
    # for i in range(len(pop)):
    #     print(Fit_values[i],fitnessFunction(pop[i]))
    


    pop = pop[:popz]
    Fit_values = Fit_values[:popz]
    print("new gen")
    
    
    

# Add binary tournament selection to select the best 100

print(max(Fit_values))
print(pop[0],fitnessFunction(pop[0]))