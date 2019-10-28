import numpy as np
import math
import copy
from collections import deque


class State:
    """
    Contructeur d'un état initial
    """

    def __init__(self, pos):
        """
        pos donne la position de la voiture i dans sa ligne ou colonne (première case occupée par la voiture);
        """
        self.pos = np.array(pos)

        """
        c,d et prev premettent de retracer l'état précédent et le dernier mouvement effectué
        """
        self.c = self.d = self.prev = None

        self.nb_moves = 0
        self.score = 0

        # Position de la roche
        self.rock = []

    """
    Constructeur d'un état à partir du mouvement (c,d)
    """

    def move(self, c, d):
        s = State(self.pos)
        s.prev = self
        s.pos[c] += d
        s.c = c
        s.d = d
        s.nb_moves = self.nb_moves + 1
        s.rock = self.rock
        return s

    def put_rock(self, rock_pos):
        # Nouvel objet State à retourner
        new_s = State(self.pos)
        new_s.prev = self
        new_s.c = self.c
        new_s.d = self.d

        # Ajouter une nouvelle roche et enlever l'ancienne
        new_s.rock = rock_pos

        return new_s

    def estimee3(self, rh):
        # Nombre de déplacements minimum pour les voitures entre la voiture rouge et la sortie
        nb_car_moves = 0

        red_car_front = self.pos[0] + 2

        for i in range(1, rh.nbcars):
            # Voiture à la verticale et sur une rangée devant la voiture rouge
            if not rh.horiz[i] and rh.move_on[i] >= red_car_front:
                front = self.pos[i]
                rear = front + rh.length[i] - 1
                # L'espace entre l'avant et l'arrière de la voiture contient la rangée 2
                if front == 0 and rear == 2:
                    nb_car_moves += 3
                    nb_car_moves += len(np.where(rh.free_pos[rear + 1:, rh.move_on[i]] is False))
                elif front == 1 and rear == 3:
                    nb_car_moves += 2
                    nb_car_moves += len(np.where(rh.free_pos[rear + 1:, rh.move_on[i]] is False))
                elif front == 1 and rear == 2:
                    nb_car_moves += 1
                elif front == 2:
                    nb_car_moves += 1
                    if rh.length[i] == 3:
                        nb_car_moves += len(np.where(rh.free_pos[4:, rh.move_on[i]] is False))

        # Renvoie la distance entre la voiture rouge et la sortie plus le nombre de déplacements minimal des voitures
        # entre celle-ci et la sortie
        return 4 - self.pos[0] + nb_car_moves

    def score_state(self, rh):
        gain = 10 * self.pos[0]  # 10 fois la proximité de la voiture rouge à la sortie accordée
        perte = self.estimee3(rh)  # Chaque mouvement engendre une perte de 1 point

        # Affecte la valeur de l'état à son paramètre score
        self.score = gain - perte

    def success(self):
        return self.pos[0] == 4

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        if len(self.pos) != len(other.pos):
            print("les états n'ont pas le même nombre de voitures")

        return np.array_equal(self.pos, other.pos)

    def __hash__(self):
        h = 0
        for i in range(len(self.pos)):
            h = 37 * h + self.pos[i]
        return int(h)

    def __lt__(self, other):
        return (self.score) < (other.score)
