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
        new_s.nb_moves = self.nb_moves + 1
        new_s.score = self.score

        # Ajouter une nouvelle roche et enlever l'ancienne
        new_s.rock = rock_pos

        return new_s

    # Retourne une liste des véhicules qui touche l'endroit où pourrait se déplacer la voiture spécifiée
    def blocking_cars(self, rh, blocked_car_id, blocked_car_dir):
        # Vecteur des véhicules perpendiculaires à la voiture analysée
        v_id = [v_id for v_id in range(1, rh.nbcars) if rh.horiz[v_id] != rh.horiz[blocked_car_id]]

        # Avant et arrière de la voiture analysée
        blocked_car_rear = self.pos[blocked_car_id]
        blocked_car_front = self.pos[blocked_car_id] + rh.length[blocked_car_id] - 1

        # Calcul dépendant de la direction prise par la voiture
        if blocked_car_dir == 1:
            # Vecteur des voitures touchant la ligne de déplacement aurant en face qu'en arrière
            v_in_way = [i for i in v_id if (rh.move_on[i] > blocked_car_front) and
                        (self.pos[i] <= rh.move_on[blocked_car_id]) and
                        (self.pos[i] + rh.length[i] - 1 >= rh.move_on[blocked_car_id])]
        else:
            v_in_way = [i for i in v_id if (rh.move_on[i] < blocked_car_rear) and
                        (self.pos[i] <= rh.move_on[blocked_car_id]) and
                        (self.pos[i] + rh.length[i] - 1 >= rh.move_on[blocked_car_id])]

        # Retourne le vecteur des voitures obstruant le véhicule analysé
        return v_in_way

    # Retourne un si le véhicule est bloqué par la roche
    def blocking_rock(self, rh, car_id, car_dir):
        obstruction = 0

        # Avant et arrière de la voiture analysée
        car_rear = self.pos[car_id]
        car_front = self.pos[car_id] + rh.length[car_id] - 1

        # Dépendant de la direction prise par la voiture
        if rh.move_on[car_id] == self.rock[not rh.horiz[car_id]]:
            if car_dir == 1 and self.rock[rh.horiz[car_id]] == car_front + 1:
                obstruction += 1
            elif car_dir == -1 and self.rock[rh.horiz[car_id]] == car_rear - 1:
                obstruction += 1
        return obstruction

    # Heuristique #3 du premier TP
    def min_number_moves(self, rh):
        nb_moves = 0

        # Liste des voitures face au véhicule rouge
        cars_infront_red = self.blocking_cars(rh, 0, 1)

        # Calcule le nombre strictement minimum requis pour libérer la ligne 2
        for i in cars_infront_red:
            if rh.length[i] == 3:
                nb_moves += 3 - self.pos[i]
            else:
                nb_moves += 1

        return 4 - self.pos[0] + nb_moves

    # Compte le nombre d'obstruction et pondère le poids selon la profondeur de l'obstruction
    def obstruction_count(self, rh, depth):
        nb_obstructions = 0

        # Trouve les voitures qui obstrue la voiture rouge
        obstructed = self.blocking_cars(rh, 0, 1)
        # Nombre d'obstructions
        nb_obstructions += 5*len(obstructed)
        not_yet_visited = []

        # Recherche des obstructions des voitures obstruée qui obstruent... pondéré selon la profondeur de l'obstruction
        for i in range(1, depth):
            # On parcourt toutes les voitures obstruant le passage
            for v in obstructed:
                # Voitures de longueurs 3 bloquant les dernières colonnes
                if i == 1 and rh.length[v] == 3:
                    if rh.move_on[v] == 4:
                        nb_obstructions += len(self.blocking_cars(rh, v, 1))
                    # Les voitures de longueur 3 dans la dernière colonne doivent nécessairement descendre
                    if rh.move_on[v] == 5:
                        # Les obstructions de niveau deux ont un impact important et sont pondérées en conséquence
                        nb_obstructions += 2 * len(self.blocking_cars(rh, v, 1))
                        nb_obstructions -= self.pos[v]  # On récompense le joueur max quand on libère la dernière col
                # On énumère les voitures qui bloquent la voiture bloquée
                not_yet_visited += self.blocking_cars(rh, v, -1)
                not_yet_visited += self.blocking_cars(rh, v, 1)
                # Tient compte des roches
                if self.rock:
                    # Trouve le nombre d'obstruction directe d'une voiture par la roche
                    nb_obstructions += (depth - i) * self.blocking_rock(rh, v, -1)
                    nb_obstructions += (depth - i) * self.blocking_rock(rh, v, 1)

            # Les obstruction plus profondes sont moins importantes
            nb_obstructions += (depth - i) * len(not_yet_visited)
            # On retire les redondances pour l'explorations subséquente
            obstructed = set(not_yet_visited)
            not_yet_visited = []

        #  Retourne le nombre d'obstructions
        return nb_obstructions

    def score_state(self, rh):
        # 10 fois la proximité de la voiture rouge à la sortie accordée
        gain = 10 * self.pos[0]
        # Chaque mouvement et obstruction engendre des pertes
        perte = self.min_number_moves(rh) + self.obstruction_count(rh, 4)
        # Pour encourager la résolution en un nombre minimal de coup
        perte += self.nb_moves
        # Pour éviter de retourner dans un état précédent
        if self.c == self.prev.c and self.d == -self.prev.d:
            perte += 100
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
