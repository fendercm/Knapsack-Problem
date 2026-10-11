"""Задача о рюкзаке. Запуск: python main.py"""
import time

from algorithms import ALGORITHMS, MAX_BRUTE, brute
from interface import (ask, ask_int, input_items, random_items, show_comparison_header,
                       show_comparison_row, show_items, show_menu, show_result)


def solve(items, cap):
    print("\nВыберите алгоритм:")
    for key, (name, _, note) in ALGORITHMS.items():
        print(f"  {key}. {name} — {note}")
    print("  5. Сравнить все")
    choice = ask_int("Ваш выбор: ", 1, 5)

    if choice == 5:
        show_comparison_header()
        for name, func, _ in ALGORITHMS.values():
            if func is brute and len(items) > MAX_BRUTE:
                print(f"  {name:<30}  пропущен: слишком много предметов")
                continue
            start = time.perf_counter()
            result = func(items, cap)
            show_comparison_row(name, result, (time.perf_counter() - start) * 1000)
        return

    name, func, _ = ALGORITHMS[str(choice)]
    if func is brute and len(items) > MAX_BRUTE:
        print(f"\n  ! Полный перебор работает максимум с {MAX_BRUTE} предметами.")
        return
    start = time.perf_counter()
    result = func(items, cap)
    show_result(name, result, cap, time.perf_counter() - start)


def main():
    items, cap = [], None
    while True:
        show_menu(items, cap)
        choice = ask_int("Ваш выбор: ", 0, 5)

        if choice == 0:
            print("До свидания!")
            return
        if choice == 1:
            items = input_items()
            show_items(items)
        elif choice == 2:
            items = random_items()
            show_items(items)
        elif choice == 3:
            show_items(items)
        elif choice == 4:
            cap = ask_int("Вместимость рюкзака: ", 0)
        elif choice == 5:
            if not items:
                print("\n  ! Сначала добавьте предметы (пункт 1 или 2).")
                continue
            if cap is None:
                cap = ask_int("\nВместимость рюкзака не задана. Введите её: ", 0)
            solve(items, cap)
        ask("\nEnter — вернуться в меню...")


if __name__ == "__main__":
    main()
