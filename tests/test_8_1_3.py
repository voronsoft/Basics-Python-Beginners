# 8_1_3 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_8_1_3(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие импорта math и вызова math.floor или floor)"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Парсим код в дерево
        tree = ast.parse(code)

        def has_math_import(tree_in):
            """Проверка на import math или from math import floor"""
            for node in ast.walk(tree_in):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == 'math':
                            return True
                elif isinstance(node, ast.ImportFrom):
                    if node.module == 'math':
                        for alias in node.names:
                            if alias.name == 'floor':
                                return True
            return False

        def calls_floor_function(tree_in):
            """Проверка, вызывается ли math.floor(...) или просто floor(...)"""
            for node in ast.walk(tree_in):
                if isinstance(node, ast.Call):
                    func = node.func
                    # math.floor(...)
                    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                        if func.value.id == 'math' and func.attr == 'floor':
                            return True
                    # floor(...)
                    elif isinstance(func, ast.Name):
                        if func.id == 'floor':
                            return True
            return False

        # Выполняем проверки
        if not has_math_import(tree):
            raise ValueError("ОШИБКА: Не найден импорт math или from math import floor.")
        if not calls_floor_function(tree):
            raise ValueError("ОШИБКА: Не найден вызов math.floor(...) или floor(...).")

        result.append("Импорт math или from math import floor — OK")
        result.append("Вызов math.floor(...) или floor(...) — OK")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_8_1_3_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"

        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_8_1_3_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = ('8.11', '-10.5', '2.3')
    # Ожидаемый результат
    expected_output = ('8', '-11', '2')

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

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Проверяем результат перехваченного вывода
            if captured_output == expected_output[i]:
                test_result.append(f"Получено: {captured_output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
