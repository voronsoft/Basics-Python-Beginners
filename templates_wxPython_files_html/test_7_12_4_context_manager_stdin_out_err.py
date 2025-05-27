# 7_12_4 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_12_4(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие декоратора)"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Парсим AST
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        tree = ast.parse(code)

        def analyze_get_list(tree_in):
            """Возвращает кортеж:
            (есть ли декоратор, сколько параметров у функции get_list)"""
            for node in ast.walk(tree_in):
                if isinstance(node, ast.FunctionDef) and node.name == 'get_list':
                    num_args = len(node.args.args)
                    has_decorator = len(node.decorator_list) > 0
                    return has_decorator, num_args
            return None, None  # функция не найдена

        def uses_wraps_decorator(tree_in):
            """Проверяет, использован ли @wraps внутри определения функции-декоратора"""
            for node in ast.walk(tree_in):
                if isinstance(node, ast.FunctionDef):
                    for inner_node in ast.walk(node):
                        # ищем: @wraps(some_function)
                        if isinstance(inner_node, ast.Call) and isinstance(inner_node.func, ast.Name):
                            if inner_node.func.id == "wraps":
                                return True
            return False

        has_decorator, num_args = analyze_get_list(tree)

        if has_decorator is None:
            raise ValueError("ОШИБКА: Функция get_list не найдена.")
        if not has_decorator:
            raise ValueError("ОШИБКА: Функция get_list не задекорирована.")
        if num_args != 1:
            raise ValueError(f"ОШИБКА: Функция get_list должна принимать ровно один параметр, найдено: {num_args}")
        if not uses_wraps_decorator(tree):
            raise ValueError(
                "ОШИБКА: В декораторе не используется @wraps. Он необходим для сохранения __name__ и __doc__."
            )

        result.append("Функция get_list задекорирована и принимает 1 параметр.")
        result.append("Функция get_list задекорирована, принимает 1 параметр, декоратор использует @wraps.")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_12_4_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_12_4_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    test_input = ("8 11 -5 4 3 10",)
    expected_output = (31,)

    result = []

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=test_input[i], capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем функцию из модуля
            get_list = getattr(user_module, "get_list")
            # Вызываем функцию с тестовым вводом
            out_answer = get_list(test_input[i])
            # Получаем перехваченный вывод из stdout
            captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            if out_answer == expected_output[i]:
                test_result.append(f"Получено: {out_answer}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\n"
                    f"Получено: {out_answer}\n"
                )

            # Проверяем __doc__
            d = get_list.__doc__
            if d != 'Функция для формирования списка целых значений':
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Ожидалось: 'Функция для формирования списка целых значений'\n"
                    f"Получено: '{d}'\n"
                )
            else:
                test_result.append(f"__doc__ = {d}")

            # Проверяем __name__
            n = get_list.__name__
            if n != 'get_list':
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n" f"Ожидалось: 'get_list'\n" f"Получено: '{n}'\n"
                )
            else:
                test_result.append(f"__name__ = {n}")

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
