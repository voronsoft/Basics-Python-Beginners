# 9_3_3 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_9_3_3(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        tree = ast.parse(code)

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
            # Импортируем модуль из файла
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Подмена stdin (ввод)
            sys.stdin = StringIO(test_input[i])
            # Заглушка для sys.stderr
            original_stderr = sys.stderr  # сохраняем оригинал
            sys.stderr = StringIO()  # подменяем на буфер

            # Запускаем пользовательский код
            spec.loader.exec_module(user_module)

            # Теперь проверим, что переменная lst2D существует и является списком
            if not hasattr(user_module, "lst2D"):
                raise ValueError(f"ОШИБКА: Переменная 'lst2D' не найдена в модуле.")

            lst2D = user_module.lst2D

            # Проверка, что lst2D — это список
            if not isinstance(lst2D, list):
                raise ValueError(f"ОШИБКА: Переменная 'lst2D' должна быть списком, а не {type(lst2D)}.")

            # Проверка, что все элементы lst2D — это списки
            for row in lst2D:
                if not isinstance(row, list):
                    raise ValueError(
                        f"ОШИБКА: Каждый элемент lst2D должен быть списком, но найден элемент типа {type(row)}."
                    )

                # Проверка, что все элементы внутри вложенных списков — это целые числа
                for elem in row:
                    if not isinstance(elem, int):
                        raise ValueError(
                            f"ОШИБКА: Все элементы во вложенных списках должны быть целыми числами, найдено: {type(elem)}."
                        )

            # Проверка, что lst2D соответствует ожидаемому результату
            if lst2D != expected_output[i]:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {lst2D}\n"
                )

            # Сборка отчёта по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")
            test_result.append(f"Получено: {lst2D}\n")

            # Добавляем в общий результат
            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
