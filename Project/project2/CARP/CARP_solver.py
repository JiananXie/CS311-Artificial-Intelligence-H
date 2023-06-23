from getopt import getopt
import sys
import math
import time
import copy
import random
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
# random.seed(seed)

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
# Path_Scanning
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

def flipping():
    global ans_costs, ans_routes
    tmp_routes = copy.deepcopy(ans_routes)
    tmp_costs = ans_costs
    for i in range(len(tmp_routes)): 
        origin_cost = 0
        new_cost = 0
        if tmp_routes[i] != 0:
            if i > 0:
                if tmp_routes[i-1] == 0: 
                    origin_cost += distance[(depot, tmp_routes[i][0])]
                    new_cost += distance[(depot, tmp_routes[i][1])]

                else:
                    origin_cost += distance[(tmp_routes[i-1][1], tmp_routes[i][0])]
                    new_cost += distance[(tmp_routes[i-1][1], tmp_routes[i][1])]
            if i < len(tmp_routes)-1:
                if tmp_routes[i+1] == 0:
                    origin_cost += distance[(tmp_routes[i][1], depot)]
                    new_cost += distance[(tmp_routes[i][0], depot)]
                else:
                    origin_cost += distance[(tmp_routes[i][1], tmp_routes[i+1][0])]
                    new_cost += distance[(tmp_routes[i][0], tmp_routes[i+1][0])]
        if origin_cost > new_cost:
            tuple = tmp_routes[i]
            new_tuple = (tuple[1], tuple[0])
            tmp_routes[i] = new_tuple
            tmp_costs -= (origin_cost - new_cost)
    return tmp_routes, tmp_costs

def self_single_insertion():
    global depot, ans_routes, ans_costs, costs
    vehicle_routes = split_routes(ans_routes)
    tmp_costs = ans_costs
    tmp_routes = copy.deepcopy(ans_routes)
    route_pos = random.randint(0,len(vehicle_routes)-1)
    route = copy.deepcopy(vehicle_routes[route_pos])
    task_pos = random.randint(0,len(route)-1)
    task = route[task_pos]
    picked_pos =random.randint(0,len(route)-1)
    origin_costs = distance[(depot, route[0][0])]
    for i in range(len(route)):
        if i + 1 == len(route):
            origin_costs += distance[(route[i][1], depot)]
        else:
            origin_costs += distance[(route[i][1], route[i+1][0])]
    route.remove(task)
    route.insert(picked_pos,task)
    new_costs = distance[(depot, route[0][0])]
    for i in range(len(route)):
        if i + 1 == len(route):
            new_costs += distance[(route[i][1], depot)]
        else:
            new_costs += distance[(route[i][1], route[i+1][0])]
    if origin_costs > new_costs:
        tmp_costs -= (origin_costs - new_costs)
        tmp_routes.remove(task)
        pos = 0
        for k in range(route_pos):
            pos += (len(vehicle_routes[k]) + 2)
            pos += (1+task_pos)
        tmp_routes.insert(pos,task)
    return tmp_routes, tmp_costs

def split_routes(routes):
    vehicle_routes = []
    route = []
    for i in range(len(routes)):
        if routes[i] == 0 and (i+1 == len(routes) or routes[i+1] == 0 ):
            vehicle_routes.append(route)
            route = []
        elif routes[i] != 0:
            route.append(routes[i])
    return vehicle_routes

if __name__ == "__main__":
    start = time.time()
    Floyd()
    Path_Scanning()
    while time.time() - start <= time_limit:
        tmp_routes, tmp_costs = self_single_insertion()
        tmp_routes, tmp_costs = flipping()
        if tmp_costs < ans_costs:
            ans_costs = tmp_costs
            ans_routes = tmp_routes
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
    print("Cost:%f s"%run_time)
