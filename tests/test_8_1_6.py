# 8_1_6 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_8_1_6(path_tmp_file: str, task_num_test: str):
    """Тест структуры: импорт seed и random (как rnd) из random, и вызов seed(10), print(round(rnd(), 2))"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение и разбор кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Парсим код в дерево
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
        # Импортируем модуль пользователя
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data=" ", capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Получаем перехваченный вывод из stdout
        captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

        # Проверяем результат
        test_result = list()
        test_result.append(f"---------------OK Тест --------------")
        test_result.append(f"Ожидалось: {expected_output}")
        test_result.append(f"Получено: {captured_output}")

        # Готовим отчёт
        test_result = [
            f"---------------OK Тест --------------",
            f"Ожидалось: {expected_output}",
            f"Получено: {captured_output}",
        ]

        if captured_output == expected_output:
            result.append("\n".join(test_result))
        else:
            raise ValueError(
                f"------------- FAIL Тест --------\n" f"Ожидалось: {expected_output}\nно получено: {captured_output}\n"
            )

        return "\n".join(result)

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
