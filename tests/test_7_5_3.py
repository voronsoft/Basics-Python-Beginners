# 7_5_3 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_5_3(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры"""

    result = []  # Список для накопления результатов тестов

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(user_code)

        # Разбор кода в дерево AST
        tree = ast.parse(user_code)

        find_func = False
        find_varargs = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == "get_biggest_city":
                    find_func = node.name
                    # Проверяем наличие *args в аргументах функции
                    if node.args.vararg:
                        find_varargs = True
                        arg_name = node.args.vararg.arg  # имя переменной (обычно 'args')

        if not find_func:
            raise ValueError("ОШИБКА: Не найдена функция 'get_biggest_city'")

        if not find_varargs:
            raise ValueError(
                "ОШИБКА: Функция get_biggest_city должна принимать произвольное количество аргументов (*args)"
            )

        result.append(f"Функция найдена: '{find_func}' с параметром *{arg_name}")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_5_3_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_5_3_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (("Прага", "Вена", "Хельсинки", "Стамбул"), ("Прага", "Вена", "Стамбул"))
    # Ожидаемый результат
    expected_output = ("Хельсинки", "Стамбул")

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data="", capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем перехваченный вывод из stdout
            captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Вызываем функцию
            get_biggest_city = getattr(user_module, "get_biggest_city")
            answer = get_biggest_city(*test_input[i])

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            if captured_output:
                raise RuntimeError("Ошибка: Вывод в консоль отключен")

            # Сравниваем результат с ожидаемым значением
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
