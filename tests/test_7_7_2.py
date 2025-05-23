# 7_7_2 тест для задачи
import ast
import importlib.util
import inspect
import sys

from io import StringIO


def test_7_7_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    # Сохраняем оригинальные потоки ввода/вывода
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    # Подменяем stdin на фейковый с тестовыми данными
    test_input = "55"
    sys.stdin = StringIO(test_input)
    # Заглушка для sys.stderr
    original_stderr = sys.stderr  # сохраняем оригинал
    sys.stderr = StringIO()  # подменяем на буфер

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
        attr_search = {
            "get_rec_N": "function",
            "N": "int",
        }

        for item, expected_type in attr_search.items():
            if not hasattr(user_module, item):
                raise AttributeError(f"ОШИБКА '{item}' не найден(а) в коде пользователя")
            if item in attr_search:
                # Получаем сам атрибут
                attr = getattr(user_module, item)
                # Получаем его тип
                attr_type = type(attr).__name__

                # Проверяем тип
                if attr_type == expected_type:
                    result.append(f"Найдено: '{item}' (тип: {attr_type})")
                else:
                    # Для других типов проверяем соответствие
                    if attr_type != expected_type:
                        raise TypeError(
                            f"ОШИБКА: '{item}' имеет неверный тип. Ожидается {expected_type}, получен {attr_type}"
                        )
                    result.append(f"Найдено: '{item}' (тип: {attr_type})")

                # ДОПОЛНЕНИЕ: Проверка рекурсивности функции get_rec_N
                if item == 'get_rec_N' and attr_type == 'function':
                    # Получаем исходный код функции
                    source = inspect.getsource(attr)
                    # Парсим в AST дерево
                    tree = ast.parse(source)
                    is_recursive = False

                    # Ищем рекурсивные вызовы в теле функции
                    for node in ast.walk(tree):
                        if (
                            isinstance(node, ast.Call)
                            and isinstance(node.func, ast.Name)
                            and node.func.id == 'get_rec_N'
                        ):
                            is_recursive = True
                            break

                    if is_recursive:
                        result.append(f"Функция 'get_rec_N': recursive")
                    else:
                        raise TypeError(f"ОШИБКА: '{item}' не является рекурсивной функцией")

        result.append(f"--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_7_2_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_7_2_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = ("8", "5", "3")
    # Ожидаемый результат
    expected_output = ("1\n2\n3\n4\n5\n6\n7\n8", "1\n2\n3\n4\n5", "1\n2\n3")

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Подменяем stdin с тестовыми данными
            sys.stdin = StringIO(test_input[i])
            # Заглушка для sys.stderr
            original_stderr = sys.stderr  # сохраняем оригинал
            sys.stderr = StringIO()  # подменяем на буфер

            spec.loader.exec_module(user_module)

            # Создаем буфер для перехвата вывода
            buffer = StringIO()
            # Сохраняем оригинальный stdout
            original_stdout = sys.stdout
            sys.stdout = buffer

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            # Получаем функцию get_rec_N из модуля пользователя
            user_func = getattr(user_module, 'get_rec_N')
            # Выполняем функцию
            user_func(int(test_input[i]))
            # Получаем вывод
            output = buffer.getvalue().strip()  # Удаляем лишние переносы строк

            if output == expected_output[i]:
                test_result.append(f"Получено:\n{output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{output}\n"
                )

            result.append("\n".join(test_result))
            # Всегда восстанавливаем stdout
            sys.stdout = original_stdout

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
