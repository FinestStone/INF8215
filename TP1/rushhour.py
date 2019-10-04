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
        for c in range(self.nbcars):
            rear = state.pos[c] - 1  # Square behind the car
            if rear >= 0:
                # Case of a horizontal car
                if self.horiz[c]:
                    # Checking for empty space behind the car
                    if self.free_pos[self.move_on[c], rear]:
                        new_states.append(state.move(c, -1))  # Add the posible state
                # Case of a vertical car
                else:
                    # Checking for empty space behind the car
                    if self.free_pos[rear, self.move_on[c]]:
                        new_states.append(state.move(c, -1))  # Add the posible state

            front = state.pos[c] + self.length[c]  # Square infront of the car
            if front <= 5:
                # Case of a horizontal car
                if self.horiz[c]:
                    # Checking for empty space infront of the car
                    if self.free_pos[self.move_on[c], front]:
                        new_states.append(state.move(c, 1))  # Add the posible state
                # Case of a vertical car
                else:
                    # Checking for empty space infront of the car
                    if self.free_pos[front, self.move_on[c]]:
                        new_states.append(state.move(c, 1))  # Add the posible state
        return new_states

    def solve(self, state):
        # Ensemble hash pour mémoriser les états déjà trouvés
        visited = set()
        # File représentée par une liste (FIFO) initialisée avec l'état initial
        fifo = deque([state])
        visited.add(state)

        # Variable pour compter le nombre d'états visités lors de la résolution
        nb_visited = 0

        # Recherche en largeur sur l'arbre, tant que la liste n'est pas vide
        while fifo:
            # Extrait le premier état
            p = fifo.popleft()
            nb_visited += 1

            # Si l'état est final, on termine l'algorithme
            if p.success():
                # Afficher le nombre d'états visités lors de la résolution
                print("Nombre d'états visités lors de la résolution : %i" % nb_visited)
                return p
            # Sinon, on ajoute ses fils non visités à la fin de la liste
            else:
                s = self.possible_moves(p)
                for child in s:
                    if child not in visited:
                        fifo.append(child)
                        visited.add(child)
        return None

    def solve_Astar(self, state):
        # Ensemble hash pour mémoriser les états déjà trouvés
        visited = set()
        visited.add(state)

        # File de priorité initialisée avec l'état initial
        priority_queue = []
        state.h = state.estimee1()
        heapq.heappush(priority_queue, state)

        # Variable pour compter le nombre d'états visités lors de la résolution
        nb_visited = 0

        # Recherche en largeur sur l'arbre, tant que la liste n'est pas vide
        while priority_queue:
            # Extrait l'état ayant la valeur (fonction d'estimation) la plus prioritaire
            p = heapq.heappop(priority_queue)
            nb_visited += 1

            # Si l'état est final, on termine l'algorithme
            if p.success():
                # Afficher le nombre d'états visités lors de la résolution
                print("Nombre d'états visités lors de la résolution : %i" % nb_visited)
                return p
            # Sinon, on ajoute ses fils non visités à la file
            else:
                s = self.possible_moves(p)
                for child in s:
                    if child not in visited:
                        child.h = child.estimee3(self)
                        heapq.heappush(priority_queue, child)
                        visited.add(child)
        return None

    def print_solution(self, state):
        solution_path = []

        # List all states that lead to the solution
        while state.prev:
            solution_path.append(state)
            state = state.prev

        # Put the list in the right order
        solution_path.reverse()

        # Print all the solution elements in order
        for solution_element in solution_path:
            # Color oNombre d'états visités lors de la résolution : 956f the car that needs to be moves
            color = self.color[solution_element.c]

            # Direction of the moving car
            if self.horiz[solution_element.c]:
                if solution_element.d == 1:
                    direction = "la droite"
                else:
                    direction = "la gauche"
            else:
                if solution_element.d == 1:
                    direction = "le bas"
                else:
                    direction = "le haut"

            print("%s. Voiture %s vers %s" % (solution_path.index(solution_element) + 1, color, direction))

        return 0
