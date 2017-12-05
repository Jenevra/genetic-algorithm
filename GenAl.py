import random

path = '24.txt'
individuals = 200
count_pairs = int(individuals / 2)
generations = 100
f = open(path, 'r')
t = []


individ_price = {}
dict_creature = {}


# algorithm of greedy selection of the initial population
def greedy_algorithm(cargo_capacity, capacity):
    global_price = 0
    individ_array = []
    for x in range(individuals):
        sum_cargo = 0
        sum_space = 0
        price = 0
        individ_array.append([0 for i in range(len(t))])

        rnd = random.randint(0, 29)
        for z in range(rnd, 30):
            if sum_cargo + int(t[z][0]) < cargo_capacity and sum_space + float(t[z][1]) < capacity:
                individ_array[x][z] = 1
                sum_cargo += int(t[z][0])
                sum_space += float(t[z][1])
                price += int(t[z][2])
        global_price += price
        dict_creature.update({x: individ_array[x]})
        individ_price.update({x: price})
    return global_price

#r
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


def mutation(who_is, key):
    is_added = False
    while not is_added:
        rnd_index = random.randint(0, 29)
        if who_is[key][rnd_index] == 0 and is_added is False:
            who_is[key][rnd_index] = 1
            is_added = True


def who_to_change_in_parent():
    mutation_array1 = []
    while len(mutation_array1) != 20:
        next1 = random.randint(0, 199)
        if next1 not in mutation_array1:
            mutation_array1.append(next1)
    return mutation_array1


def who_to_change_in_child():
    mutation_array = []
    while len(mutation_array) != 20:
        next = random.randint(200, 399)
        if next not in mutation_array:
            mutation_array.append(next)
    return mutation_array


firstLine = False
for line in f:
    if firstLine is False:
        first = line.split()
        firstLine = True
    else:
        listSplit = line.split()
        t.append(listSplit)


big_bag = t.copy()
cargoCapacity = int(first[0])
capacityValue = int(first[1])
t.sort(key=lambda i: i[2], reverse=True)



# total price of all individuals' prices

total_price = greedy_algorithm(cargoCapacity, capacityValue)
copy_dict = dict_creature.copy()
maxy = individ_price[max(individ_price, key=individ_price.get)]
gen_count = 0
best_price = maxy
qwe = 0
while gen_count != generations:
    # pairs of parents that are selected by roulette method
    parent_pairs = roulette_selection(total_price)

    # children of pair of parents
    descendants = crossingover()
    # we choose who will be changed 10% in parents' part and 10% in children's part (total 40)
    mutate_parents = who_to_change_in_parent()
    mutate_children = who_to_change_in_child()

    # here we add one random thing to each individual
    for index in mutate_children:
        mutation(descendants, index)

    result_dictionary_children = {}
    for line in descendants.keys():
        result_dictionary_children.update({line: fitness_function(descendants[line])})

    for index in mutate_parents:
        mutation(copy_dict, index)

    result_dictionary_parents = {}
    for line in copy_dict.keys():
        result_dictionary_parents.update({line: fitness_function(copy_dict[line])})

    sortedDictChild = sorted(result_dictionary_children.items(), key=lambda q: q[1], reverse=True)
    sortedDictParent = sorted(result_dictionary_parents.items(), key=lambda q: q[1], reverse=False)

    for x in range(60):
        sortedDictParent[x] = sortedDictChild[x]

    sortedDictParent = sorted(sortedDictParent, key=lambda x: x[1][0], reverse=True)

    result_individual = list(sortedDictParent)[0][0]
    other_result = list(sortedDictParent)[0][1]

    if result_individual in range(200):
        result_bag = copy_dict[result_individual]
    else:
        result_bag = descendants[result_individual]


    print("number generation ", gen_count)


    total_price = 0
    result_things_in_bag = []
    for x in range(len(result_bag)):
        if result_bag[x] == 1:
            for y in range(len(big_bag)):
                if t[x][2] == big_bag[y][2]:
                    result_things_in_bag.append(y+1)

    print("value:", other_result[0])
    print("weight:", other_result[1])
    print("volume:", int(other_result[2]))
    # indexes in real bag (that is located in file) start from 1 to 30
    print("items:", result_things_in_bag)

    if abs(best_price / other_result[0] - 1) > 0.1:
        best_price = other_result[0]
    else:
        break
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



