from state import *
from collections import deque
import heapq


class Rushhour:

    def __init__(self, horiz, length, move_on, color=None):
        self.nbcars = len(horiz)
        self.horiz = horiz
        self.length = length
        self.move_on = move_on
        self.color = color

        self.free_pos = None

    def init_positions(self, state):
        self.free_pos = np.ones((6, 6), dtype=bool)

        # Initialise la matrice en fonction de l'état donné
        for i in range(self.nbcars):
            if self.horiz[i]:  # Cas où la voiture est à l'horizontale
                self.free_pos[self.move_on[i], state.pos[i]:state.pos[i] + self.length[i]] = False
            else:  # Cas où la voiture est à la verticale
                self.free_pos[state.pos[i]:state.pos[i] + self.length[i], self.move_on[i]] = False

    def possible_moves(self, state):
        self.init_positions(state)
        new_states = []

        # Recherche des véhicules qui peuvent se déplacer
        for i in range(self.nbcars):
            new_state = state

            # Cas où la voiture est à l'horizontale
            if self.horiz[i]:
                if state.pos[i] + self.length[i] <= 5 and \
                        self.free_pos[self.move_on[i], state.pos[i] + self.length[i]]:  # Case libre en face
                    new_state.move(i, 1)
                    new_states.append(new_state)
                if state.pos[i] - 1 >= 0 and self.free_pos[self.move_on[i], state.pos[i] - 1]:  # Case libre derrière
                    new_state.move(i, -1)
                    new_states.append(new_state)

            # Cas où la voiture est à la verticale
            else:
                if state.pos[i] + self.length[i] <= 5 and \
                        self.free_pos[state.pos[i] + self.length[i], self.move_on[i]]:  # Case libre en face
                    new_state.move(i, 1)
                    new_states.append(new_state)
                if state.pos[i] - 1 >= 0 and self.free_pos[state.pos[i] - 1, self.move_on[i]]:  # Case libre derrière
                    new_state.move(i, -1)
                    new_states.append(new_state)

        # Renvoie l'ensemble d'états qui peuvent être atteints à partir de l'état state
        return new_states

    def solve(self, state):
        visited = set()
        fifo = deque([state])
        visited.add(state)
        # TODO

        return None

    def solve_Astar(self, state):
        visited = set()
        visited.add(state)

        priority_queue = []
        state.h = state.estimee1()
        heapq.heappush(priority_queue, state)

        # TODO
        return None

    def print_solution(self, state):
        # TODO
        return 0


def test2():
    rh = Rushhour([True, True, False, False, True, True, False, False],
                  [2, 2, 3, 2, 3, 2, 3, 3],
                  [2, 0, 0, 0, 5, 4, 5, 3])
    s = State([1, 0, 1, 4, 2, 4, 0, 1])
    rh.init_positions(s)
    b = True
    print(rh.free_pos)
    ans = [[False, False, True, True, True, False], [False, True, True, False, True, False],
           [False, False, False, False, True, False],
           [False, True, True, False, True, True], [False, True, True, True, False, False],
           [False, True, False, False, False, True]]
    b = b and (rh.free_pos[i, j] == ans[i, j] for i in range(6) for j in range(6))
    # print("\n", "résultat correct" if b else "mauvais résultat")


def test3():
    rh = Rushhour([True, False, True, False, False, True, False, True, False, True, False, True],
                 [2, 2, 3, 2, 3, 2, 2, 2, 2, 2, 2, 3],
                 [2, 2, 0, 0, 3, 1, 1, 3, 0, 4, 5, 5])
    s = State([1, 0, 3, 1, 1, 4, 3, 4, 4, 2, 4, 1])
    s2 = State([1, 0, 3, 1, 1, 4, 3, 4, 4, 2, 4, 2])
    print(len(rh.possible_moves(s)))
    print(len(rh.possible_moves(s2)))


test2()
test3()
