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
    for i in total_batch_list:
        tdf = cp.loc[cp['Semester'] == i]
        sch = 0
        for j in tdf['NOCW']:
            sch+=j
        subject_batch_dict[i].append('NC'+str(i))
        no_class_hours_dict['NC'+str(i)] = 30-sch
        course_type_dict['NC'+str(i)] = 'NC'
        
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
                           

    # Add remaining classes brute-force-ly or think of something else

    return week

# week = initializeChromosome()
# for i in week:
#     print(i)
# for i in subject_credithour_dict:
#     print(i,subject_credithour_dict[i])
# for i in subject_lab_credithour_dict:
#     print(i,subject_lab_credithour_dict[i])

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
popz = 50
pop = []
for i in range(popz):
    pop.append(initializeChromosome())
# for i in pop:
#     print(i)

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
        f1 = 0
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

        f1 = 1/(1+c1)
        # Faculty should get a slot off after teaching 2 hours continously ( not nessacary to same batch )  
        # for day in week:
        #     for i in range(5):
        #         print(day[i],day[i+1])
        #         for s1 in day[i]:
        #             # How to handle faculty conflicts and repeating classes ?
        #             for s2 in day[i+1]:


        # Every batch should have only one class of 2 continous classes 
        # And no class should be repeated after later in day or should only be 2 hours class
        
        # We calculate these conflicts by calculating the total count of a subject in a day and the longest continous class of 
        # that subject ; then no. of conflict = (total class - longest class) + (longest class - 2)
        f2 =0
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
                        # Added the conflicts 
                        if lc == 1:
                            c2+= (tc-lc)
                        else:
                            c2+= (tc-lc)+(lc-2)

                if len(two_class_day)>1:
                    c2+= len(two_class_day)-1
                two_class_day.clear()
                classes_in_day.clear()
                day_classes = []

        f2 = 1/(1+c2)
        return f1+f2

    fitness_value += hardConstraints(chromosome)
    # total_val += 1/(2+sconflicts)

    return (fitness_value)


# Fitness Calculations

Fit_values = []
for chromosome in pop:
    Fit_values.append(fitnessFunction(chromosome))

# for i in range(len(pop)):
#     print(pop[i],Fit_values[i])

print(pop[Fit_values.index(max(Fit_values))],max(Fit_values))