# 7_5_5 тест для задачи
import importlib.util
import sys
from io import StringIO


def test_7_5_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры"""

    # Сохраняем оригинальные потоки ввода/вывода
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    # Подменяем stdin на фейковый с тестовыми данными
    test_input = "1 0 0 0 0\n0 0 1 0 0\n0 0 0 0 0\n0 1 0 1 0\n0 0 0 0 0"
    sys.stdin = StringIO(test_input)

    # Перенаправляем stdout, чтобы не засорять вывод тестов
    sys.stdout = StringIO()

    result = []  # Список для накопления результатов тестов

    try:
        result.append(f"-------------Тест structure ------------")

        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
        # Восстанавливаем оригинальные потоки
        sys.stdin = original_stdin
        sys.stdout = original_stdout

        # Проверяем что есть необходимые атрибуты в коде пользователя
        attr_search = {"verify": "function", "is_isolate": "function", "lst2D": "list"}  # предполагаемый тип для lst2D

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

        result.append(f"--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_5_5_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_5_5_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        [
            [1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
        ],
        [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1],
            [0, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 1, 0],
            [0, 0, 0],
            [1, 0, 1],
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [[1, 0], [0, 1]],
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
        ],
        [
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
        ],
        [
            [1, 0, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
        ],
        [
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [1, 1, 0, 0],
        ],
    )
    # Ожидаемый результат
    expected_output = (
        True,
        False,
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    # Сохраняем оригинальные потоки ввода/вывода
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    # Подменяем stdin на фейковый с тестовыми данными
    fake_input = "1 0 0 0 0\n0 0 1 0 0\n0 0 0 0 0\n0 1 0 1 0\n0 0 0 0 0"
    sys.stdin = StringIO(fake_input)
    # Перенаправляем stdout, чтобы не засорять вывод тестов
    sys.stdout = StringIO()

    result = []  # Список для накопления результатов тестов

    try:
        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Проверяем работу атрибута lst2D (разово)
        # Импортируем lst2D из модуля
        lst2D = user_module.lst2D
        if lst2D != test_input[0]:
            raise AssertionError(f"lst2D сформирован неправильно:\nОжидалось: {test_input[0]}\nПолучено : {lst2D}")

        # Получаем verify функцию для работы с ней
        func = user_module.verify

        for i in range(len(test_input)):
            # Вызываем функцию, передавая данные
            output = func(test_input[i])

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Сравниваем результат с ожидаемым значением
            if output == expected_output[i]:
                test_result.append(f"Получено: {output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {output}\n"
                )

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
