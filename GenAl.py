import random
import PyEasyGa
import requests
import json

path = '24.txt'
individuals = 200
count_pairs = int(individuals / 2)
generations = 100
items = 30

mutating_percent = 0.2
change_percent = 0.3
f = open(path, 'r')
t = []

# list of prices for each individual
individ_price = {}
# list of individuals
dict_creature = {}


# 1. algorithm of greedy selection of the initial population
# returns total price of all items
def greedy_algorithm(cargo_capacity, capacity):
    global_price = 0
    individ_array = []
    for x in range(individuals):
        sum_cargo = 0
        sum_space = 0
        price = 0
        individ_array.append([0 for i in range(len(t))])

        rnd = random.randint(0, items - 1)
        for z in range(rnd, items):
            if sum_cargo + int(t[z][0]) < cargo_capacity and sum_space + float(t[z][1]) < capacity:
                individ_array[x][z] = 1
                sum_cargo += int(t[z][0])
                sum_space += float(t[z][1])
                price += int(t[z][2])
        global_price += price
        dict_creature.update({x: individ_array[x]})
        individ_price.update({x: price})
    return global_price


# 2. roulette selection of individuals for crossing over
# returns array of pairs for crossing over
def roulette_selection(sum_price):
    pairs = []
    for z in range(count_pairs):
        pairs.append([])
        for i in range(2):
            roulette = random.randint(0, sum_price)
            for x in dict_creature.keys():
                roulette -= individ_price[x]
                if roulette <= 0:
                    sum_price -= individ_price[x]
                    pairs[z].append(x)
                    dict_creature.pop(x)
                    individ_price.pop(x)
                    break
    return pairs


# 3. multipoint crossing over with 3 points (7|7|9|7)
# returns new population according to rules of crossing over
def crossingover():
    a = 7
    b = 14
    e = 23
    d = 30
    new_population = {}
    count = 199
    for c in parent_pairs:
        sel1_1 = copy_dict[c[0]][0:a]
        sel1_2 = copy_dict[c[0]][a:b]
        sel1_3 = copy_dict[c[0]][b:e]
        sel1_4 = copy_dict[c[0]][e:d]

        sel2_1 = copy_dict[c[1]][0:a]
        sel2_2 = copy_dict[c[1]][a:b]
        sel2_3 = copy_dict[c[1]][b:e]
        sel2_4 = copy_dict[c[1]][e:d]

        count += 1
        new_1 = sel1_1 + sel2_2 + sel1_3 + sel2_4
        new_population.update({count: new_1})

        count += 1
        new_2 = sel2_1 + sel1_2 + sel2_3 + sel1_4
        new_population.update({count: new_2})
    return new_population


def fitness_function(individual):
    sum_cargo = 0
    sum_space = 0
    price = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            sum_cargo += int(t[i][0])
            sum_space += float(t[i][1])
            price += int(t[i][2])
    if sum_cargo >= cargoCapacity or int(sum_space) >= capacityValue:
        price = 0
    return [price, sum_cargo, sum_space]


# randomly decide which individuals will be mutated in parental population
# 10% from parental population
def who_to_change_in_parent():
    mutation_array_parent = []
    while len(mutation_array_parent) != (individuals * mutating_percent) / 2:
        next = random.randint(0, 199)
        if next not in mutation_array_parent:
            mutation_array_parent.append(next)
    return mutation_array_parent


# randomly decide which individuals will be mutated in child population
# 10% from child population
def who_to_change_in_child():
    mutation_array_child = []
    while len(mutation_array_child) != (individuals * mutating_percent) / 2:
        next = random.randint(200, 399)
        if next not in mutation_array_child:
            mutation_array_child.append(next)
    return mutation_array_child


# 4. mutation of individuals
def mutation(who_is, key):
    is_added = False
    while not is_added:
        rnd_index = random.randint(0, items - 1)
        if who_is[key][rnd_index] == 0 and is_added is False:
            who_is[key][rnd_index] = 1
            is_added = True


# read file
firstLine = False
for line in f:
    if firstLine is False:
        first = line.split()
        firstLine = True
    else:
        listSplit = line.split()
        t.append(listSplit)

# initial bag with items
big_bag = t.copy()

cargoCapacity = int(first[0])
capacityValue = int(first[1])

# sort items according to their price
t.sort(key=lambda i: i[2], reverse=True)

# result of greedy algorithm
total_price = greedy_algorithm(cargoCapacity, capacityValue)

# after  greedy selection we also got list of individuals
# we copy it because in roulette selection we pop elements from dict_creature
# but this information will use later
copy_dict = dict_creature.copy()

# get best (max) price of individual in initial population
best_price = individ_price[max(individ_price, key=individ_price.get)]
gen_count = 0
qwe = 0
print("")

while gen_count != generations:
    # pairs of parents that are selected by roulette method
    parent_pairs = roulette_selection(total_price)

    # children of pair of parents
    descendants = crossingover()

    # we choose who will be changed 10% in parents' part and 10% in children's part (total 40)
    mutate_parents = who_to_change_in_parent()
    mutate_children = who_to_change_in_child()

    # we add one random thing to each individual in child population according to list of who will be mutated
    for index in mutate_children:
        mutation(descendants, index)
    # recalculate all the parameters for the individual
    result_dictionary_children = {}
    for line in descendants.keys():
        result_dictionary_children.update({line: fitness_function(descendants[line])})

    # add one random thing to each individual in parent population according to list of who will be mutated
    for index in mutate_parents:
        mutation(copy_dict, index)
    # recalculate all the parameters for the individual
    result_dictionary_parents = {}
    for line in copy_dict.keys():
        result_dictionary_parents.update({line: fitness_function(copy_dict[line])})

    # sort all populations
    # parents will be sorted in ascending order
    # children will be sorted in descending order

    sortedDictChild = sorted(result_dictionary_children.items(), key=lambda q: q[1], reverse=True)
    sortedDictParent = sorted(result_dictionary_parents.items(), key=lambda q: q[1], reverse=False)

    # 5. replace 30% of the worst individuals in parental population by descendants
    for x in range(int(individuals * change_percent)):
        sortedDictParent[x] = sortedDictChild[x]

    # sort new population that we got after replacement
    sortedDictParent = sorted(sortedDictParent, key=lambda x: x[1][0], reverse=True)

    # best individual in population
    result_individual = list(sortedDictParent)[0][0]
    # results for it
    other_result = list(sortedDictParent)[0][1]

    # we get its bag with items
    if result_individual in range(individuals):
        result_bag = copy_dict[result_individual]
    else:
        result_bag = descendants[result_individual]

    print("number generation ", gen_count)
    # because things in main bag were sorted we need to get their real indexes
    result_things_in_bag = []
    for x in range(len(result_bag)):
        if result_bag[x] == 1:
            for y in range(items):
                if t[x][2] == big_bag[y][2]:
                    result_things_in_bag.append(y+1)

    print("weight:", other_result[1])
    print("value:", other_result[0])
    print("volume:", int(other_result[2]))

    # indexes in main bag (that is located in file) start from 1 to 30
    print("items:", result_things_in_bag)

    if abs(best_price / other_result[0] - 1) > 0.1:
        best_price = other_result[0]
    else:
        break

    # part that includes all new data for the next generation
    # we need to set set to zero total price
    # also because keys of individual in initial population were from 0 to 199
    # and in child population from 200 to 399
    # there is a need to change indexes in result population that will be parental (or initial)
    # in next generation
    total_price = 0
    new_copy_dict = {}
    new_index = 0
    for each_key in dict(sortedDictParent).keys():
        if each_key in range(200, 400):
            new_copy_dict.update({new_index: descendants[each_key]})
            individ_price.update({new_index: result_dictionary_children[each_key][0]})
            total_price += result_dictionary_children[each_key][0]
            new_index += 1
        else:
            new_copy_dict.update({new_index: copy_dict[each_key]})
            individ_price.update({new_index: result_dictionary_parents[each_key][0]})
            total_price += result_dictionary_parents[each_key][0]
            new_index += 1

    dict_creature = new_copy_dict.copy()
    copy_dict = new_copy_dict.copy()
    gen_count += 1

print("")
print("weigth", PyEasyGa.best_results[0])
print("value", PyEasyGa.best[0])
print("volume", PyEasyGa.best_results[1])
print("items", PyEasyGa.best_results[2])


# post request
host = 'https://cit-home1.herokuapp.com/api/ga_homework'
header = {'content-type': 'application/json',
          'user-agent': 'Pankratova Jane 43506/1'}

dataRequest = json.dumps({"1": {"value": PyEasyGa.best[0],
                                "weight": PyEasyGa.best_results[0],
                                "volume": PyEasyGa.best_results[1],
                                "items": PyEasyGa.best_results[2]},

                          "2": {"value": other_result[0],
                                "weight": other_result[1],
                                "volume": int(other_result[2]),
                                "items": result_things_in_bag}})
postRequest = requests.post(host, data=dataRequest, headers=header)
print(postRequest)
print(postRequest.json())