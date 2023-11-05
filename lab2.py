import sys

def unify(clauseI, clauseJ, vars):
    for itemI in clauseI:
        for itemJ in clauseJ:
            for var in vars:
                    if itemI.find(var) != -1:
                        index = clauseI.index(itemI)
                        constant = itemJ[itemJ.find("(") + 1:itemJ.find(")")]
                        itemI = itemI.replace(var, constant)
                        clauseI[index] = itemI

                    elif itemJ.find(var) != -1:
                        index = clauseJ.index(itemJ)
                        constant = itemI[itemI.find("(") + 1:itemI.find(")")]
                        itemJ = itemJ.replace(var, constant)
                        clauseJ[index] = itemJ
    return clauseI, clauseJ

def negate(clause):
    if '!' in clause:
        return clause[1:]
    else:
        return '!' + clause


def resolve(clauseI, clauseJ, vars):
    new = []
    hasEmpty = False
    toAdd = False
    
    if len(vars) != 0:
        clauseI, clauseJ = unify(clauseI, clauseJ, vars)
    
    for iItem in clauseI:
        for jItem in clauseJ:
            #flip J
            #print(iItem, jItem)
            negatedJ = negate(jItem)
            #If they match after negation, combine the 2, but with the clause that negates deleted
            if iItem == negatedJ:
                holderI = clauseI.copy()
                holderJ = clauseJ.copy()
                holderI.remove(iItem)
                holderJ.remove(jItem)
                temp = holderI + holderJ
                newClause = " ".join(temp)
                if newClause == "":
                    #If new is empty, empty clause is found
                    return True, [], False
                
                new.append(newClause)
                toAdd = True
                
    return False, new, toAdd


def resolution(input):
    #Get info on KB
    with input as file:
        predicates= file.readline().split()
        predicates = predicates[1:]
        #print(predicates)
        
        variables = file.readline().split()
        variables = variables [1:]
        #print(variables)
        
        constants = file.readline().split()
        constants = constants[1:]
        #print(constants)
        
        functions = file.readline().split()
        functions = functions[1:]
        #print(functions)

        clauses = file.read().split()
        clauses = clauses[1:]
        #print(clauses)
        
    stillResolving = True
    while stillResolving:
        x = 0
        start = clauses.copy()
        while x < len(clauses):
            first = clauses[x]
            #handles if multiple clauses in single list
            first = first.strip().split()
            #start y after x pos, prevents repeat instances
            y = x + 1
            #fix off by one due to +1
            while y < len(clauses) - 1:
                second = clauses[y]
                second = second.strip().split()
                #hasEmpty -> does it contain []
                #new -> new clauses
                #toAdd -> contains new clauses to add to KB
                hasEmpty, new, toAdd = resolve(first, second, variables)
                
                if hasEmpty:
                    return False
                
                if toAdd:
                    for item in new:
                        if item not in clauses:
                            clauses += item
                y = y + 1
            x = x + 1
        if clauses == start:
            stillResolving = False
    return True
                                



if __name__ == '__main__':
    input = open(sys.argv[1])
    end = resolution(input)
    
    if end:
        print("yes")
    else:
        print("no")