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

    tdf = cp.loc[cp['Type'] == 'L']
    for i, j in zip(tdf['Course_Code'], tdf['NOCW']):
        subject_lab_credithour_dict[i] = j

    tdf = cp.loc[cp['Type'] == 'N']
    for i, j in zip(tdf['Course_Code'], tdf['NOCW']):
        subject_credithour_dict[i] = j

    for i in total_batch_list:
        tdf = cp.loc[cp['Semester'] == i]
        for j in tdf['Course_Code']:
            if i not in subject_batch_dict:
                subject_batch_dict[i] = [j]
            else:
                subject_batch_dict[i].append(j)
    
    for i, j in zip(cp['Course_Code'], cp['Semester']):
        subject_batch_ind_dict[i] = j

    for i, j in zip(cp['Course_Code'], cp['Faculty_id']):
        subject_teacher_dict[i] = j

    for i, j in zip(cp['Course_Code'], cp['Type']):
        course_type_dict[i] = j
#---------------------------------------------------------#

# Intialization 

# Initialize a week chromosome 
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
                rn = random.randint(0, len(subject_batch_dict[(i*2)+2]))
                if rn <=len(subject_batch_dict[(i*2)+2])-1:
                    sub = subject_batch_dict[(i*2)+2][rn]
                    if course_type_dict[sub] == 'N':
                        if subject_credithour_dict[sub]>0:
                            slot[i] += sub
                            subject_credithour_dict[sub]-=1
                    elif course_type_dict[sub] == "L":
                        if subject_lab_credithour_dict[sub]>0:
                            slot[i] += sub
                            subject_lab_credithour_dict[sub]-=1
    return week

# week = initializeChromosome()
# for i in week:
#     print(i)
# for i in subject_credithour_dict:
#     print(i,subject_credithour_dict[i])
# for i in subject_lab_credithour_dict:
#     print(i,subject_lab_credithour_dict[i])


# Create a population 
popz = 100
pop = []
for i in range(popz):
    pop.append(initializeChromosome())
# for i in pop:
#     print(i)


# Fitness evaluation 

# No Faculty should have been assigned two different classes at same time ( in same slot of day )
# No Lab should be assigned to two different batches at same time

# We count the number of conflicts / Violations made in the chromosome and add 1/1+c score to the chromosome's final eval score
# if c is 0 the max value of 1 is added 

def fitnessFunction(chromosome):
    total_val = 0
    hconflicts = 0
    sconflicts = 0
    def hardConstraints(week):
        c = 0
        for day in week:
            for slot in day:
                for sub in slot:
                    for osub in slot:
                        if sub!='' and osub!='':   
                            # Faculty clash check
                            if sub!=osub and subject_teacher_dict[sub]==subject_teacher_dict[osub]:
                                c+=1
                            # Lab clash check
                            if sub!=osub and course_type_dict[sub]=='L' and course_type_dict[osub]=='L':   
                                if lab_alloted[subject_batch_ind_dict[sub]] == lab_alloted[subject_batch_ind_dict[osub]]:
                                    c+=1         
        return c//2

    def softContraints(week):
        c = 0
        for day in week:
            for slot in day:
                for sub in slot:
                    for osub in slot:
                        if sub!='' and osub!='':   
                            
                            
        return c//2
    

    hconflicts += hardConstraints(chromosome)
    # Add more conflicts here 
    total_val += 1/(1+hconflicts)
    total_val += 1/(2+sconflicts)

    return (1/(1+hconflicts))

# Fitness Calculations
Fit_values = []
for chromosome in pop:
    Fit_values.append(fitnessFunction(chromosome))

with open("best_chromosome.txt", "a") as f:
   f.write(str(pop[Fit_values.index(max(Fit_values))]))
   f.write("\n")

for i in range(len(pop)):
    print(pop[i],Fit_values[i])