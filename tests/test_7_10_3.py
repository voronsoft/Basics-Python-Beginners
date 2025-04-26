# 7_10_3 тест для задачи
import importlib.util
import inspect
import sys

from io import StringIO


def test_7_10_3(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие корректного замыкания)"""

    original_stdin = sys.stdin
    original_stdout = sys.stdout
    sys.stdin = StringIO("test")
    sys.stdout = StringIO()

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Восстанавливаем потоки
        sys.stdin = original_stdin
        sys.stdout = original_stdout

        outer_func = None

        # Поиск внешней функции без параметров
        for name in dir(user_module):
            obj = getattr(user_module, name)
            if callable(obj) and inspect.isfunction(obj):
                sig = inspect.signature(obj)
                if len(sig.parameters) == 0:
                    outer_func = obj
                    break
                else:
                    raise ValueError(f"ОШИБКА: Внешняя функция '{name}' не должна принимать параметры")

        if outer_func is None:
            raise ValueError("ОШИБКА: Внешняя функция не найдена")

        result.append(f"Найдена внешняя функция: {outer_func.__name__}")

        # Вызываем внешнюю функцию
        inner_func = outer_func()
        if not callable(inner_func):
            raise TypeError("ОШИБКА: Внешняя функция должна возвращать другую функцию")

        result.append("Внешняя функция возвращает вложенную функцию")

        # Проверяем, что вложенная функция использует замыкание
        closure = inner_func.__closure__
        if closure is None:
            raise ValueError(
                "ОШИБКА: Вложенная функция не использует переменные из внешней функции (не является замыканием)"
            )

        result.append("Замыкание используется корректно.")

        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_10_3_1(path_tmp_file, inner_func)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        sys.stdin = original_stdin
        sys.stdout = original_stdout
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_10_3_1(path_tmp_file: str, inner_func):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Balakirev",
        "Sergey",
        "Hello Python!",
        "У тебя получилось, молодец",
    )
    # Ожидаемый результат
    expected_output = (
        "<h1>Balakirev</h1>",
        "<h1>Sergey</h1>",
        "<h1>Hello Python!</h1>",
        "<h1>У тебя получилось, молодец</h1>",
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

            # Получаем перехваченный вывод из print()
            captured_output = output_buffer.getvalue().rstrip()

            # Получаем результат работы функции при прямом обращении
            answ = inner_func(test_input[i])

            # Проверяем результат перехваченного вывода and результат работы функции при прямом обращении
            if captured_output == expected_output[i] and answ == expected_output[i]:
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
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
