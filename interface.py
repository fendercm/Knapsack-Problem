"""Ввод и вывод: всё, что общается с пользователем."""
import random
import sys


# ----------------------------- ввод -----------------------------
def ask(text):
    try:
        return input(text).strip()
    except EOFError:
        print("\nДо свидания!")
        sys.exit(0)


def ask_int(text, minimum=0, maximum=None):
    while True:
        try:
            n = int(ask(text))
            if n >= minimum and (maximum is None or n <= maximum):
                return n
        except ValueError:
            pass
        limit = f", максимум {maximum}" if maximum is not None else ""
        print(f"  ! Введите целое число (минимум {minimum}{limit}).")


def input_items():
    print("\nВводите предметы по одному: название вес ценность")
    print("Пример: Палатка 12 40")
    print("Пустая строка — закончить.\n")
    items = []
    while True:
        line = ask(f"  Предмет {len(items) + 1}: ")
        if not line:
            if items:
                return items
            print("  ! Нужен хотя бы один предмет.")
            continue
        parts = line.split()
        try:
            weight, value = int(parts[-2]), int(parts[-1])
            if len(parts) < 3 or weight <= 0 or value < 0:
                raise ValueError
            items.append((" ".join(parts[:-2]), weight, value))
        except (ValueError, IndexError):
            print("  ! Неверный формат. Нужно: название вес ценность (вес > 0, числа целые).")


def random_items():
    n = ask_int("Сколько предметов создать (1-1000)? ", 1, 1000)
    return [(f"Предмет {i + 1}", random.randint(1, 30), random.randint(1, 100)) for i in range(n)]


# ----------------------------- вывод -----------------------------
def show_menu(items, cap):
    print("\n╔════════════════════════════╗")
    print("║     ЗАДАЧА О РЮКЗАКЕ       ║")
    print("╚════════════════════════════╝")
    print("  1. Ввести предметы вручную")
    print("  2. Создать случайные предметы")
    print("  3. Показать предметы")
    print("  4. Задать вместимость рюкзака")
    print("  5. Решить")
    print("  0. Выход")
    print(f"  [предметов: {len(items)}, вместимость: {cap if cap is not None else 'не задана'}]")


def show_items(items):
    if not items:
        print("\n  Список предметов пуст.")
        return
    width = max(8, *(len(x[0]) for x in items[:30]))
    print(f"\n  {'№':>3}  {'Название':<{width}}  {'Вес':>5}  {'Ценность':>8}")
    print("  " + "─" * (width + 22))
    for i, (name, w, v) in enumerate(items[:30], 1):
        print(f"  {i:>3}  {name:<{width}}  {w:>5}  {v:>8}")
    if len(items) > 30:
        print(f"  ... и ещё {len(items) - 30}")
    print(f"\n  Всего: {len(items)} предметов, общий вес {sum(x[1] for x in items)}")


def show_result(title, chosen, cap, seconds):
    weight = sum(x[1] for x in chosen)
    value = sum(x[2] for x in chosen)
    print(f"\n── {title} ({seconds * 1000:.2f} мс) ──")
    if chosen:
        width = max(8, *(len(x[0]) for x in chosen[:30]))
        print(f"  {'Название':<{width}}  {'Вес':>5}  {'Ценность':>8}")
        for name, w, v in chosen[:30]:
            print(f"  {name:<{width}}  {w:>5}  {v:>8}")
        if len(chosen) > 30:
            print(f"  ... и ещё {len(chosen) - 30}")
    else:
        print("  Ни один предмет не помещается.")
    bar = int(20 * weight / cap) if cap else 0
    print(f"\n  Рюкзак: [{'█' * bar}{'░' * (20 - bar)}] {weight} из {cap}")
    print(f"  Общая ценность: {value}")


def show_comparison_header():
    print(f"\n  {'Алгоритм':<30}{'Ценность':>10}{'Вес':>6}{'Время, мс':>12}")
    print("  " + "─" * 58)


def show_comparison_row(name, chosen, ms):
    print(f"  {name:<30}{sum(x[2] for x in chosen):>10}{sum(x[1] for x in chosen):>6}{ms:>12.2f}")
