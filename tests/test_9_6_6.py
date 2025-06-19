# 9_6_6 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_6_6(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода: найти словарь и функцию, получить их имена"""
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
        func_name = None

        for node in ast.walk(tree):

            # Поиск функции
            if isinstance(node, ast.FunctionDef):
                func_name = node.name

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
        if not func_name:
            raise ValueError("ОШИБКА: Не найдена функция.")

        result.append(f"Найден словарь с именем: {dict_name}")
        result.append(f"Найдена функция с именем: {func_name}")
        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_9_6_6_1(path_tmp_file, dict_name, func_name)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_6_6_1(path_tmp_file: str, dict_name: str, func_name: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "смартфон:120000\nяблоко:2\nсумка:560\nбрюки:2500\nлинейка:10\nбумага:500",
        "смартфон:120000\nсумка:560\nбрюки:2500\nбумага:500\nпалатка:10000",
    )

    # Ожидаемые данные вывода
    expected_output = (
        "яблоко линейка бумага",
        "бумага сумка брюки",
    )

    # Проверяем словарь
    expected_dict = (
        {120000: 'смартфон', 2: 'яблоко', 560: 'сумка', 2500: 'брюки', 10: 'линейка', 500: 'бумага'},
        {120000: 'смартфон', 560: 'сумка', 2500: 'брюки', 500: 'бумага', 10000: 'палатка'},
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

            # Получаем из модуля словарь
            user_dict = getattr(user_module, dict_name)
            # Получаем из модуля функцию
            user_function = getattr(user_module, func_name)
            # Запускаем функцию пользователя
            answer = " ".join(user_function(expected_dict[i]))

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

            # Проверка работы функции
            if answer != expected_output[i]:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n" f"Ошибка: Функция возвращает не правильное значение"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
