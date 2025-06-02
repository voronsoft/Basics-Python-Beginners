# 7_5_5 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_5_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры"""
    result = []  # Список для накопления результатов тестов

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()
            # Проверка кода на безопасность
            check_code_safety(user_code, allowed_imports=["sys"], allowed_calls=["sys.stdin.readlines"])

        # Разбор кода в дерево AST
        tree = ast.parse(user_code)

        find_func = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == "verify":
                    find_func.append(node.name)
                if node.name == "is_isolate":
                    find_func.append(node.name)

        if len(find_func) != 2:
            raise RuntimeError("ОШИБКА: В коде необходимо объявить функции: 'verify' и 'is_isolate'")

        result.append(f"Функции 'verify' и 'is_isolate' найдены")

        if "lst2D" not in user_code:
            raise RuntimeError("ОШИБКА: lst2D не найден")

        result.append("lst2D найден")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_5_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")


def test_7_5_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        [
            [1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1],
            [0, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 1, 0],
            [0, 0, 0],
            [1, 0, 1],
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [[1, 0], [0, 1]],
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
        ],
        [
            [1, 0, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
        ],
        [
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [1, 1, 0, 0],
        ],
    )
    # Ожидаемый результат
    expected_output = (
        True,
        False,
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(
                stdin_data="0 1 0\n0 0 0\n1 0 1", capture_stdout=True, capture_stderr=True
            ) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем перехваченный вывод из stdout
            captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Проверка формирования lst2D разово
            if i == 0:
                # Получаем из модуля
                lst2D = getattr(user_module, "lst2D")
                if lst2D != test_input[2]:
                    raise RuntimeError("ОШИБКА: Неправильно формируется 'lst2D'")

            # Вызываем функцию
            verify = getattr(user_module, "verify")
            answer = verify(test_input[i])

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Сравниваем результат с ожидаемым значением
            if answer == expected_output[i]:
                test_result.append(f"Получено: {answer}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {answer}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
