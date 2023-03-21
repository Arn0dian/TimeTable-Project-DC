import itertools
from initialization import *
# No Faculty should have been assigned two different classes at same time ( in same slot of day )
# No Lab should be assigned to two different batches at same time

# We count the number of conflicts / Violations made in the chromosome and add 1/1+c score to the chromosome's final eval score
# if c is 0 the max value of 1 is added 
def returnFit(x):
    return sum([1/(1+i) for i in x])

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
                 

def fitnessFunction(chromosome):
    conflicts = []
    fitness_value = 0

    # chromosome = substoweek(list(chromosome))

    def hardConstraints(week):

        # 1 No faculty should have two classes alloted in same slot of time
        # 1 No two batches should have same lab alloted to them in same slot of time
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
        conflicts.append(0) # 2 Blank class
        conflicts.append(0) # 3 Repeated class
        conflicts.append(0) # 4 lab second half
        for day in week:
            for j in range(4):
                day_classes = [day[i][j] for i in range(6)]

                # Blank class conflict 
                blank_class = day_classes.count('')
                if blank_class == 0:
                    conflicts[-3] += 0.2

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

        # 5 Class after lunch and before lunch should not be same                       
        conflicts.append(0)
        for day in week:
            if set(day[2]).intersection(set(day[3]))!=set(): 
                conflicts[-1] += 1

        # Try to check if each day have more

        # 6 Try not to fill the first slot of each day ( it is very early in morning )
        conflicts.append(0)
        for day in week:
            if day[0]!=['','','','']:
                conflicts[-1]+=0.1

        # 7 Class hour discontinuity : breakage between two classes 
        conflicts.append(0)
        for day in week:
            conflicts_day = []
            for j in range(4):
                cc = sum([1 for i in range(6) if day[i][j] != ''])
                conflicts_day.append(cc)
            if max(conflicts_day) > 1:
                conflicts[-1] += 0.5

        # 8 Try to have atleast one 2 hours continous class of a subject with credit >= 3
        conflicts.append(0)
        for day in week:
            for j in range(4):
                classes = []
                for i in range(6):
                    classes.append(day[i][j])
                cool_subjects = {}
                if classes[0]!='' and classes[0] == classes[1]:
                    if classes[0] in subject_tcredithour_dict:
                        cool_subjects[classes[0]] = 1
                elif classes[1]!='' and classes[2] == classes[1]:
                    if classes[0] in subject_tcredithour_dict:
                        cool_subjects[classes[0]] = 1
                elif classes[3]!='' and classes[4] == classes[1]:
                    if classes[0] in subject_tcredithour_dict:
                        cool_subjects[classes[0]] = 1
                elif classes[4]!='' and classes[5] == classes[1]:
                    if classes[0] in subject_tcredithour_dict:
                        cool_subjects[classes[0]] = 1

                conflicts[-1]+= (len(subject_tcredithour_dict)-len(cool_subjects))/10





        # 9 Subjects held today will not be held tommorow
        

        
        

        # 10 Try to spread class evenly across all days

        # conflicts.append(0)
        # y1 , y2 , y3 , y4 = separateChromosome(week)
        # l = 0
        # countcl = cp['Semester'].value_counts()[2]
        # count
        # print(count)
        # for day in y1:
        #     l+= (len(y1[day])-(y1[day].count('')))/5
        # print(l)                    
        
        # 11 Try to only have 1 two hour class in a day for every batch
        #  



        # print(conflicts)
        # number of occupied slots should not be more than 5
        return returnFit(conflicts)

    fitness_value += hardConstraints(chromosome)
    return (fitness_value)

# for chromosome in pop:
#     fitness = fitnessFunction(chromosome)
#     pop[chromosome] = fitness

    
# Fitness Calculations
Fit_values = []
for chromosome in pop:
    Fit_values.append(fitnessFunction(chromosome))

# for i in range(len(pop)):
#     print(pop[i],Fit_values[i])
# print(pop[Fit_values.index(max(Fit_values))],max(Fit_values))

#---------------------------------------------------------------------------#