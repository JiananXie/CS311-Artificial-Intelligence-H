import numpy as np
import random
import time
import math
import copy

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)

direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
pos_weight = np.array([[800, -100, -50, -60, -60, -50, -100, 800],
                       [-100, -50, 1, 1, 1, 1, -50, -100],
                       [-50, 1, 3, 2, 2, 3, 1, -50],
                       [-60, 1, 2, 1, 1, 2, 1, -60],
                       [-60, 1, 2, 1, 1, 2, 1, -60],
                       [-50, 1, 3, 2, 2, 3, 1, -50],
                       [-100, -50, 1, 1, 1, 1, -50, -100],
                       [800, -100, -50, -60, -60, -50, -100, 800]])


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need to add your decision to your candidate_list. The system will get the end of your candidate_list as your decision.
        self.candidate_list = []

    # The input is the current chessboard. Chessboard is a numpy array.
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        self.candidate_list = self.valid_position(chessboard, self.color)
        # begin = time.time()
        if len(self.candidate_list) != 0:
            blank = np.argwhere(chessboard == COLOR_NONE)
            if len(blank) > 40:
                _, move = self.alphabeta_go(chessboard, 1)
            elif len(blank) > 35:
                _, move = self.alphabeta_go(chessboard, 2)
            elif len(blank) > 10:
                _, move = self.alphabeta_go(chessboard, 3)
            elif len(blank) > 5:
                _, move = self.alphabeta_go(chessboard, 4)
            else:
                _, move = self.alphabeta_go(chessboard, 5)
            self.candidate_list.append(move)
        # end = time.time()
        # print(end - begin)

    def alphabeta_go(self, chessboard, depth):

        def max_value(state, alpha, beta, depth):
            if self.is_terminal(state, self.color) or depth == 0:
                return self.evalutation(state), None
            value, move = -math.inf, None
            valid_pos = self.valid_position(state, self.color)
            # actions = sorted(valid_pos, key=lambda a: self.evalutation(self.next_state(state, a, self.color)), reverse=True)
            for action in valid_pos:
                v_tmp, _ = min_value(self.next_state(state, action, self.color), alpha, beta, depth - 1)
                if value < v_tmp:
                    value = v_tmp
                    move = action
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value, move

        def min_value(state, alpha, beta, depth):
            if self.is_terminal(state, -self.color) or depth == 0:
                return self.evalutation(state), None
            value, move = math.inf, None
            valid_pos = self.valid_position(state, -self.color)
            # actions = sorted(valid_pos, key=lambda a: self.evalutation(self.next_state(state, a, self.color)), reverse=False)
            for action in valid_pos:
                v_tmp, _ = max_value(self.next_state(state, action, -self.color), alpha, beta, depth - 1)
                if value > v_tmp:
                    value = v_tmp
                    move = action
                if value <= alpha:
                    break
                beta = min(beta, value)
            return value, move

        return max_value(chessboard, -math.inf, +math.inf, depth)

    def valid_position(self, chessboard, color):
        valid_pos = []
        mychesses = np.argwhere(chessboard == color)
        for mychess in mychesses:
            for dx, dy in direction:
                flag = False
                x = mychess[0] + dx
                y = mychess[1] + dy
                if self.within_bound(x, y) and chessboard[x][y] == -color:
                    flag = True
                while flag == True and self.within_bound(x, y):
                    if chessboard[x][y] == color:
                        break
                    elif chessboard[x][y] == COLOR_NONE:
                        if (x, y) not in valid_pos:
                            valid_pos.append((x, y))
                        break
                    x = x + dx
                    y = y + dy
        return valid_pos

    def is_terminal(self, chessboard, color):
        my_full = True
        oppo_full = True
        full = True
        can_move = True
        mychesses = np.argwhere(chessboard == self.color)
        oppochesses = np.argwhere(chessboard == -self.color)
        if len(mychesses) + len(oppochesses) < 64:
            full = False
        if len(mychesses) != 0:
            oppo_full = False
        if len(oppochesses) != 0:
            my_full = False
        if len(self.valid_position(chessboard, color)) == 0:
            can_move = False
        if my_full or oppo_full or full or not can_move:
            return True
        return False

    def within_bound(self, x, y):
        if 0 <= x <= 7 and 0 <= y <= 7:
            return True
        else:
            return False

    def evalutation(self, state):
        my_chess = np.argwhere(state == self.color)
        oppo_chess = np.argwhere(state == -self.color)

        def pos_value():
            return sum(sum(state * pos_weight)) * (-self.color)

        def move_value():
            my_move = self.valid_position(state, self.color)
            oppo_move = self.valid_position(state, -self.color)
            return len(my_move) - len(oppo_move)

        def stable_value():
            my_stable = 0
            oppo_stable = 0
            my_path = self.valid_path(state, self.color)
            oppo_path = self.valid_path(state, -self.color)
            for oc in oppo_chess:
                if tuple(oc) not in my_path:
                    oppo_stable += 1
            for mc in my_chess:
                if tuple(mc) not in oppo_path:
                    my_stable += 1
            return my_stable - oppo_stable

        def count_value():
            return len(my_chess) - len(oppo_chess)

        if self.is_terminal(state, self.color) or self.is_terminal(state, -self.color):
            if len(my_chess) < len(oppo_chess):
                return 1000 + pos_value() + -3 * move_value() - 30 * stable_value() - 35 * count_value()
            elif len(my_chess) > len(oppo_chess):
                return -1000 + pos_value() + -3 * move_value() - 30 * stable_value() - 35 * count_value()
            else:
                return pos_value() + -3 * move_value() - 30 * stable_value() - 35 * count_value()
        else:
            stage = len(np.argwhere(state == COLOR_NONE))
            if stage > 40:
                return pos_value() + 5 * move_value() - 10 * stable_value()
            elif stage > 30:
                return pos_value() + 5 * move_value() - 10 * stable_value()
            elif stage > 25:
                return pos_value() + 5 * move_value() - 25 * stable_value() - 15 * count_value()
            else:
                return pos_value() + -5 * move_value() - 25 * stable_value() - 25 * count_value()

    # get the new state after this move
    def next_state(self, state, move, color):
        new_state = copy.deepcopy(state)
        new_state[move[0]][move[1]] = color
        turn_over = []
        for dx, dy in direction:
            x = move[0] + dx
            y = move[1] + dy
            flag = False
            while self.within_bound(x, y):
                if new_state[x][y] == -color:
                    turn_over.append((x, y))
                if new_state[x][y] == COLOR_NONE:
                    break
                if new_state[x][y] == color:
                    flag = True
                    break
                x = x + dx
                y = y + dy
            if flag:
                for a, b in turn_over:
                    new_state[a][b] = color
            turn_over.clear()
        return new_state

    # return a list of opponet's chesses in any path from my chess to some valid pos
    def valid_path(self, chessboard, color):
        valid_path = []
        mychesses = np.argwhere(chessboard == color)
        for mychess in mychesses:
            for dx, dy in direction:
                flag = False
                has_none = False
                x = mychess[0] + dx
                y = mychess[1] + dy
                path = []
                if self.within_bound(x, y) and chessboard[x][y] == -color:
                    flag = True
                while flag == True and self.within_bound(x, y):
                    if chessboard[x][y] == color:
                        break
                    elif chessboard[x][y] == COLOR_NONE:
                        has_none = True
                        break
                    if (x, y) not in valid_path:
                        path.append((x, y))
                    x = x + dx
                    y = y + dy
                if has_none:
                    for p in path:
                        valid_path.append(p)
        return valid_path
