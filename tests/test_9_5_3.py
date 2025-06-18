# 9_5_3 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_5_3(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code, allowed_imports=["sys"], allowed_calls=["sys.stdin.readlines"])

        # Разбор кода в дерево AST
        tree = ast.parse(code)

        zip_used = False

        # Проход по дереву AST
        for node in ast.walk(tree):
            # Проверка на вызовы функций (zip(...))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == 'zip':
                    zip_used = True

        # Сообщения, если чего-то не хватает
        if not zip_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции zip.")

        result.append("Найден вызов функции zip()")
        result.append("--------------OK structure -------------\n")

        # Выполнение функционального теста
        try:
            res = test_9_5_3_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_5_3_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "1 2 3 4\n5 6 7 8\n9 8 7 6",
        "3 4 5\n6 7 8\n9 3 4\n5 6 7",
    )

    # Ожидаемые данные вывода
    expected_output = (
        "1 5 9\n2 6 8\n3 7 7\n4 8 6",
        "3 6 9 5\n4 7 3 6\n5 8 4 7",
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
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            if captured_output == expected_output[i]:
                test_result.append(f"Получено:\n{captured_output}\n")
            else:
                raise  RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получено:\n{captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
