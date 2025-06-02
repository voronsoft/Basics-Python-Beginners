# 7_4_5 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_4_5(path_tmp_file: str, task_num_test: str):
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
        find_args = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == "constructor" and len(node.args.args) == 2:
                    find_func = node.name
                    find_args = len(node.args.args)

        if not find_func or not find_args:
            raise ValueError(
                "ОШИБКА: Не найдена функция 'constructor(data, tag='h1')'\nили неверное количество аргументов"
            )

        result.append(f"Функция найдена: '{find_func}' параметров: {find_args}")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_4_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_4_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = ("Работаем с функциями",)
    # Ожидаемый результат
    expected_output = ("<h1>Работаем с функциями</h1>", "<div>Работаем с функциями</div>")

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=test_input[i], capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем перехваченный вывод из stdout
            captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Вызываем функцию
            constructor = getattr(user_module, "constructor")
            answer_h1 = constructor(test_input[i])
            answer_div = constructor(test_input[i], "div")

            # Формируем отчет по тесту
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось:\n{'\n'.join(expected_output)}")

            if captured_output != "<h1>Работаем с функциями</h1>\n<div>Работаем с функциями</div>":
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Ожидалось:\n{'\n'.join(expected_output)}\nно получен:\n{captured_output}\n"
                )

            if answer_h1 == expected_output[i] and answer_div == expected_output[-1]:
                test_result.append(f"Получено:\n{answer_h1}\n{answer_div}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось:\n{'\n'.join(expected_output)}\nно получен:\n{'\n'.join((answer_h1, answer_div))}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)
    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
