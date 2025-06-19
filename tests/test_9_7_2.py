# 9_7_2 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_7_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code, allowed_imports=["sys"], allowed_calls=["sys.stdin.readlines"])

        # Разбор в AST
        tree = ast.parse(code)

        dict_name = None
        sort_used = False
        key_used = False

        for node in ast.walk(tree):
            # Поиск "sort", "sorted", "key"
            if isinstance(node, ast.Call):
                func_name = ""

                # Определяем имя функции, даже если это mylist.sort(...)
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name in {"sort", "sorted"}:
                    sort_used = True

                    # Проверяем, используется ли аргумент key
                    if any(kw.arg == "key" for kw in node.keywords):
                        key_used = True

            # Поиск словаря через:
            # - обычный словарь: ast.Dict
            # - генератор словаря: ast.DictComp
            # - вызов dict(): ast.Call with func.id == 'dict'
            if isinstance(node, ast.Assign):
                value = node.value

                is_dict = (
                    isinstance(value, ast.Dict)
                    or isinstance(value, ast.DictComp)
                    or (isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'dict')
                )

                if is_dict:
                    if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                        dict_name = node.targets[0].id

        if not dict_name:
            raise ValueError("ОШИБКА: Не найдено присваивание словаря (dict, dict comprehension или вызов dict()).")

        result.append(f"Найден словарь с именем: {dict_name}")

        # Проверка, были ли найдены нужные вызовы
        if not sort_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции sort() или sorted().")

        result.append("Найден вызов функции sort()/sorted()")

        if key_used:
            result.append("Отлично! Параметр 'key' используется.")
        else:
            raise ValueError("ОШИБКА: Вызов sort()/sorted() без параметра 'key'.")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_9_7_2_1(path_tmp_file, dict_name)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_7_2_1(path_tmp_file: str, dict_name: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "ножницы=100\nкотелок=500\nспички=20\nзажигалка=40\nзеркальце=50",
        "ножницы=10\nкотелок=500\nспички=200\nзажигалка=40\nзеркальце=150",
    )

    # Ожидаемые данные вывода
    expected_output = (
        "котелок ножницы зеркальце зажигалка спички",
        "котелок спички зеркальце зажигалка ножницы",
    )

    # Проверяем словарь
    expected_dict = (
        {'ножницы': 100, 'котелок': 500, 'спички': 20, 'зажигалка': 40, 'зеркальце': 50},
        {'ножницы': 10, 'котелок': 500, 'спички': 200, 'зажигалка': 40, 'зеркальце': 150},
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

            # Получаем словарь
            user_dict = getattr(user_module, dict_name)

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Проверка вывода в консоль
            if captured_output == expected_output[i]:
                test_result.append(f"Получено: {captured_output}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {captured_output}\n"
                )

            # Проверка формирования словаря
            if user_dict != expected_dict[i]:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n" f"Ошибка: Словарь формируется НЕ правильно."
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
