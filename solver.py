# -*- coding: utf-8 -*-
from utils import *
import copy
import time
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

adjacenyList = {}

def initAdjList():
    global adjacenyList
    for i in range(9):
        for j in range(9):
            c = (i, j)
            adjacenyList[c] = []
            adjacenyList[c].append(get_col_set(c))
            adjacenyList[c].append(get_row_set(c))
            adjacenyList[c].append(get_block_set(c))
            adjacenyList[c].append(get_all_set(c))


isOptimisationActive = True

def activateOptimisation():
    global isOptimisationActive
    isOptimisationActive = True

def deactivateOptimisation():
    global isOptimisationActive
    isOptimisationActive = False


def validateIter(state):
    global isOptimisationActive
    opCount = 0
    for i in range(9):
        for j in range(9):
            initialLen = len(state[(i,j)])
            if initialLen > 1:
                # def validateCell(c,state):
                state[(i,j)] = "".join(sorted(set(state[(i,j)]) - set([state[x] for x in get_all_set((i,j)) if len(state[x]) == 1])))
                if isOptimisationActive:
                    alternative((i,j),state)
                opCount += initialLen - len(state[(i,j)])
    return opCount

def validate(state):
    while(True):
        val = validateIter(state)
        if val == 0:
            break


def alternative(c, state):
    val = gen_row_prob(c,state)
    if len(val) == 1:
        state[c] = "".join(sorted(val))
    else:
        val = gen_col_prob(c,state)
        if len(val) == 1:
            state[c] = "".join(sorted(val))
        else:
            val = gen_block_prob(c,state)
            if len(val) == 1:
                state[c] = "".join(sorted(val))


def init(state, input):
    for i in range(9):
        for j in range(9):
            c = (i,j)
            l = input[i*9 + j]
            if l != '.':
                if not assign(state, c, l):
                    return False

    return state

def assign(state, location, v):
    remove = state[location].replace(v, '')

    for i in remove:
        if propagate(state, location, i):
            continue
        else:
            return False

    return state


def hasContradiction(state, c):
    if len(state[c]) == 0:
        # GAP!
        return True
    elif len(state[c]) == 1:
        for s2 in adjacenyList[c][3]:
            if not propagate(state, s2, state[c]):
                return True
            else:
                continue

    return False

def propagate(state, c, d):
    if d not in state[c]:
        return state

    state[c] = state[c].replace(d, '')

    if hasContradiction(state, c):
        return False

    for adj_type in range(3):
        dplaces = [c for c in adjacenyList[c][adj_type] if d in state[c]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(state, dplaces[0], d):
                return False

    return state

def findFirst(state):
    scores = []
    for i in range(9):
        for j in range(9):
            c = (i,j)
            if len(state[c]) > 1:
                return c

def solve_dfs(state, counter, item_id = 0):
    if state is False:
        return False
    elif isCompleted(state):
        return state
    else:
        c = getIJ(item_id)
        # select any pos.
        for val in state[c]:
            counter['dfs'] = counter['dfs'] + 1
            result = solve_dfs(assign(copy.deepcopy(state), c, val), counter, item_id+1)
            if result:
                return result
        return False

def solve_idfs(state, counter, depth = 0, depth_start = 8):
    currentDepth = depth_start
    while(True):

        result = solve_idfs_partial(state, counter, 0, currentDepth)
        if result:
            return result
        else:
            currentDepth = currentDepth + 1


def solve_idfs_partial(state, counter, depth, maxDepth):
    if state is False:
        return False
    elif isCompleted(state):
        return state
    elif depth > maxDepth:
        return False
    else:
        c = findFirst(state)
        for val in state[c]:
            counter['idfs'] = counter['idfs'] + 1
            result = solve_idfs_partial(assign(copy.deepcopy(state), c, val), counter, depth + 1, maxDepth)
            if result:
                return result
        return False


def findBest(state):
    scores = []
    for i in range(9):
        for j in range(9):
            c = (i,j)
            if len(state[c]) > 1:
                scores.append((len(state[c]), c))
    return min(scores)[1]

def findBest_2(state):
    scores = []
    for i in range(9):
        for j in range(9):
            c = (i,j)
            if len(state[c]) > 1:
                scores.append((sum([len(state[x]) for x in get_all_set(c)]), c))
    return min(scores)[1]


def solve_bfs(state, counter):
    if state is False:
        return False
    elif isCompleted(state):
        return state
    else:
        c = findBest(state)
        for val in state[c]:
            counter['bfs'] = counter['bfs'] + 1
            result = solve_bfs(assign(copy.deepcopy(state), c, val), counter)
            if result:
                return result
        return False

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False


def depth_example():

    ps = get_puzzles_from_file("hard95.txt")

    # Table Header
    # print("—"*63)
    # print("│ {:^20} │ {:^10} │ {:^10} │ {:^10} │".format(*['Test Case', 'Algorithm', 'State', 'Time']))
    # print("—"*63)

    stateCount = {'idfs':0,'idfs_2':0,'idfs_4':0,'idfs_8':0,'idfs_12':0,'idfs_16':0,'idfs_20':0}
    timer = {'idfs_2':0,'idfs_4':0,'idfs_8':0,'idfs_12':0,'idfs_16':0,'idfs_20':0}

    initAdjList()

    for m in range(0,5):
        state = empty_state()

        beginTime = time.clock()
        init(state, ps[m])
        inTime = (time.clock() - beginTime)
        beginTime = time.clock()

        beginTime = time.clock()
        solved_idfs = solve_idfs(state, counter=stateCount, depth_start=2)
        timer['idfs_2'] = timer['idfs_2'] + (time.clock() - beginTime) + inTime
        stateCount['idfs_2'] = stateCount['idfs_2'] + stateCount['idfs']
        stateCount['idfs'] = 0

        beginTime = time.clock()
        solved_idfs = solve_idfs(state, counter=stateCount, depth_start=4)
        timer['idfs_4'] = timer['idfs_4'] + (time.clock() - beginTime) + inTime
        stateCount['idfs_4'] = stateCount['idfs_4'] + stateCount['idfs']
        stateCount['idfs'] = 0

        beginTime = time.clock()
        solved_idfs = solve_idfs(state, counter=stateCount, depth_start=8)
        timer['idfs_8'] = timer['idfs_8'] + (time.clock() - beginTime) + inTime
        stateCount['idfs_8'] = stateCount['idfs_8'] + stateCount['idfs']
        stateCount['idfs'] = 0

        beginTime = time.clock()
        solved_idfs = solve_idfs(state, counter=stateCount, depth_start=12)
        timer['idfs_12'] = timer['idfs_12'] + (time.clock() - beginTime) + inTime
        stateCount['idfs_12'] = stateCount['idfs_12'] + stateCount['idfs']
        stateCount['idfs'] = 0

        beginTime = time.clock()
        solved_idfs = solve_idfs(state, counter=stateCount, depth_start=16)
        timer['idfs_16'] = timer['idfs_16'] + (time.clock() - beginTime) + inTime
        stateCount['idfs_16'] = stateCount['idfs_16'] + stateCount['idfs']
        stateCount['idfs'] = 0

        beginTime = time.clock()
        solved_idfs = solve_idfs(state, counter=stateCount, depth_start=20)
        timer['idfs_20'] = timer['idfs_20'] + (time.clock() - beginTime) + inTime
        stateCount['idfs_20'] = stateCount['idfs_20'] + stateCount['idfs']
        stateCount['idfs'] = 0

    # print(resultTable)
    #     print(stateCount)
    #     print(timer)

    return {
        'file': "hard95.txt",
        'time': timer,
        'state': stateCount
    }
    # print ('(%.2f seconds)\n' % t)



def sudoku_solver(file, algo = None,  case = -1):

    ps = get_puzzles_from_file(file)

    # Table Header
    # print("—"*63)
    # print("│ {:^20} │ {:^10} │ {:^10} │ {:^10} │".format(*['Test Case', 'Algorithm', 'State', 'Time']))
    # print("—"*63)

    stateCount = {'dfs':0,'bfs':0,'idfs':0}
    timer = {'dfs':0,'bfs':0,'idfs':0}


    # Decide range
    if case == -1:
        caseText = "Test results for all cases in " + file
        ranger = range(len(ps)-1)
    elif type(case) is range:
        caseText = "Test results for given case list"
        ranger = case
    else:
        caseText = "Test results for case-"+str(case)+" in "+file
        ranger = range(case, case + 1)

    print(caseText)

    initAdjList()

    for m in ranger:
        state = empty_state()

        beginTime = time.clock()
        init(state, ps[m])
        inTime = (time.clock() - beginTime)
        beginTime = time.clock()
        solved_dfs = solve_dfs(state, counter = stateCount)
        timer['dfs'] = timer['dfs'] + (time.clock() - beginTime) + inTime

        beginTime = time.clock()
        solved_bfs = solve_bfs(state, counter = stateCount)
        timer['bfs'] = timer['bfs'] + (time.clock() - beginTime) + inTime

        beginTime = time.clock()
        solved_idfs = solve_idfs(state, counter=stateCount)
        timer['idfs'] = timer['idfs'] + (time.clock() - beginTime) + inTime

    # print(resultTable)
    #     print(stateCount)
    #     print(timer)

    return {
        'file': file,
        'time': timer,
        'state': stateCount,
        'count': len(ranger)
    }
    # print ('(%.2f seconds)\n' % t)

def constraint_example():
    focus = (6,7)
    ps = get_puzzles_from_file("easy50.txt")
    state = gen_state_from_str(ps[5])
    print_grid(state)

    print("Please focus on the cell ", focus, "\n")

    deactivateOptimisation()
    validate(state)
    print_grid(state)

    before = totalPossibility(state)
    print("Current possible value set is: ", state[focus], "\n")
    print("Total Possibility: ", before, "\n")

    activateOptimisation()
    validate(state)
    print_grid(state)
    after = totalPossibility(state)
    print("Current possible value set is: ", state[focus], "\n")
    print("Total Possibility: ", after, "\n")

    print("Change in Possibilities; \n")
    print("Before / After = ", before, " / ", after, " = ", (before / after))


"""
        elif algo == None:
            print("Cross Testing")
        else:
            print(algo, " Algorithm does not exist. Please try dfs or bfs or idfs")
"""


def compareDepth(resultSet):
    objects = (2,4,8,12,16,20)
    y_pos = np.arange(len(objects))
    performance = [resultSet['state']['idfs_2'], resultSet['state']['idfs_4'], resultSet['state']['idfs_8'],
                   resultSet['state']['idfs_12'], resultSet['state']['idfs_16'], resultSet['state']['idfs_20']
                   ]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('State Count')
    plt.xlabel('Initial Depth')
    plt.title('I-DFS - Affect of Initial Depth')

    plt.show()

def compareState(resultSet):
    objects = ('DFS', 'BFS', 'I-DFS')
    y_pos = np.arange(len(objects))
    performance = [resultSet['state']['dfs'] / resultSet['count'], resultSet['state']['bfs']/ resultSet['count'], resultSet['state']['idfs']/ resultSet['count']]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('State Count')
    plt.title('Sudoku Solving Algoritm ('+resultSet['file']+')')

    plt.show()

def compareTime(resultSet):
    objects = ('DFS', 'BFS', 'I-DFS')
    y_pos = np.arange(len(objects))
    performance = [resultSet['time']['dfs']/ resultSet['count'], resultSet['time']['bfs']/ resultSet['count'], resultSet['time']['idfs']/ resultSet['count']]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Avg Time (s)')
    plt.title('Sudoku Solving Algoritm ('+resultSet['file']+')')

    plt.show()

def infoTableState(resultSet):
    print("—"*58)
    print("│ {:^15} │ {:^10} │ {:^10} │ {:^10} │".format(*['', 'DFS', 'BFS', 'I-BFS']))
    print("—"*58)
    print("│ {:^15} │ {:^10} │ {:^10} │ {:^10} │".format(*['State (total)', resultSet['state']['dfs'], resultSet['state']['bfs'], resultSet['state']['idfs']]))
    print("—" * 58)
    print("│ {:^15} │ {:^10} │ {:^10} │ {:^10} │".format(
        *['State(avg)',
          '%.2f' %(resultSet['state']['dfs'] / resultSet['count']),
          '%.2f' % (resultSet['state']['bfs'] / resultSet['count']),
          '%.2f' % (resultSet['state']['idfs'] / resultSet['count'])]))
    print("—" * 58)

def infoTableTime(resultSet):
    print("—" * 78)
    print("│ {:^20} │ {:^15} │ {:^15} │ {:^15} │".format(*['', 'DFS', 'BFS', 'I-BFS']))
    print("—" * 78)
    print("│ {:^20} │ {:^15} │ {:^15} │ {:^15} │".format(
        *['Time(total ms)', '%.2f ms' % (resultSet['time']['dfs'] *1000), '%.2f ms' % (resultSet['time']['bfs']*1000), '%.2f ms' % (resultSet['time']['idfs'] *1000)]))
    print("—" * 78)
    print("│ {:^20} │ {:^15} │ {:^15} │ {:^15} │".format(
        *['Time(avg ms)', '%.2f ms' % (resultSet['time']['dfs'] * 1000 / resultSet['count']), '%.2f ms' % (resultSet['time']['bfs'] * 1000 / resultSet['count']),
          '%.2f ms' % (resultSet['time']['idfs'] * 1000 / resultSet['count'])]))
    print("—" * 78)

# print(depth_example())
# print(sudoku_solver(file = "easy50.txt", case = 0))
