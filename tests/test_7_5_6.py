# 7_5_6 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_7_5_6(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода:
    - Проверка наличия функции str_min
    - Проверка наличия функции str_min3
    - Проверка наличия функции str_min4
    - Проверка типов атрибутов
    """

    result = []  # Список для накопления результатов тестов

    try:
        result.append(f"-------------Тест structure ------------")

        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Читаем исходный код для анализа AST
        with open(path_tmp_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        tree = ast.parse(source_code)

        # Проверяем что есть необходимые атрибуты в коде пользователя
        attr_search = {"str_min": "function", "str_min3": "function", "str_min4": "function"}

        for item, expected_type in attr_search.items():
            if not hasattr(user_module, item):
                raise AttributeError(f"ОШИБКА '{item}' не найден(а) в коде пользователя")
            else:
                # Получаем сам атрибут
                attr = getattr(user_module, item)
                # Получаем его тип
                attr_type = type(attr).__name__

                # Проверяем тип
                if expected_type == "function":
                    # Для функций проверяем, является ли атрибут вызываемым
                    if not callable(attr):
                        raise TypeError(f"ОШИБКА: '{item}' найден, но не является функцией (тип: {attr_type})")
                    result.append(f"Найдено: '{item}' (тип: {attr_type})")
                else:
                    # Для других типов проверяем соответствие
                    if attr_type != expected_type:
                        raise TypeError(
                            f"ОШИБКА: '{item}' имеет неверный тип. Ожидается {expected_type}, получен {attr_type}"
                        )
                    result.append(f"Найдено: '{item}' (тип: {attr_type})")

        # Проверяем использование str_min в str_min3 и str_min4 через AST
        str_min3_uses_str_min = False
        str_min4_uses_str_min = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == 'str_min3':
                    for subnode in ast.walk(node):
                        if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Name):
                            if subnode.func.id == 'str_min':
                                str_min3_uses_str_min = True
                elif node.name == 'str_min4':
                    for subnode in ast.walk(node):
                        if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Name):
                            if subnode.func.id == 'str_min':
                                str_min4_uses_str_min = True

        if not str_min3_uses_str_min:
            raise ValueError("ОШИБКА: функция str_min3 не использует str_min")
        if not str_min4_uses_str_min:
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

    # Сохраняем оригинальные потоки ввода/вывода
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    sys.stderr = StringIO()
    # Перенаправляем stdout, чтобы не засорять вывод тестов
    sys.stdout = StringIO()

    result = []  # Список для накопления результатов тестов

    try:
        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

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
    finally:
        # Восстанавливаем потоки в исходное состояние
        sys.stdin = original_stdin
        sys.stdout = original_stdout
