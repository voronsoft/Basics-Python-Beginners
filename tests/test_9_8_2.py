# 9_8_2 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_8_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Разбор в AST
        tree = ast.parse(code)

        func_found = False
        isinstance_used = False

        for node in ast.walk(tree):
            # Поиск определения функции get_add с двумя аргументами
            if isinstance(node, ast.FunctionDef):
                if node.name == "get_add" and len(node.args.args) == 2:
                    func_found = True

            # Поиск вызова isinstance(...)
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "isinstance":
                    isinstance_used = True

        if not func_found:
            raise RuntimeError("ОШИБКА: В коде не найдена функция get_add(a, b)")

        result.append("Найдена функция get_add(a, b)")

        if not isinstance_used:
            raise RuntimeError("ОШИБКА: В коде не найден вызов функции isinstance")

        result.append("Найден вызов функции isinstance")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_9_8_2_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_8_2_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        (2.2, 2.2),
        (5, 5),
        ("прав", "ильно"),
        (5, "нет"),
    )

    # Ожидаемые данные вывода
    expected_output = (
        (4.4),
        (10),
        ("правильно"),
        (None),
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=" ", capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем перехваченный вывод из stdout
            captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Получаем из модуля get_add
            get_add = getattr(user_module, "get_add")
            # Выполняем
            answer = get_add(*test_input[i])

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Проверка формирования списка
            if answer == expected_output[i]:
                test_result.append(f"Получено: {answer}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Ожидалось: {expected_output}\nно получено: {answer}"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
