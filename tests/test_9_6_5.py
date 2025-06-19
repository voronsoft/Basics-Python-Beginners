# 9_6_5 тест для задачи
import ast
import importlib.util

from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_6_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Разбор кода в дерево AST
        tree = ast.parse(code)

        sort_used = False
        zip_used = False
        map_used = False

        # Проход по дереву AST
        for node in ast.walk(tree):
            # Проверка на вызовы функций (sort, sorted)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == 'sort' or node.func.id == 'sorted' or ".sort()" in code:
                    sort_used = True
                if node.func.id == 'zip':
                    zip_used = True
                if node.func.id == 'map':
                    map_used = True

        # Сообщения, если чего-то не хватает
        if not sort_used:
            raise ValueError("ОШИБКА: В коде не найдено использование: sort/sorted.")
        if not zip_used:
            result.append("Было бы не плохо использовать в решении zip()")
        if zip_used:
            result.append("Найден вызов функции zip")
        if map_used:
            result.append("Найден вызов функции map")

        result.append("Найден вызов функции sort/sorted")
        result.append("--------------OK structure -------------\n")

        # Выполнение функционального теста
        try:
            res = test_9_6_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_6_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "7 6 4 2 6 7 9 10 4\n-4 5 10 4 5 65",
        "7 6 4 2 7 9 10 4\n-4 5 10 4 5 65 10",
    )

    # Ожидаемые данные вывода
    expected_output = (
        "67 14 9 11 10 3",
        "67 14 14 11 12 11 5",
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
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
