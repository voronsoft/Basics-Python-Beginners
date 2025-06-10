# 7_12_2 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_12_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Парсим код в дерево
        tree = ast.parse(code)

        decorator_names = []  # имена подходящих декораторов
        decorated_funcs = []  # функции с декораторами

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                arg_names = [arg.arg for arg in node.args.args]
                if "tag" in arg_names:
                    tag_index = arg_names.index("tag")
                    num_total_args = len(arg_names)
                    num_defaults = len(node.args.defaults)
                    first_default_index = num_total_args - num_defaults

                    # Проверка: есть ли значение по умолчанию у параметра tag
                    if tag_index >= first_default_index:
                        default_value = node.args.defaults[tag_index - first_default_index]
                        if isinstance(default_value, ast.Constant) and default_value.value == "h1":
                            result.append("Декоратор имеет параметр tag со значением по умолчанию 'h1'")
                        else:
                            raise ValueError("Параметр 'tag' в декораторе должен иметь значение по умолчанию 'h1'")
                    else:
                        raise ValueError("Параметр 'tag' в декораторе должен иметь значение по умолчанию 'h1'")

                    decorator_names.append(node.name)

                # Сохраняем все функции, у которых есть хотя бы один декоратор
                if node.decorator_list:
                    decorated_funcs.append(node)

        if not decorator_names:
            raise ValueError(
                "ОШИБКА: Не найдена функция-декоратор, принимающая параметр 'tag' со значением по умолчанию 'h1'."
            )

        if not decorated_funcs:
            raise ValueError("ОШИБКА: Не найдена ни одна задекорированная функция.")

        # Проверяем, что хотя бы одна функция задекорирована нужным декоратором
        matched_func = None
        for func in decorated_funcs:
            for decorator in func.decorator_list:
                # Ищем: @decorator(tag=...)
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                    if decorator.func.id in decorator_names:
                        if len(func.args.args) == 1:
                            matched_func = func.name
                            break

        if not matched_func:
            raise ValueError(
                "ОШИБКА: Не найдена функция, задекорированная декоратором с параметром 'tag' и принимающая 1 аргумент."
            )

        result.append(f"Декоратор найден, применяется к функции '{matched_func}', которая принимает 1 параметр.")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_12_2_1(path_tmp_file, matched_func, decorator_names[0])
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_12_2_1(path_tmp_file: str, fnc_name, dec_name):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Декораторы - это классно!",
        "Сергей Балакирев",
        "Python",
    )
    # Ожидаемый результат
    expected_output = (
        "<div>декораторы - это классно!</div>",
        "<div>сергей балакирев</div>",
        "<div>python</div>",
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
                    f"Ожидалось: {expected_output[i]}\nно получен: {captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
