"""Проверка алгоритмов. Запуск: python test_algorithms.py"""
import random

from algorithms import bnb, brute, dp, greedy


def value(chosen):
    return sum(x[2] for x in chosen)


def weight(chosen):
    return sum(x[1] for x in chosen)


# классический пример: ответ 220 (предметы b и c)
classic = [("a", 10, 60), ("b", 20, 100), ("c", 30, 120)]
assert value(dp(classic, 50)) == 220

# жадный может ошибиться, точные — нет
trap = [("x", 1, 2), ("y", 10, 19)]
assert value(greedy(trap, 10)) == 2
assert value(dp(trap, 10)) == 19

# крайние случаи
assert dp([], 10) == []
assert dp(classic, 0) == []

# точные алгоритмы дают одинаковый ответ и не превышают вместимость
for seed in range(200):
    r = random.Random(seed)
    items = [(f"i{k}", r.randint(1, 15), r.randint(0, 50)) for k in range(r.randint(1, 10))]
    cap = r.randint(0, 50)
    expected = value(brute(items, cap))
    for func in (dp, bnb):
        result = func(items, cap)
        assert value(result) == expected, (func.__name__, seed)
        assert weight(result) <= cap

print("Все проверки пройдены ✔")
