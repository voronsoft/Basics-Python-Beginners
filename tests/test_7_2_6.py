# 7_2_6 тест для задачи
import ast
import importlib.util
import sys

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_2_6(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(user_code)

        # Разбор кода в дерево AST
        tree = ast.parse(user_code)

        find_func = False

        # Поиск определения функции с аргументами
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == "get_sq" and len(node.args.args) >= 1:
                    find_func = node.name

        if not find_func:
            raise ValueError("ОШИБКА: Не найдено определение функции 'def get_sq(...)'\nили неверное количество аргументов")

        result.append(f"Функция найдена: {find_func}")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_2_6_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_2_6_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    test_input = [
        ("RECT", 2, (5, 2), 10),
        ("SQ", 1, (5,), 25),
        ("OTHER", 1, (4,), 16),
    ]

    result = []  # Список для накопления результатов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Подготавливаем входные данные для проверки кода
            input_data, expected_args, call_args, expected_answer = test_input[i]

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=input_data, capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля
                # Получаем перехваченный вывод из stdout
                captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""



            # Подготовка теста
            test_result = [
                f"---------------OK Тест: {i + 1} --------------",
                f"Входные данные: tp='{input_data}'",
                f"Аргументы функции: {call_args}",
                f"Ожидалось аргументов: {expected_args}",
            ]

            # Проверка результата
            answer_output = user_module.get_sq(*call_args)
            test_result.append(f"Ожидаемый результат: {expected_answer}")
            test_result.append(f"Получено: {answer_output}\n")

            # Проверка вывода в консоль
            if captured_output:
                raise ValueError("Ошибка: В консоль выводить ничего не нужно.")

            # Сравниваем результат с ожидаемым значением
            if answer_output != expected_answer:
                raise ValueError(
                    f"------------- FAIL Тест {i+1} --------\n"
                    f"Неверный результат вычислений\n"
                    f"Ожидалось: {expected_answer}\n"
                    f"Получено: {answer_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)
    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
    finally:
        sys.stdin = sys.__stdin__
