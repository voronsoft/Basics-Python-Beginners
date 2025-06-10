# 7_11_5 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_11_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие декоратора и двух параметров у декорируемой функции)"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение и разбор кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Парсим код в дерево
        tree = ast.parse(code)

        # Ищем все функции, у которых есть декораторы
        decorated_funcs = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.decorator_list:
                decorated_funcs.append((node.name, len(node.args.args)))

        if not decorated_funcs:
            raise ValueError("ОШИБКА: Не найдена ни одна задекорированная функция.")

        # Ищем функцию с 1 параметром
        target_funcs = [f for f in decorated_funcs if f[1] == 1]

        if not target_funcs:
            raise ValueError(f"ОШИБКА: Функция {decorated_funcs[0][0]}\nдолжна принимать всего один параметр - строку.")
        elif len(target_funcs) > 1:
            raise ValueError(
                f"ОШИБКА: Найдено несколько задекорированных функций с 1 параметром: {[f[0] for f in target_funcs]}"
            )
        else:
            result.append(f"Функция '{target_funcs[0][0]}' найдена, задекорирована и принимает параметры.")

        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_11_5_1(path_tmp_file, target_funcs[0][0])
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_11_5_1(path_tmp_file: str, fnc_name):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Python - это круто!",
        "Сергей Балакирев",
        "Декораторы - это классно",
    )
    # Ожидаемый результат
    expected_output = (
        "python-eto-kruto!",
        "sergey-balakirev",
        "dekoratory-eto-klassno",
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

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Проверяем результат перехваченного вывода
            if captured_output == expected_output[i]:
                test_result.append(f"Получено: {captured_output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
