# 8_1_4 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_8_1_4(path_tmp_file: str, task_num_test: str):
    """Тест структуры: импорт factorial как fact, определение своей функции factorial, без вызовов"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Парсим код в дерево
        tree = ast.parse(code)

        def has_correct_import(tree_in):
            """Проверяет, что есть from math import factorial as fact"""
            for node in ast.walk(tree_in):
                if isinstance(node, ast.ImportFrom) and node.module == "math":
                    for alias in node.names:
                        if alias.name == "factorial" and alias.asname == "fact":
                            return True
            return False

        def has_own_factorial_def(tree_in):
            """Проверяет, что есть функция с именем factorial"""
            for node in ast.walk(tree_in):
                if isinstance(node, ast.FunctionDef) and node.name == "factorial":
                    return True
            return False

        # Проверки
        if not has_correct_import(tree):
            raise ValueError("ОШИБКА: Нет правильного импорта: from math import factorial as fact.")
        if not has_own_factorial_def(tree):
            raise ValueError("ОШИБКА: Функция factorial не определена.")

        result.append("Импорт: from math import factorial as fact — OK")
        result.append("Функция factorial определена — OK")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_8_1_4_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        print(error_info)
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_8_1_4_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (8, 5, 3)
    # Ожидаемый результат
    expected_output = (40320, 120, 6)

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=" ", capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

                factorial = getattr(user_module, "factorial")  # Получаем функцию пользователя из модуля
                # Выполняем функцию
                answer = factorial(test_input[i])

                # Получаем перехваченный вывод из stdout
                captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Проверяем результат перехваченного вывода
            if captured_output == "my factorial" and answer == expected_output[i]:
                test_result.append(f"Получено: {answer}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n" f"Ваше решение не правильное, попробуйте ещё раз..."
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
