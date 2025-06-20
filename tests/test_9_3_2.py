# 9_3_2 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_3_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

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
        lst_is_list = False

        # Проход по дереву AST
        for node in ast.walk(tree):
            # Проверка на вызовы функций (map(...))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == 'map':
                    map_used = True

            # ПРОВЕРКА: lst — список
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "lst":
                        if isinstance(node.value, ast.List):
                            lst_is_list = True
                        elif isinstance(node.value, ast.Call):
                            if isinstance(node.value.func, ast.Name) and node.value.func.id == "list":
                                lst_is_list = True

        # Сообщения, если чего-то не хватает
        if not map_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции map.")

        if not lst_is_list:
            raise ValueError("ОШИБКА: Переменная 'lst' не найдена или не является списком.")

        result.append("Найден вызов функции map()")
        result.append("Переменная 'lst' является списком")
        result.append("--------------OK structure -------------\n")

        # Выполнение функционального теста
        try:
            res = test_9_3_2_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_3_2_1(path_tmp_file: str):
    """Функция тестирования работы пользовательского кода"""

    # Тестовые входные строки
    test_input = (
        "-5 6 8 11 -10 0",
        "1 2 3 -1 -2 -3",
    )

    # Ожидаемые выходные строки
    expected_output = (
        "5 6 8 11 10 0",
        "1 2 3 1 2 3",
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
