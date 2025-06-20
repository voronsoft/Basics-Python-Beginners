# 9_5_1 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_5_1(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Разбор кода в дерево AST
        tree = ast.parse(code)

        zip_used = False
        map_used = False
        next_used = False

        # Проход по дереву AST
        for node in ast.walk(tree):
            # Проверка на вызовы функций (zip, next, map)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == 'zip':
                    zip_used = True
                elif node.func.id == 'map':
                    map_used = True
                elif node.func.id == 'next':
                    next_used = True

        # Сообщения, если чего-то не хватает
        if not zip_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции zip.")
        if not map_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции map.")
        if not next_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции next.")

        result.append("Найден вызов функции zip()")
        result.append("Найден вызов функции map()")
        result.append("Найден вызов функции next()")
        result.append("--------------OK structure -------------\n")

        # Выполнение функционального теста
        try:
            res = test_9_5_1_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_5_1_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "-7 8 11 -1 3\n1 2 3 4 5 6 7 8 9 10",
        "1 -2 -3 4\n5 6 7 8 9 0 10",
    )

    # Ожидаемые данные вывода
    expected_output = (
        "-7 16 33",
        "5 -12 -21",
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=test_input[i], capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем перехваченный вывод из stdout
            captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            if captured_output == expected_output[i]:
                test_result.append(f"Получено: {captured_output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
