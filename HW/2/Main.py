import string


def assign_the_grammar():
    file = open(my_path + "grammar.txt", "r")
    production_dict = dict()
    for r in file.readlines():
        r = r.replace("\n", "").replace(";", "")
        production_dict[r.split("-")[0]] = r.split(">")[1].split("|")
    return production_dict


def adding_a_grammar(productions, checked, key, vars_list):
    products = []
    for p in productions[key]:
        if len(p) is 1 and p in vars_list:
            if p not in checked:
                checked.append(p)
                products.extend(adding_a_grammar(productions, checked, p, vars_list))
        else:
            products.append(p)
    return products


def print_the_grammar(production, text=None):
    print(text)
    for key, value in production.items():
        print(key, "->", value)


def delete_unit_grammar(productions, vars_list):
    deleted = dict()
    for key in productions:
        checked_list = []
        deleted[key] = list()
        for value in productions[key]:
            if len(value) is 1 and value in vars_list:
                checked_list.append(key)
                productions[key].extend(adding_a_grammar(productions, checked_list, value, vars_list))
                deleted[key].append(value)
                productions[key] = list(dict.fromkeys(productions[key]))
    for key, value in deleted.items():
        for v in value:
            productions[key].remove(v)


def separate_productions(productions, all_variables):
    temp = dict()
    flag = True
    for key in productions:
        for i in range(len(productions[key])):
            value = productions[key][i]
            if len(value) > 2:
                flag = False
                productions[key][i] = value[0:1] + all_variables[0]
                x = list()
                x.append(value[1:])
                temp[all_variables.pop(0)] = x
    productions.update(temp)
    return flag


def delete_terminal_production(productions, terminals, variables, all_variables):
    terminals_to_variables = dict()
    for t in terminals.readlines():
        for temp in t.split(","):
            terminals_to_variables[all_variables[0]] = list(temp)
            variables.append(all_variables.remove(all_variables[0]))
    for key in productions:
        for i in range(len(productions[key])):
            value = productions[key][i]
            if len(value) is 1: continue
            temp = value
            for t_k in terminals_to_variables:
                temp = temp.replace(terminals_to_variables[t_k][0], t_k)
            productions[key][i] = temp
    productions.update(terminals_to_variables)


def setting_the_variables():
    vars_list = []
    for s in open(my_path + "variables.txt", "r").readline():
        if s in all_variables:
            all_variables.remove(s)
            vars_list.append(s)
    return vars_list


def do_process(my_path):
    terminals = open(my_path + "terminals.txt", "r")
    variables = setting_the_variables()
    grammars = assign_the_grammar()
    delete_unit_grammar(grammars, variables)
    delete_terminal_production(grammars, terminals, variables, all_variables)
    while True:
        if separate_productions(grammars, all_variables):  # tested
            break
    print_the_grammar(grammars, "Chomsky Normal Form is:")


all_variables = list(string.ascii_uppercase)
for i in range(6):
    path = 'test_cases\\'
    my_path = path + str(i + 1) + "\\"
    print("Test " + str(i + 1) + ":")
    do_process(my_path)
