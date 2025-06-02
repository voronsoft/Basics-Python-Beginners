# 7_4_4 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_4_4(path_tmp_file: str, task_num_test: str):
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
                if len(node.args.args) == 2:
                    find_func = node.name
                    find_args = len(node.args.args)

        if not find_func or not find_args:
            raise ValueError("ОШИБКА: Не найдена функция\nили неверное количество аргументов")

        result.append(f"Функция найдена: '{find_func}' параметров: {find_args}")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_4_4_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_4_4_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Лучший курс по Python!",
        "Я люблю Python",
        "Это очень круто",
    )
    # Ожидаемый результат
    expected_output = (
        "luchshiy-kurs-po-python!\nluchshiy+kurs+po+python!",
        "ya-lyublyu-python\nya+lyublyu+python",
        "eto-ochen-kruto\neto+ochen+kruto",
    )

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

            # Формируем отчет по тесту
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            if captured_output == expected_output[i]:
                test_result.append(f"Получено:\n{captured_output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)
    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
