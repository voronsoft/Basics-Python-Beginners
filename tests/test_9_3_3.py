# 9_3_3 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_3_3(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()

        # Проверка кода на безопасность
        check_code_safety(user_code, allowed_imports=["sys"], allowed_calls=["sys.stdin.readlines"])

        # Разбор кода в дерево AST
        tree = ast.parse(user_code)

        lst_in_found = False
        lst2D_found = False
        map_used_in_lst2D = False
        map_used_in_lst_in = False

        def contains_map_call(node):
            """Рекурсивно ищет вызов map() в поддереве AST."""
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    if child.func.id == "map":
                        return True
            return False

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id == "lst_in":
                            lst_in_found = True
                            if contains_map_call(node.value):
                                map_used_in_lst_in = True
                        elif target.id == "lst2D":
                            lst2D_found = True
                            if contains_map_call(node.value):
                                map_used_in_lst2D = True

        if not lst_in_found:
            raise ValueError("ОШИБКА: Переменная 'lst_in' не найдена.")
        if not lst2D_found:
            raise ValueError("ОШИБКА: Переменная 'lst2D' не найдена.")
        if not map_used_in_lst_in:
            raise ValueError("ОШИБКА: lst_in должно использовать функцию map.")
        if not map_used_in_lst2D:
            raise ValueError("ОШИБКА: lst2D должно использовать функцию map.")

        result.append("Переменная lst_in найдена")
        result.append("Переменная lst2D найдена")
        result.append("Найден вызов map() для lst_in")
        result.append("Найден вызов map() для lst2D")
        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_9_3_3_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_3_3_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""

    # Тестовые входные строки (таблица чисел)
    test_input = (
        "8 11 -5\n3 4 10\n-1 -2 3\n4 5 6",
        "1 2 3 4\n5 6 7 8\n9 8 7 6",
    )

    # Ожидаемый результат: двумерный список
    expected_output = (
        [[8, 11, -5], [3, 4, 10], [-1, -2, 3], [4, 5, 6]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6]],
    )

    result = []  # Для хранения результатов тестов

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

            # Сборка отчёта по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")
            # test_result.append(f"Получено: {lst2D}\n")

            lst2D = getattr(user_module, "lst2D")

            # Проверка, что lst2D соответствует ожидаемому результату
            if lst2D != expected_output[i]:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {lst2D}\n"
                )

            # Добавляем в общий результат
            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
