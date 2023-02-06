import csv
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
subject_lab_credithour_dict = {}
subject_credithour_dict = {}
subject_batch_dict = {}


#--------------------------------------------#
for i in fp['Faculty_Name']:
    total_teacher_list.append(i)

for i in cp['Course_Name']:
    total_subject_list.append(i)
    
for i in cp['Semester']:
    total_batch_list.add(i)

tdf = cp.loc[cp['Type'] == 'L']
for i, j in zip(tdf['Course_Name'], tdf['NOCW']):
    subject_lab_credithour_dict[i] = j


tdf = cp.loc[cp['Type'] == 'L']
for i, j in zip(tdf['Course_Name'], tdf['NOCW']):
    subject_lab_credithour_dict[i] = j


for i in total_batch_list:
     tdf = cp.loc[cp['Semester'] == i]
     for j in tdf['Course_Code']:
        if i not in subject_batch_dict:
            subject_batch_dict[i] = [j]
        else:
            subject_batch_dict[i].append(j)

    

