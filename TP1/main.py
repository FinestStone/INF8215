from rushhour import *


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


def solve46():
    rh = Rushhour([True, False, True, False, False, True, False, True, False, True, False, True],
                 [2, 2, 3, 2, 3, 2, 2, 2, 2, 2, 2, 3],
                 [2, 2, 0, 0, 3, 1, 1, 3, 0, 4, 5, 5],
                 ["rouge", "vert clair", "jaune", "orange", "violet clair", "bleu ciel", "rose", "violet", "vert", "noir", "beige", "bleu"])
    s = State([1, 0, 3, 1, 1, 4, 3, 4, 4, 2, 4, 1])
    # s = rh.solve(s)
    s = rh.solve_Astar(s)
    rh.print_solution(s)


def solve16():
    rh = Rushhour([True, True, False, False, True, True, False, False],
                  [2, 2, 3, 2, 3, 2, 3, 3],
                  [2, 0, 0, 0, 5, 4, 5, 3],
                  ["rouge", "vert clair", "violet", "orange", "vert", "bleu ciel", "jaune", "bleu"])
    s = State([1, 0, 1, 4, 2, 4, 0, 1])
    # s = rh.solve(s)
    s = rh.solve_Astar(s)
    n = rh.print_solution(s)


def solve81():
    rh = Rushhour([True, False, True, False, False, False, False, True, False, False, True, True, True],
                  [2, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2],
                  [2, 0, 0, 4, 1, 2, 5, 3, 3, 2, 4, 5, 5],
                  ["rouge", "jaune", "vert clair", "orange", "bleu clair", "rose", "violet clair", "bleu", "violet",
                   "vert", "noir", "beige", "jaune clair"])
    s = State([3, 0, 1, 0, 1, 1, 1, 0, 3, 4, 4, 0, 3])
    # s = rh.solve(s)
    s = rh.solve_Astar(s)
    n = rh.print_solution(s)


if __name__ == '__main__':
    # test1()
    # test2()
    # test3()
    solve46()
    print("\n--------------------------------------------\n")
    # %time
    solve16()
    print("\n--------------------------------------------\n")
    solve81()
    print("\n--------------------------------------------\n")
    # % time
