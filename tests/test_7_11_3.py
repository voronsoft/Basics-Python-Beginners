# 7_11_3 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_7_11_3(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие декоратора)"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Парсим AST
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code)

        def analyze_get_list(tree_in):
            """Возвращает кортеж:
            (есть ли декоратор, сколько параметров у функции get_list)"""
            for node in ast.walk(tree_in):
                if isinstance(node, ast.FunctionDef) and node.name == 'get_list':
                    num_args = len(node.args.args)
                    has_decorator = len(node.decorator_list) > 0
                    return has_decorator, num_args
            return None, None  # функция не найдена

        has_decorator, num_args = analyze_get_list(tree)

        if has_decorator is None:
            raise ValueError("ОШИБКА: Функция get_list не найдена.")
        if not has_decorator:
            raise ValueError("ОШИБКА: Функция get_list не задекорирована.")
        if num_args != 1:
            raise ValueError(f"ОШИБКА: Функция get_list должна принимать ровно один параметр, найдено: {num_args}")

        result.append("Функция get_list задекорирована и принимает 1 параметр.")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_11_3_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        print(error_info)
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_11_3_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "8 11 -5 4 3 10",
        "5 4 3 6 4 6 7 8 9 -1",
        "1 2",
    )
    # Ожидаемый результат
    expected_output = (
        "-5 3 4 8 10 11",
        "-1 3 4 4 5 6 6 7 8 9",
        "1 2",
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("module.name", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Подменяем stdin с тестовыми данными
            sys.stdin = StringIO(test_input[i])

            # Создаем буфер для перехвата вывода
            output_buffer = StringIO()
            # Сохраняем оригинальный stdout
            original_stdout = sys.stdout
            # Перенаправляем stdout в буфер
            sys.stdout = output_buffer

            spec.loader.exec_module(user_module)

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

            get_list = getattr(user_module, "get_list")  # Получаем функцию из модуля
            # Выполняем функцию
            get_list(test_input[i])
            # Получаем перехваченный вывод из print()
            captured_output = output_buffer.getvalue().rstrip()
            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

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
