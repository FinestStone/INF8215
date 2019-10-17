from state import *


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
        for i in range(self.nbcars):
            if self.horiz[i]:
                self.free_pos[self.move_on[i], state.pos[i]:state.pos[i] + self.length[i]] = False
            else:
                self.free_pos[state.pos[i]:state.pos[i] + self.length[i], self.move_on[i]] = False
        # Emplacement de la roche
        self.free_pos[state.rock] = False

    def possible_moves(self, state):
        self.init_positions(state)
        new_states = []
        for i in range(self.nbcars):
            if self.horiz[i]:
                if state.pos[i] + self.length[i] - 1 < 5 and \
                        self.free_pos[self.move_on[i], state.pos[i] + self.length[i]]:
                    new_states.append(state.move(i, +1))
                if state.pos[i] > 0 and self.free_pos[self.move_on[i], state.pos[i] - 1]:
                    new_states.append(state.move(i, -1))
            else:
                if state.pos[i] + self.length[i] - 1 < 5 and \
                        self.free_pos[state.pos[i] + self.length[i], self.move_on[i]]:
                    new_states.append(state.move(i, +1))
                if state.pos[i] > 0 and self.free_pos[state.pos[i] - 1, self.move_on[i]]:
                    new_states.append(state.move(i, -1))
        return new_states

    def possible_rock_moves(self, state):
        self.init_positions(state)
        new_states = []  # Tous les coups possibles de l'adversaire (avec la roche) à partir de l'état courant

        rock_current_row = rock_current_column = None

        if state.rock:
            (rock_current_row, rock_current_column) = state.rock

        # Ne peut mettre deux roches consécutives sur la même ligne ou sur la ligne 2
        for row in set(range(6)) - {2, rock_current_row}:
            # Ne peut mettre deux roches consécutives sur la même colonne
            for column in set(range(6)) - {rock_current_column}:
                if self.free_pos[row, column]:
                    new_states.append(state.put_rock((row, column)))

        return new_states

    def print_pretty_grid(self, state):
        self.init_positions(state)
        grid = np.chararray((6, 6))
        grid[:] = '-'
        for car in range(self.nbcars):
            for pos in range(state.pos[car], state.pos[car] + self.length[car]):
                if self.horiz[car]:
                    grid[self.move_on[car]][pos] = self.color[car][0]
                else:
                    grid[pos][self.move_on[car]] = self.color[car][0]
        grid[state.rock] = 'x'
        print(grid)
