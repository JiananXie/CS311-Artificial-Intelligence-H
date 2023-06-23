import time
import copy
import numpy as np

N = 5  # You should change the test size here !!!


def my_range(start, end):
    if start <= end:
        return range(start, end + 1)
    else:
        return range(start, end - 1, -1)


class Problem:
    char_mapping = ('·', 'Q')

    def __init__(self, n=4):
        self.n = n

    def is_valid(self, state):
        """
        check the state satisfy condition or not.
        :param state: list of points (in (row id, col id) tuple form)
        :return: bool value of valid or not
        """
        board = self.get_board(state)
        res = True
        for point in state:
            i, j = point
            condition1 = board[:, j].sum() <= 1
            condition2 = board[i, :].sum() <= 1
            condition3 = self.pos_slant_condition(board, point)
            condition4 = self.neg_slant_condition(board, point)
            res = res and condition1 and condition2 and condition3 and condition4
            if not res:
                break
        return res

    def is_satisfy(self, state):
        return self.is_valid(state) and len(state) == self.n

    def pos_slant_condition(self, board, point):
        i, j = point
        tmp = min(self.n - i - 1, j)
        start = (i + tmp, j - tmp)
        tmp = min(i, self.n - j - 1)
        end = (i - tmp, j + tmp)
        rows = my_range(start[0], end[0])
        cols = my_range(start[1], end[1])
        return board[rows, cols].sum() <= 1

    def neg_slant_condition(self, board, point):
        i, j = point
        tmp = min(i, j)
        start = (i - tmp, j - tmp)
        tmp = min(self.n - i - 1, self.n - j - 1)
        end = (i + tmp, j + tmp)
        rows = my_range(start[0], end[0])
        cols = my_range(start[1], end[1])
        return board[rows, cols].sum() <= 1

    def get_board(self, state):
        board = np.zeros([self.n, self.n], dtype=int)
        for point in state:
            board[point] = 1
        return board

    def print_state(self, state):
        board = self.get_board(state)
        print('_' * (2 * self.n + 1))
        for row in board:
            for item in row:
                print(f'|{Problem.char_mapping[item]}', end='')
            print('|')
        print('-' * (2 * self.n + 1))


def improving_bts(problem):
    action = []
    remain = []
    picked = []
    for i in range(N):
        temp = []
        for j in range(N):
            temp.append((i, j))
        remain.append(temp)
    if N >= 4:
        next = 0
        ans = go(problem,action,remain,picked,next)
        yield  ans



def valid_pos(action, remain):
    delet_remain = []
    row = 0
    a = action[-1]
    while row < N:
        temp = []
        for r in remain[row]:
            if a[0] == r[0] or a[1] == r[1] or abs(r[0] - a[0]) == abs(a[1] - r[1]):
                temp.append(r)
        delet_remain.append(temp)
        row = row + 1
    for row in range(N):
        for r in delet_remain[row]:
            remain[row].remove(r)
    return remain


def constraint(action, remain):
    num1 = 0
    num2 = 0
    for r1 in remain:
        num1 += len(r1)
    for r2 in valid_pos(action, remain):
        num2 += len(r2)
    return num1 - num2


def go(problem, action, remain, picked, next):
    if len(picked) == N or len(remain[next]) == 0:
        return action
    pos = []
    c = N*N
    for t in remain[next]:
        action.append(t)
        cop = copy.deepcopy(remain)
        cost = constraint(action, cop)
        if c > cost:
            c = cost
        action.pop()
    for t in remain[next]:
        action.append(t)
        cop = copy.deepcopy(remain)
        if c == constraint(action, cop):
            pos.append(t)
        action.pop()
    for p in pos:
        action.append(p)
        picked.append(next)
        copy_remain = copy.deepcopy(remain)
        rem = valid_pos(action, copy_remain)
        min = 0
        for r in range(N):
            if (len(rem[r]) < len(rem[min]) and len(rem[r]) != 0 or len(rem[min]) == 0 and min != r) and r not in picked :
                min = r
        n_action = copy.deepcopy(action)
        n_remain = copy.deepcopy(rem)
        n_picked = copy.deepcopy(picked)
        ans = go(problem, n_action, n_remain, n_picked, min)
        if len(ans) == N:
            return ans
        else:
            action.pop()
            picked.pop()
    return ans


# You can know what yield means in CSDN~
# test_block
n = N  # Do not modify this parameter, if you want to change the size, go to the first line of whole program. # here to select GUI or not
method = improving_bts  # here to change your method; bts or improving_bts
p = Problem(n)
start_time = time.time()
for actions in method(p):
    pass
p.print_state(actions)
print(time.time() - start_time)
