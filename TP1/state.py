import numpy as np
import math
import copy


class State:
    """
    Contructeur d'un état initial
    """

    def __init__(self, pos):
        """
        pos donne la position de la voiture i (première case occupée par la voiture);
        """
        self.pos = np.array(pos)

        """
        c, d et prev premettent de retracer l'état précédent et le dernier mouvement effectué
        """
        self.c = self.d = self.prev = None

        self.nb_moves = 0
        self.h = 0

    """
    Constructeur d'un état à partir mouvement (c,d)
    """

    def move(self, c, d):
        # Création d'un nouvel objet State
        s = State(self.pos)

        # Déplacement de la voiture c de 1 case dans la direction d
        s.pos[c] += d

        # Définition des variables prev, c et d.
        s.prev = self
        s.c = c
        s.d = d
        return s

    """ est il final? """

    def success(self):
        # Vérifie si l'avant de la voiture rouge est sur la case 2-5
        return self.pos[0] == 4

    """
    Estimation du nombre de coup restants 
    """

    def estimee1(self):
        # TODO
        return 0

    def estimee2(self, rh):
        # TODO
        return 0

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
        return (self.nb_moves + self.h) < (other.nb_moves + other.h)


def test1():
    positioning = [1, 0, 1, 4, 2, 4, 0, 1]
    s0 = State(positioning)
    b = not s0.success()
    print(b)
    s = s0.move(1, 1)
    print(s.prev == s0)
    b = b and s.prev == s0
    print(s0.pos[1], " ", s.pos[1])
    s = s.move(6, 1)
    s = s.move(1, -1)
    s = s.move(6, -1)
    print(s == s0)
    b = b and s == s0
    s = s.move(1, 1)
    s = s.move(2, -1)
    s = s.move(3, -1)
    s = s.move(4, 1)
    s = s.move(4, -1)
    s = s.move(5, -1)
    s = s.move(5, 1)
    s = s.move(5, -1)
    s = s.move(6, 1)
    s = s.move(6, 1)
    s = s.move(6, 1)
    s = s.move(7, 1)
    s = s.move(7, 1)
    s = s.move(0, 1)
    s = s.move(0, 1)
    s = s.move(0, 1)
    print(s.success())
    b = b and s.success()
    print("\n", "résultat correct" if b else "mauvais résultat")
