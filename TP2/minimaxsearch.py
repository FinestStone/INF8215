from rushhour import *
import random


class MiniMaxSearch:

    def __init__(self, rushHour, initial_state, search_depth):
        self.rushhour = rushHour
        self.state = initial_state
        self.search_depth = search_depth
        self.visited_states = 0

    def minimax_1(self, current_depth, current_state):
        best_move = (None, None)
        self.visited_states += 1

        # Contient la logique de l'algorithme minimax pour un seul joueur
        if current_depth == 0 or current_state.success():
            current_state.score_state(self.rushhour)
            return current_state.score, (None, None)

        max_value = float('-inf')

        for s in self.rushhour.possible_moves(current_state):
            eval_child, move_child = self.minimax_1(current_depth-1, s)

            if eval_child > max_value:
                max_value = eval_child
                best_move = (s.c, s.d)

        # Retourne le meilleur coup à prendre à partir de l'état courant
        return max_value, best_move

    def minimax_2(self, current_depth, current_state, is_max):
        best_move = (None, None)
        self.visited_states += 1

        # Contient la logique de l'algorithme minimax pour deux joueurs
        if current_depth == 0 or current_state.success():
            current_state.score_state(self.rushhour)
            return current_state.score, (None, None)

        if is_max:
            max_value = float('-inf')
            for s in self.rushhour.possible_moves(current_state):
                eval_child, move_child = self.minimax_2(current_depth - 1, s, False)
                if eval_child > max_value:
                    max_value = eval_child
                    best_move = (s.c, s.d)
            # Retourne le meilleur coup à prendre à partir de l'état courant
            return max_value, best_move

        else:
            min_value = float('inf')
            for s in self.rushhour.possible_rock_moves(current_state):
                eval_child, move_child = self.minimax_2(current_depth - 1, s, True)
                if eval_child < min_value:
                    min_value = eval_child
                    best_move = (s.rock[0], s.rock[1])
            # Retourne le meilleur coup à prendre à partir de l'état courant
            return min_value, best_move

    def minimax_pruning(self, current_depth, current_state, is_max, alpha, beta):
        best_move = (None, None)
        self.visited_states += 1

        # Contient la logique de l'algorithme minimax pour deux joueurs
        if current_depth == 0 or current_state.success():
            current_state.score_state(self.rushhour)
            return current_state.score, (None, None)

        if is_max:
            max_value = float('-inf')
            for s in self.rushhour.possible_moves(current_state):
                eval_child, move_child = self.minimax_pruning(current_depth - 1, s, False, alpha, beta)
                if eval_child > max_value:
                    max_value = eval_child
                    best_move = (s.c, s.d)
                alpha = max(alpha, eval_child)
                if beta <= alpha:
                    break
            # Retourne le meilleur coup à prendre à partir de l'état courant
            return max_value, best_move

        else:
            min_value = float('inf')
            for s in self.rushhour.possible_rock_moves(current_state):
                eval_child, move_child = self.minimax_pruning(current_depth - 1, s, True, alpha, beta)
                if eval_child < min_value:
                    min_value = eval_child
                    best_move = (s.rock[0], s.rock[1])
                beta = min(beta, eval_child)
                if beta <= alpha:
                    break
            # Retourne le meilleur coup à prendre à partir de l'état courant
            return min_value, best_move

    def value_with_probability(self, i, children, vision):
        if vision == "expectimax_aleatoire":
            return random.random() * 1/len(children)
        elif vision == "expectimax_pessimistic":
            pass
        elif vision == "expectimax_optimistic":
            pass

    def expectimax(self, current_depth, current_state, is_max, vision):
        best_move = (None, None)
        self.visited_states += 1

        # Contient la logique de l'algorithme minimax pour deux joueurs
        if current_depth == 0 or current_state.success():
            current_state.score_state(self.rushhour)
            return current_state.score, (None, None)

        if is_max:
            max_value = float('-inf')
            for s in self.rushhour.possible_moves(current_state):
                eval_child, move_child = self.expectimax(current_depth - 1, s, False, vision)
                if eval_child > max_value:
                    max_value = eval_child
                    best_move = (s.c, s.d)
                # Retourne le meilleur coup à prendre à partir de l'état courant
            return max_value, best_move

        else:
            children = []
            for s in self.rushhour.possible_rock_moves(current_state):
                eval_child, move_child = self.expectimax(current_depth - 1, s, True, vision)
                children.append(eval_child)
            i_state = 0
            min_value = float('inf')
            children_return = 0
            for s in self.rushhour.possible_rock_moves(current_state):
                v = self.value_with_probability(i_state, children, vision)
                if v < min_value:
                    children_return = children[i_state]
                    min_value = v
                    best_move = (s.rock[0], s.rock[1])
                i_state += 1
            return children_return, best_move

            # children = []
            # min_value = float('inf')
            # for s in self.rushhour.possible_rock_moves(current_state):
            #     eval_child, move_child = self.expectimax(current_depth - 1, s, True, vision)
            #     children.append(eval_child)
            #     if eval_child < min_value:
            #         min_value = eval_child
            #         best_move = (s.rock[0], s.rock[1])
            # v = 0
            # for i_state in children:
            #     v += self.probability(i_state, children) * children[i_state]
            #     i_state += 1
            # return v, best_move

    def decide_best_move_1(self):
        # Trouve et exécute le meilleur coup pour une partie à un joueur
        _, best_move = self.minimax_1(self.search_depth, self.state)
        self.state = self.state.move(best_move[0], best_move[1])

    def decide_best_move_2(self, is_max):
        # Trouve et exécute le meilleur coup pour une partie à deux joueurs
        _, best_move = self.minimax_2(self.search_depth, self.state, is_max)
        if is_max:
            self.state = self.state.move(best_move[0], best_move[1])
        else:
            self.state = self.state.put_rock((best_move[0], best_move[1]))

    def decide_best_move_pruning(self, is_max):
        _, best_move = self.minimax_pruning(self.search_depth, self.state, is_max, float('-inf'), float('inf'))
        if is_max:
            self.state = self.state.move(best_move[0], best_move[1])
        else:
            self.state = self.state.put_rock((best_move[0], best_move[1]))

    def decide_best_move_expectimax(self, is_max, vision):
        _, best_move = self.expectimax(self.search_depth, self.state, is_max, vision)
        if is_max:
            self.state = self.state.move(best_move[0], best_move[1])
        else:
            self.state = self.state.put_rock((best_move[0], best_move[1]))

    def solve(self, is_singleplayer, second_player):
        #second_player peut prendre cinq valeurs: 'pessimistic', 'pruning', 'expectimax_aleatoire', 'expectimax_pessimistic', 'expectimax_optimistic'
        # Résout un problème de Rush Hour avec le nombre minimal de coups
        if is_singleplayer:
            while not self.state.success():
                self.decide_best_move_1()
                self.print_move(True, self.state)
                self.solve(True, False)

        elif not is_singleplayer:
            turn = not self.state.nb_moves % 2  # Tours pairs: joueur max
            while not self.state.success():
                if second_player == 'pessimistic':
                    self.decide_best_move_2(turn)
                    self.print_move(turn, self.state)
                    self.solve(False, 'pessimistic')
                elif second_player == 'pruning':
                    self.decide_best_move_pruning(turn)
                    self.print_move(turn, self.state)
                    self.solve(False, 'pruning')
                elif second_player == 'expectimax_aleatoire':
                    self.decide_best_move_expectimax(turn, second_player)
                    self.print_move(turn, self.state)
                    self.solve(False, 'expectimax_aleatoire')
                elif second_player == 'expectimax_optimistic':
                    self.decide_best_move_expectimax(turn, second_player)
                    self.print_move(turn, self.state)
                    self.solve(False, 'expectimax_optimistic')
                elif second_player == 'expectimax_pessimistic':
                    self.decide_best_move_expectimax(turn, second_player)
                    self.print_move(turn, self.state)
                    self.solve(False, 'expectimax_pessimistic')

            return self.visited_states

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
            print("%i. Voiture %s vers %s" % (self.state.nb_moves, color, direction))

        # État sous le contrôle de l’adversaire
        else:
            if state.rock:
                # Imprime le coup fait
                print("%i. Roche dans la case %i-%i" % (self.state.nb_moves, state.rock[0], state.rock[1]))
