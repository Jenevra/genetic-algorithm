from pyeasyga import pyeasyga

# Genetic Algorithm - fist task
# Using pyeasyga lib

sourceFile = open("24.txt", 'r')
t = []
firstLine = False
for line in sourceFile:
    if firstLine is False:
        first = line.split()
        firstLine = True
    else:
        listSplit = line.split()
        t.append(listSplit)


cargoCapacity = int(first[0])
capacityValue = float(first[1])

genetic_algorithm = pyeasyga.GeneticAlgorithm(t)
genetic_algorithm.population_size = 200


def fitness_function(individual, data):
    sum_cargo, sum_space, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            sum_cargo += int(item[0])
            sum_space += float(item[1])
            price += int(item[2])
    if sum_cargo >= cargoCapacity or sum_space >= capacityValue:
        price = 0
    return price


def calculate(things):
    sum_cargo, sum_space = 0, 0
    items = []
    for x in range(len(things)):
        if things[x] == 1:
            sum_cargo += int(t[x][0])
            sum_space += float(t[x][1])
            items.append(x+1)
    return [sum_cargo, int(sum_space), items]


genetic_algorithm.fitness_function = fitness_function
genetic_algorithm.run()

best = genetic_algorithm.best_individual()
best_results = calculate(best[1])
# print(best_results)

