# 7_12_3 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_7_12_3(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code)

        decorator_names = []  # имена подходящих декораторов
        decorated_funcs = []  # функции с декораторами

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                arg_names = [arg.arg for arg in node.args.args]
                if "chars" in arg_names:
                    chars_index = arg_names.index("chars")
                    num_total_args = len(arg_names)
                    num_defaults = len(node.args.defaults)
                    first_default_index = num_total_args - num_defaults

                    # Проверка: есть ли значение по умолчанию у параметра chars
                    if chars_index >= first_default_index:
                        default_value = node.args.defaults[chars_index - first_default_index]
                        if isinstance(default_value, ast.Constant) and default_value.value == " !?":
                            result.append("Декоратор имеет параметр chars со значением по умолчанию ' !?'")
                        else:
                            raise ValueError("Параметр 'chars' в декораторе должен иметь значение по умолчанию ' !?'")
                    else:
                        raise ValueError("Параметр 'chars' в декораторе должен иметь значение по умолчанию ' !?'")

                    decorator_names.append(node.name)

                # Сохраняем все функции, у которых есть хотя бы один декоратор
                if node.decorator_list:
                    decorated_funcs.append(node)

        if not decorator_names:
            raise ValueError(
                "ОШИБКА: Не найдена функция-декоратор, принимающая параметр 'chars' со значением по умолчанию ' !?'.")

        if not decorated_funcs:
            raise ValueError("ОШИБКА: Не найдена ни одна задекорированная функция.")

        # Проверяем, что хотя бы одна функция задекорирована нужным декоратором
        matched_func = None
        for func in decorated_funcs:
            for decorator in func.decorator_list:
                # Ищем: @decorator(chars=...)
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                    if decorator.func.id in decorator_names:
                        if len(func.args.args) >= 1:
                            matched_func = func.name
                            break

        if not matched_func:
            raise ValueError(
                "ОШИБКА: Не найдена функция, задекорированная декоратором с параметром 'chars' и принимающая 1 аргумент.")

        result.append(f"Декоратор найден, применяется к функции '{matched_func}', которая принимает параметр(ы).")
        result.append("--------------OK structure -------------\n")

        print("decorated_funcs", decorated_funcs[0].name, matched_func)
        print("decorator_names[0]", decorator_names[0])
        # Дополнительно — тест выполнения кода
        try:
            res = test_7_12_3_1(path_tmp_file, matched_func, decorator_names[0])
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_12_3_1(path_tmp_file: str, fnc_name, dec_name):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Декораторы - это круто!",
        "Python - is the best language",
        "Балакирев",
    )
    # Ожидаемый результат
    expected_output = (
        "dekoratory-eto-kruto-",
        "python-is-the-best-language",
        "balakirev",
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("module.name", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Подменяем stdin с тестовыми данными
            sys.stdin = StringIO(test_input[i])

            # Создаем буфер для перехвата вывода
            output_buffer = StringIO()
            # Сохраняем оригинальный stdout
            original_stdout = sys.stdout
            # Перенаправляем stdout в буфер
            sys.stdout = output_buffer

            spec.loader.exec_module(user_module)

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

            func = getattr(user_module, fnc_name)  # Получаем функцию из модуля
            # Выполняем функцию
            data = test_input[i]
            func(data)
            # Получаем перехваченный вывод из print()
            captured_output = output_buffer.getvalue().rstrip()
            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

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
