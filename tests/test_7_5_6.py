# 7_5_6 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_5_6(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры"""

    result = []  # Список для накопления результатов тестов

    try:
        result.append(f"-------------Тест structure ------------")

        # Читаем исходный код для анализа AST
        with open(path_tmp_file, 'r', encoding='utf-8') as f:
            user_code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(user_code)

        # Разбор кода в дерево AST
        tree = ast.parse(user_code)

        find_str_min = False
        find_str_min3 = False
        find_str_min4 = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == 'str_min':
                    find_str_min = True
                elif node.name == 'str_min3':
                    for subnode in ast.walk(node):
                        if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Name):
                            if subnode.func.id == 'str_min':
                                find_str_min3 = True
                elif node.name == 'str_min4':
                    for subnode in ast.walk(node):
                        if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Name):
                            if subnode.func.id == 'str_min':
                                find_str_min4 = True

        if not find_str_min3:
            raise ValueError("ОШИБКА: функция str_min3 не использует str_min")
        if not find_str_min4:
            raise ValueError("ОШИБКА: функция str_min4 не использует str_min")

        result.append("Проверка использования str_min в str_min3 и str_min4: OK")

        result.append(f"--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_5_6_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_5_6_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные и ожидаемые результаты
    test_data = (
        # (аргументы для функций, ожидаемые результаты для str_min, str_min3, str_min4)
        (("значимый", "подвиг"), "значимый", "значимый", "значимый"),
        (("это", "заметный", "подвиг"), "заметный", "заметный", "заметный"),
        (("я", "выполнил", "значимый", "подвиг"), "выполнил", "выполнил", "выполнил"),
        (("морковка", "уха"), "морковка", "морковка", "морковка"),
        (("самара", "тольятти", "ульяновск"), "самара", "самара", "самара"),
        (("омск", "самара", "тольятти", "ульяновск"), "омск", "омск", "омск"),
    )

    result = []  # Список для накопления результатов тестов

    try:
        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data="", capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Получаем функции для тестирования
        str_min = user_module.str_min
        str_min3 = user_module.str_min3
        str_min4 = user_module.str_min4

        for i, (args, exp_min, exp_min3, exp_min4) in enumerate(test_data):
            test_result = []
            test_result.append(f"---------------Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {args}")

            # Тестируем str_min если передано 2 аргумента
            if len(args) >= 2:
                output = str_min(*args[:2])
                test_result.append(f"str_min ожидалось: {exp_min}")
                if output == exp_min:
                    test_result.append(f"str_min получено: {output}")
                else:
                    raise ValueError(f"str_min получено: {output}")

            # Тестируем str_min3 если передано 3 аргумента
            if len(args) >= 3:
                output = str_min3(*args[:3])
                test_result.append(f"str_min3 ожидалось: {exp_min3}")
                if output == exp_min3:
                    test_result.append(f"str_min3 получено: {output}")
                else:
                    raise ValueError(f"str_min3 получено: {output}")

            # Тестируем str_min4 если передано 4 аргумента
            if len(args) >= 4:
                output = str_min4(*args[:4])
                test_result.append(f"str_min4 ожидалось: {exp_min4}")
                if output == exp_min4:
                    test_result.append(f"str_min4 получено: {output}")
                else:
                    raise ValueError(f"str_min4 получено: {output}")

            test_result.append("")  # Пустая строка для разделения тестов
            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
