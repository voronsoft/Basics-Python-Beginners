# 8_1_4 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_8_1_4(path_tmp_file: str, task_num_test: str):
    """Тест структуры: импорт factorial как fact, определение своей функции factorial, без вызовов"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
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
            spec = importlib.util.spec_from_file_location("module.name", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(user_module)

            # Создаем буфер для перехвата вывода
            output_buffer = StringIO()
            # Сохраняем оригинальный stdout
            original_stdout = sys.stdout
            # Перенаправляем stdout в буфер
            sys.stdout = output_buffer

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            func = getattr(user_module, "factorial")  # Получаем функцию из модуля
            # Выполняем функцию
            return_answer = func(test_input[i])

            # Получаем перехваченный вывод из print()
            captured_output = output_buffer.getvalue().rstrip()
            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

            # Проверяем результат перехваченного вывода
            if captured_output == "my factorial" and return_answer == expected_output[i]:
                test_result.append(f"Получено: {return_answer}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {return_answer}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
