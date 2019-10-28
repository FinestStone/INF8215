from rushhour import *


class MiniMaxSearch:
    def __init__(self, rushHour, initial_state, search_depth):
        self.rushhour = rushHour
        self.state = initial_state
        self.search_depth = search_depth

    def minimax_1(self, current_depth, current_state):
        # Contient la logique de l'algorithme minimax pour un seul joueur
        if current_depth == 0 or current_state.success():
            current_state.score_state(self.rushhour)
            return current_state.score, (None, None)

        max_value = float('-inf')
        best_move = (None, None)

        for s in self.rushhour.possible_moves(current_state):
            eval_child, move_child = self.minimax_1(current_depth-1, s)

            if eval_child > max_value:
                max_value = eval_child
                best_move = (s.c, s.d)

        # Retourne le meilleur coup à prendre à partir de l'état courant
        return max_value, best_move

    def minimax_2(self, current_depth, current_state, is_max):
        best_move = None

        # TODO
        return best_move

    def minimax_pruning(self, current_depth, current_state, is_max, alpha, beta):
        best_move = None

        # TODO
        return best_move

    def expectimax(self, current_depth, current_state, is_max):
        best_move = None

        # TODO
        return best_move

    def decide_best_move_1(self):
        # Trouve et exécute le meilleur coup pour une partie à un joueur
        _, best_move = self.minimax_1(self.search_depth, self.state)
        self.state = self.state.move(best_move[0], best_move[1])

    def decide_best_move_2(self, is_max):
        # TODO
        pass

    def decide_best_move_pruning(self, is_max):
        # TODO
        pass

    def decide_best_move_expectimax(self, is_max):
        # TODO
        pass

    def solve(self, state, is_singleplayer):
        # Résout un problème de Rush Hour avec le nombre minimal de coups
        if is_singleplayer:
            while not state.success():
                self.decide_best_move_1()
                self.solve(self.state, True)

    def print_move(self, is_max, state):
        # État sous le contrôle de l’agent
        if is_max:
            color = self.rushhour.color[state.c]
            if self.rushhour.horiz[state.c]:
                if state.d == 1:
                    direction = "la droite"
                else:
                    direction = "la gauche"
            else:
                if state.d == 1:
                    direction = "le bas"
                else:
                    direction = "le haut"

            # Imprime le coup fait
            print("Voiture %s vers %s" % (color, direction))

        # État sous le contrôle de l’adversaire
        else:
            if state.rock:
                # Imprime le coup fait
                print("Roche dans la case %i-%i" % (state.rock[0], state.rock[1]))
