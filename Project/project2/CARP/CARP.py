from getopt import getopt
import sys
import math
import time
#get input(1)
args = getopt(sys.argv, "-t-s")[1]
path = args[1]
time_limit = float(args[3])
seed = args[5]
with open(path, "r") as f:
    contents = f.readlines()
vertices = int(contents[1].split(": ")[1])
depot = int(contents[2].split(": ")[1])
num_reqedges = int(contents[3].split(": ")[1])
num_nreqedges = int(contents[4].split(": ")[1])
vehicles = int(contents[5].split(": ")[1])
capacity = int(contents[6].split(": ")[1])
tot_cost_reqedges = int(contents[7].split(": ")[1])
#class node
class node:
    index = 0
    neibors = []

    def __init__(self):
        self.index = 0
        self.neibors = []

free_list = []
nodes = [node()]
costs = {}
demands = {}
distance = {}
ans_routes = []
ans_costs = 0

for i in range(vertices):
    nodes.append(node())
    nodes[i].index = i + 1
    distance[(i+1, i+1)] = 0
for i in range(1, vertices+1):
    for j in range(i+1, vertices+1):
        distance[(i, j)] = math.inf
        distance[(j, i)] = math.inf
#get input(2)
read_count = 9
line = contents[read_count].split()
while line[0] != 'END':
    node_1 = int(line[0])
    node_2 = int(line[1])
    costs[(node_1, node_2)] = int(line[2])
    costs[(node_2, node_1)] = int(line[2])
    distance[(node_1, node_2)] = int(line[2])
    distance[(node_2, node_1)] = int(line[2])
    demands[(node_1, node_2)] = int(line[3])
    demands[(node_2, node_1)] = int(line[3])
    nodes[node_1].neibors.append(node_2)
    nodes[node_2].neibors.append(node_1)
    if int(line[3]) > 0:
        free_list.append((node_1, node_2))
        free_list.append((node_2, node_1))
    read_count = read_count + 1   
    line = contents[read_count].split()

#Floyd
def Floyd():
    global distance
    for k in range(1, vertices+1):
        for i in range(1, vertices+1):
            for j in range(1, vertices+1):
                if distance[(i, j)] > distance[(i, k)] + distance[(k, j)]:
                   distance[(i, j)] = distance[(i, k)] + distance[(k, j)]

# Floyd()
# for i in range(1, vertices+1):
#     result = []
#     for j in range(1, vertices+1):
#         result.append(distance[(i,j)])
#     print(result)
#Path_Scanning
def Path_Scanning():
    global free_list, demands, costs, capacity, ans_costs, ans_routes, depot

    tot_cost = load = 0
    route = []
    end = depot
    task = (1,1)
    one_fit = False

    while len(free_list) != 0 :
        d = math.inf
        for arc in free_list:
            if demands[arc] + load <= capacity:
                one_fit = True
                if distance[(end,arc[0])] < d:
                    task = arc
                    d = distance[(end, arc[0])]
                elif distance[(end, arc[0])] == d and distance[(arc[1], depot)] > distance[(task[1], depot)]:
                    task = arc
        if one_fit:
            route.append(task)
            tot_cost = tot_cost + distance[(end,task[0])] + costs[task]
            load = load + demands[task]
            end = task[1]
            one_fit = False
            free_list.remove((task[0], task[1]))
            free_list.remove((task[1], task[0]))
        else:
            ans_costs = ans_costs + tot_cost + distance[(task[1], depot)]
            ans_routes.append(0)
            ans_routes.extend(route)
            ans_routes.append(0)
            tot_cost = load = 0
            route = []
            end = depot
            task = (1,1)
    if len(route) != 0 :
        ans_costs = ans_costs + tot_cost + distance[(task[1], depot)]
        ans_routes.append(0)
        ans_routes.extend(route)
        ans_routes.append(0)     

if __name__ == "__main__":
    start = time.time()
    Floyd()
    Path_Scanning()
    print("s 0", end="")
    for i in range(1, len(ans_routes)):
        if ans_routes[i] == 0:
            print(",0",end="")
        else:
            print(",(%d,%d)"%(ans_routes[i][0], ans_routes[i][1]), end="")
        if i == len(ans_routes) - 1:
            print()
    print("q %d"%ans_costs)
    run_time = (time.time() - start)
