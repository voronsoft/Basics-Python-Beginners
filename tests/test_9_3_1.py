# 9_3_1 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_3_1(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода — наличие map и next"""

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

        map_used = False
        next_used = False

        # Проход по дереву AST
        for node in ast.walk(tree):
            # Проверка на вызовы функций (map(...), next(...))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == 'map':
                    map_used = True
                elif node.func.id == 'next':
                    next_used = True

        # Сообщения, если чего-то не хватает
        if not map_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции map.")
        if not next_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции next.")

        result.append("Найден вызов функции map()")
        result.append("Найден вызов функции next()")
        result.append("--------------OK structure -------------\n")

        # Выполнение функционального теста
        try:
            res = test_9_3_1_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_3_1_1(path_tmp_file: str):
    """Функция тестирования работы пользовательского кода"""

    # Тестовые входные строки
    test_input = (
        "4.35 -10.6 1.0 200.34 0.56",
        "1.2 3.4 -5.6 7.8",
    )

    # Ожидаемые выходные строки
    expected_output = (
        "4.35 -10.6 1.0",
        "1.2 3.4 -5.6",
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
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")
            test_result.append(f"Получено: {captured_output}\n")

            # Сравнение результата
            if captured_output != expected_output[i]:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {captured_output}\n"
                )

            # Добавляем в общий результат
            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
