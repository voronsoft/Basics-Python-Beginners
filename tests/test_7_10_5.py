# 7_10_5 тест для задачи
import importlib.util
import inspect
import sys

from io import StringIO


def test_7_10_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие корректного замыкания)"""

    original_stdin = sys.stdin
    original_stdout = sys.stdout
    sys.stdin = StringIO("list\n-5 6 8 11 0 111 -456 3")
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

        # Поиск внешней функции с 1 параметром.
        for name in dir(user_module):
            obj = getattr(user_module, name)
            if inspect.isfunction(obj) and obj.__module__ == "user_module":
                sig = inspect.signature(obj)
                if len(sig.parameters) == 1:
                    try:
                        result_func = obj("тест")  # пробуем вызвать
                        if callable(result_func):
                            outer_func = obj
                            break  # нашли подходящую
                    except Exception:
                        continue  # пропускаем, если вызов невозможен

        if outer_func is None:
            raise ValueError("ОШИБКА: Внешняя функция не найдена или ошибка в параметрах (принимать 1 параметр")

        result.append(f"Найдена внешняя функция: {outer_func.__name__} принимает параметр")

        # Вызываем внешнюю функцию
        inner_func = outer_func("h1")
        if not callable(inner_func):
            raise TypeError("ОШИБКА: Внешняя функция должна возвращать другую функцию")

        result.append("Внешняя функция возвращает вложенную функцию")

        # Проверка, что внутренняя функция принимает 1 параметр
        sig_inner = inspect.signature(inner_func)
        if len(sig_inner.parameters) != 1:
            raise ValueError("ОШИБКА: Вложенная функция должна принимать 1 параметр")

        result.append("Вложенная функция принимает 1 параметр")

        # Проверка, что внутренняя функция возвращает, а не выводит результат в консоль
        test_input = "-5 6 8 11 0 111 -456 3"
        returned = inner_func(test_input)

        if not isinstance(returned, str) and returned is None:
            raise TypeError("ОШИБКА: Вложенная функция должна возвращать строку, а не None")

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
            res = test_7_10_5_1(path_tmp_file, outer_func)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        sys.stdin = original_stdin
        sys.stdout = original_stdout
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_10_5_1(path_tmp_file: str, outer_func):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "list\n-5 6 8 11 0 111 -456 3",
        "tuple\n4 5 6 7 3 -5 6 -7",
        "list\n1 2 3",
    )
    # Ожидаемый результат
    expected_output = (
        "[-5, 6, 8, 11, 0, 111, -456, 3]",
        "(4, 5, 6, 7, 3, -5, 6, -7)",
        "[1, 2, 3]",
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
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

            # Получаем перехваченный вывод из print()
            captured_output = output_buffer.getvalue().rstrip()

            # Проверяем прямой запуск функции
            tp, int_string = test_input[i].split("\n")  # Готовим тестовые данные для передачи в функции
            inn_fnc = outer_func(tp)
            # Получаем результат
            answ = inn_fnc(int_string)
            print(333, answ)
            # Проверяем результат перехваченного вывода и то что возвращает функция при прямом обращении
            if captured_output == expected_output[i]:  # and answ == expected_output[i]:
                test_result.append(f"Получено: {captured_output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
