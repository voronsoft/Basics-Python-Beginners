# 7_8_2 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_8_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append(f"-------------Тест structure ------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(user_code)

        # Импортируем модуль пользователя
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data=" ", capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Проверяем что есть необходимые атрибуты в коде пользователя
        if not hasattr(user_module, "get_sq"):
            raise AttributeError("ОШИБКА: переменная 'get_sq' не найдена в коде пользователя")

        # Разбор кода в дерево AST
        tree = ast.parse(user_code)

        lambda_found = False

        # Проверка что 'get_sq' присвоена лямбда функция
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "get_sq":
                        if isinstance(node.value, ast.Lambda):
                            lambda_found = True

                            # Проверка: один параметр
                            if len(node.value.args.args) != 1:
                                raise ValueError("ОШИБКА: лямбда-функция должна иметь 1 параметр")

                            result.append("Переменной 'get_sq' присвоена лямбда-функция с одним параметром")

        if not lambda_found:
            raise TypeError("ОШИБКА: переменной 'get_sq' не присвоена лямбда-функция")

        result.append("--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_8_2_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_8_2_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        6,
        -2,
        11,
    )
    # Ожидаемый результат
    expected_output = (
        36,
        4,
        121,
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

            # Получаем get_sq из модуля пользователя
            get_sq = getattr(user_module, 'get_sq')
            # Вызываем функцию с тестовым вводом
            answer = get_sq(test_input[i])

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            if answer == expected_output[i]:
                test_result.append(f"Получено: {answer}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {answer}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
