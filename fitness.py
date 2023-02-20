import itertools
from initialization import *
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
        # conflicts.append(0) # Blank class
        conflicts.append(0) # Repeated class
        conflicts.append(0) # lab second half
        for day in week:
            for j in range(4):
                day_classes = [day[i][j] for i in range(6)]

                # # Blank class conflict 
                # blank_class = day_classes.count('')
                # if blank_class == 0:
                #     conflicts[-3] += 0.1

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

        # If whole day is empty then 

        # Try not to fill the first slot of each day ( it is very early in morning )
        # for day in week:
        #     if day[0][0] =='':
        #         bonus+=1



        # number of occupied slots should not be more than 5
        return returnFit(conflicts)

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