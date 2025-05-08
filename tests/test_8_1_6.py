# 8_1_6 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_8_1_6(path_tmp_file: str, task_num_test: str):
    """Тест структуры: импорт seed и random (как rnd) из random, и вызов seed(10), print(round(rnd(), 2))"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code)

        def has_correct_import(tree_in):
            """Проверяет, что импортированы seed и random as rnd из random"""
            has_seed = False
            has_random_as_rnd = False
            for node in ast.walk(tree_in):
                if isinstance(node, ast.ImportFrom) and node.module == "random":
                    for alias in node.names:
                        if alias.name == "seed" and alias.asname is None:
                            has_seed = True
                        if alias.name == "random" and alias.asname == "rnd":
                            has_random_as_rnd = True
            return has_seed and has_random_as_rnd

        def calls_seed_and_rnd(tree_in):
            """Проверяет, что есть вызов seed(10) и print(round(rnd(), 2))"""
            seed_call_found = False
            print_round_rnd_found = False

            for node in ast.walk(tree_in):
                if isinstance(node, ast.Call):
                    # Проверка seed(10)
                    if isinstance(node.func, ast.Name) and node.func.id == "seed":
                        if len(node.args) == 1 and isinstance(node.args[0], ast.Constant) and node.args[0].value == 10:
                            seed_call_found = True

                    # Проверка print(round(rnd(), 2))
                    if isinstance(node.func, ast.Name) and node.func.id == "print":
                        if len(node.args) == 1:
                            arg = node.args[0]
                            if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id == "round":
                                # Проверяем аргументы round(...)
                                if (
                                    len(arg.args) == 2
                                    and isinstance(arg.args[0], ast.Call)
                                    and isinstance(arg.args[0].func, ast.Name)
                                    and arg.args[0].func.id == "rnd"
                                    and isinstance(arg.args[1], ast.Constant)
                                    and arg.args[1].value == 2
                                ):
                                    print_round_rnd_found = True

            return seed_call_found and print_round_rnd_found

        # Проверка импорта и вызовов
        if not has_correct_import(tree):
            raise ValueError("ОШИБКА: Ожидается импорт: from random import seed, random as rnd")
        if not calls_seed_and_rnd(tree):
            raise ValueError("ОШИБКА: Не найдены вызовы seed(10) и print(round(rnd(), 2))")

        result.append("Импорт: from random import seed, random as rnd — OK")
        result.append("Вызов seed(10) и print(round(rnd(), 2)) — OK")
        result.append("--------------OK structure -------------\n")

        # Запуск теста выполнения кода
        try:
            res = test_8_1_6_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        print(error_info)
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_8_1_6_1(path_tmp_file: str):
    """Функция тестирования: проверяет выполнение seed(10) и print(round(rnd(), 2))"""

    # Ожидаемый результат при seed(10) и round(rnd(), 2)
    expected_output = "0.57"

    result = []

    try:
        i = 0  # Номер теста

        # Импортируем модуль из файла
        spec = importlib.util.spec_from_file_location("module.name", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Сохраняем оригинальные потоки
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        # Подменяем ввод и вывод
        sys.stdin = StringIO("")
        output_buffer = StringIO()
        sys.stdout = output_buffer

        # Выполняем код пользователя
        spec.loader.exec_module(user_module)

        # Считываем перехваченный вывод
        captured_output = output_buffer.getvalue().strip()

        # Восстанавливаем потоки
        sys.stdout = original_stdout
        sys.stdin = original_stdin

        # Готовим отчёт
        test_result = [
            f"---------------OK Тест: {i + 1} --------------",
            f"Ожидалось: {expected_output}",
            f"Получено: {captured_output}",
        ]

        if captured_output == expected_output:
            result.append("\n".join(test_result))
        else:
            raise ValueError(
                f"------------- FAIL Тест: {i + 1} --------\n"
                f"Ожидалось: {expected_output}\nно получено: {captured_output}\n"
            )

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
