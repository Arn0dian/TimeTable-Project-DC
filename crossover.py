from initialization import*
from fitness import *

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