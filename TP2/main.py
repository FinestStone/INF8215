from rushhour import *


def testRocks():
    rh = Rushhour([True, False, True, False, False, True, False, True, False, True, False, True],
                  [2, 2, 3, 2, 3, 2, 2, 2, 2, 2, 2, 3],
                  [2, 2, 0, 0, 3, 1, 1, 3, 0, 4, 5, 5],
                  ["rouge", "vert clair", "jaune", "orange", "violet clair", "bleu ciel", "rose", "violet", "vert",
                   "noir", "beige", "bleu"])
    s0 = State([1, 0, 3, 1, 1, 4, 3, 4, 4, 2, 4, 1])

    s1 = s0.put_rock((4, 4))
    s2 = s1.put_rock((3, 2))

    print("État initial")
    rh.print_pretty_grid(s0)
    print(rh.free_pos)
    print('\n')

    print("Roche 4-4")
    rh.print_pretty_grid(s1)
    print(rh.free_pos)
    print('\n')

    print("Roche 3-2")
    rh.print_pretty_grid(s2)
    print(rh.free_pos)
    print('\n')


def testPossibleRockMoves():
    rh = Rushhour([True, False, True, False, False, True, False, True, False, True, False, True],
                 [2, 2, 3, 2, 3, 2, 2, 2, 2, 2, 2, 3],
                 [2, 2, 0, 0, 3, 1, 1, 3, 0, 4, 5, 5],
                 ["rouge", "vert clair", "jaune", "orange", "violet clair", "bleu ciel", "rose", "violet", "vert", "noir", "beige", "bleu"])
    s = State([1, 0, 3, 1, 1, 4, 3, 4, 4, 2, 4, 1])
    sols = rh.possible_rock_moves(s)
    print(len(sols))
    s1 = s.put_rock((3,4))
    sols = rh.possible_rock_moves(s1)
    print(len(sols))


if __name__ == '__main__':
    testRocks()
    testPossibleRockMoves()
