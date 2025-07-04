# 8_1_5 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_8_1_5(path_tmp_file: str, task_num_test: str):
    """Тест структуры: импорт seed и randint из random, и вызов seed(1), print(randint(...))"""

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
            """Проверяет, что импортированы seed и randint из random (вместе или по отдельности)"""
            imported_names = set()
            for node in ast.walk(tree_in):
                if isinstance(node, ast.ImportFrom) and node.module == "random":
                    for alias in node.names:
                        imported_names.add(alias.name)
            return "seed" in imported_names and "randint" in imported_names

        def calls_seed_and_randint(tree_in):
            """Проверяет, что есть вызов seed(1) и print(randint(10, 50))"""
            seed_call_found = False
            randint_in_print_found = False

            for node in ast.walk(tree_in):
                if isinstance(node, ast.Call):
                    # seed(1)
                    if isinstance(node.func, ast.Name) and node.func.id == "seed":
                        if len(node.args) == 1 and isinstance(node.args[0], ast.Constant) and node.args[0].value == 1:
                            seed_call_found = True

                    if isinstance(node.func, ast.Name) and node.func.id == "print":
                        if len(node.args) == 1 and isinstance(node.args[0], ast.Call):
                            inner = node.args[0]
                            if isinstance(inner.func, ast.Name) and inner.func.id == "randint":
                                if (
                                    len(inner.args) == 2
                                    and all(isinstance(arg, ast.Constant) for arg in inner.args)
                                    and inner.args[0].value == 10
                                    and inner.args[1].value == 50
                                ):
                                    randint_in_print_found = True

            return seed_call_found and randint_in_print_found

        # Выполняем проверки
        if not has_correct_import(tree):
            raise ValueError("ОШИБКА: Нет правильного импорта: from random import seed, randint.")
        if not calls_seed_and_randint(tree):
            raise ValueError("ОШИБКА: Не найдены вызовы seed(1) или print(randint(10, 50)).")

        result.append("Импорт: from random import seed, randint — OK")
        result.append("Вызов seed(1) и print(randint(10, 50)) — OK")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_8_1_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_8_1_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""

    # Ожидаемый результат вывода при seed(1) и randint(10, 50)
    expected_output = "18"

    result = []  # Список для накопления результатов тестов

    try:
        # Импортируем модуль пользователя
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data=" ", capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Получаем перехваченный вывод из stdout
        captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

        # Проверяем результат
        test_result = list()
        test_result.append(f"---------------OK Тест --------------")
        test_result.append(f"Ожидалось: {expected_output}")
        test_result.append(f"Получено: {captured_output}")

        # Сравнение результата
        if captured_output == expected_output:
            result.append("\n".join(test_result))
        else:
            raise ValueError(
                f"------------- FAIL Тест --------\n" f"Ожидалось: {expected_output}\nно получено: {captured_output}\n"
            )

        return "\n".join(result)

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
