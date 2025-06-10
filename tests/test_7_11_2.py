# 7_11_2 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_11_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие декоратора)"""

    result = []

    try:
        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        result.append(f"-------------Тест structure ------------")

        # Импортируем модуль пользователя
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data="8 11", capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Получаем перехваченный вывод из stdout
        captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

        # Парсим код в дерево
        tree = ast.parse(code)

        def check_decorator_in_code(tree_in, decorator_name):
            """Проверяет, что функция get_menu декорирована декоратором decorator_name=show_menu"""
            for node in ast.walk(tree_in):
                if isinstance(node, ast.FunctionDef) and node.name == 'get_menu':
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == decorator_name:
                            return True
            return False

        # Проверка, что функция get_menu декорирована декоратором show_menu
        if not check_decorator_in_code(tree, 'show_menu'):
            raise ValueError("ОШИБКА: Функция get_menu не декорирована декоратором show_menu")

        result.append("Функция get_menu декорирована декоратором show_menu.")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_11_2_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"1 Ошибка выполнения теста:\n\n{error_info}")


def test_7_11_2_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Главная Добавить Удалить Выйти",
        "Пункт1 Пункт2 Пункт3 Пункт4",
        "Дели Джакарта Стамбул Париж",
    )
    # Ожидаемый результат
    expected_output = (
        "1. Главная\n2. Добавить\n3. Удалить\n4. Выйти",
        "1. Пункт1\n2. Пункт2\n3. Пункт3\n4. Пункт4",
        "1. Дели\n2. Джакарта\n3. Стамбул\n4. Париж",
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

                get_menu = getattr(user_module, "get_menu")  # Получаем функцию из модуля
                # Выполняем функцию
                get_menu(test_input[i])

                # Получаем перехваченный вывод из stdout
                captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            # Проверяем результат перехваченного вывода
            if captured_output == expected_output[i]:
                test_result.append(f"Получено:\n{captured_output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен: {captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
