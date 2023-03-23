
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
