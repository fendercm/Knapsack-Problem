"""Алгоритмы решения задачи о рюкзаке (0/1).

Предмет — кортеж (название, вес, ценность).
Каждый алгоритм принимает список предметов и вместимость
и возвращает список выбранных предметов.
"""
from itertools import combinations

MAX_BRUTE = 20  # полный перебор дольше не потянет


def dp(items, cap):
    """Динамическое программирование. Точный, O(n * вместимость)."""
    n = len(items)
    t = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, w, v = items[i - 1]
        for c in range(cap + 1):
            t[i][c] = t[i - 1][c]
            if w <= c:
                t[i][c] = max(t[i][c], t[i - 1][c - w] + v)
    chosen, c = [], cap
    for i in range(n, 0, -1):  # восстанавливаем, какие предметы взяты
        if t[i][c] != t[i - 1][c]:
            chosen.append(items[i - 1])
            c -= items[i - 1][1]
    return chosen[::-1]


def brute(items, cap):
    """Полный перебор всех комбинаций. Точный, но медленный."""
    best, best_value = [], 0
    for r in range(len(items) + 1):
        for combo in combinations(items, r):
            if sum(x[1] for x in combo) <= cap:
                value = sum(x[2] for x in combo)
                if value > best_value:
                    best, best_value = list(combo), value
    return best


def bnb(items, cap):
    """Ветви и границы: перебор с отсечением заведомо плохих веток. Точный."""
    order = sorted(items, key=lambda x: x[2] / x[1], reverse=True)
    n = len(order)
    best = {"value": 0, "set": []}

    def bound(i, weight, value):  # оптимистичная оценка (предметы можно делить)
        for j in range(i, n):
            _, w, v = order[j]
            if weight + w <= cap:
                weight, value = weight + w, value + v
            else:
                return value + (cap - weight) * v / w
        return value

    def go(i, weight, value, taken):
        if value > best["value"]:
            best["value"], best["set"] = value, taken[:]
        if i == n or bound(i, weight, value) <= best["value"]:
            return
        _, w, v = order[i]
        if weight + w <= cap:
            go(i + 1, weight + w, value + v, taken + [order[i]])
        go(i + 1, weight, value, taken)

    go(0, 0, 0, [])
    return best["set"]


def greedy(items, cap):
    """Жадный: берём самые «выгодные» (ценность/вес). Быстрый, но НЕ всегда оптимальный."""
    chosen, left = [], cap
    for x in sorted(items, key=lambda x: x[2] / x[1], reverse=True):
        if x[1] <= left:
            chosen.append(x)
            left -= x[1]
    return chosen


# номер в меню -> (название, функция, пояснение)
ALGORITHMS = {
    "1": ("Динамическое программирование", dp, "точный, быстрый"),
    "2": ("Ветви и границы", bnb, "точный, быстрый"),
    "3": ("Полный перебор", brute, f"точный, медленный (до {MAX_BRUTE} предметов)"),
    "4": ("Жадный алгоритм", greedy, "самый быстрый, но может ошибаться"),
}
