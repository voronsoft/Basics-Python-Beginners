# 9_7_1 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_7_1(path_tmp_file: str, task_num_test: str):
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

        sort_used = False
        key_used = False

        # Проход по дереву AST
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = ""

                # Определяем имя функции, даже если это mylist.sort(...)
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name in {"sort", "sorted"}:
                    sort_used = True

                    # Проверяем, используется ли аргумент key
                    if any(kw.arg == "key" for kw in node.keywords):
                        key_used = True

        # Проверка, были ли найдены нужные вызовы
        if not sort_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции sort() или sorted().")

        result.append("Найден вызов функции sort()/sorted()")

        if key_used:
            result.append("Отлично! Параметр 'key' используется.")
        else:
            raise ValueError("ОШИБКА: Вызов sort()/sorted() без параметра 'key'.")

        result.append("--------------OK structure -------------\n")

        # Выполнение функционального теста
        try:
            res = test_9_7_1_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_7_1_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Лена Енисей Волга Дон",
        "Угрюм Свияга Тушонка Лена Обь",
    )

    # Ожидаемые данные вывода
    expected_output = (
        "Енисей Волга Лена Дон",
        "Тушонка Свияга Угрюм Лена Обь",
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
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            if captured_output == expected_output[i]:
                test_result.append(f"Получено: {captured_output}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
