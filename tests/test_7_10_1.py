# 7_10_1 тест для задачи
import importlib.util
import inspect
import sys

from io import StringIO


def test_7_10_1(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие замыкания)"""

    # Сохраняем оригинальные потоки ввода/вывода
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    # Подменяем stdin на фейковый с тестовыми данными
    sys.stdin = StringIO("0")
    sys.stdout = StringIO()

    result = []  # Список для накопления результатов тестов

    try:
        result.append(f"-------------Тест structure ------------")

        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Восстанавливаем потоки
        sys.stdin = original_stdin
        sys.stdout = original_stdout

        # Проверка наличия функции counter_add
        if not hasattr(user_module, "counter_add"):
            raise AttributeError("ОШИБКА: Функция 'counter_add' не найдена")

        # Получаем функцию из модуля
        counter_add = getattr(user_module, "counter_add")

        # Проверка, что функция объявлена строго как сказано в задаче -def counter_add(): (без аргументов)
        sig = inspect.signature(counter_add)
        params = sig.parameters
        if len(params) > 0:
            raise ValueError(f"ОШИБКА: Функция 'counter_add' не должна принимать аргументы.")

        # Проверяем что это функция (вызываемая - callable)
        if not callable(counter_add):
            raise TypeError("ОШИБКА: 'counter_add' должна быть функцией")

        # Вызываем counter_add и проверяем, что возвращается функция
        inner_func = counter_add()
        if not callable(inner_func):
            raise TypeError("ОШИБКА: 'counter_add' должна возвращать функцию (вложенную)")

        # Проверка на замыкание
        if inner_func.__closure__ is None:
            raise ValueError("ОШИБКА: Возвращённая функция не является замыканием")

        result.append("Найдена функция 'counter_add'")
        result.append("Функция возвращает другую функцию")
        result.append("Замыкание определено корректно")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_10_1_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        # Восстанавливаем потоки в случае ошибки
        sys.stdin = original_stdin
        sys.stdout = original_stdout
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_10_1_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "7",
        "-3",
        "0",
    )
    # Ожидаемый результат
    expected_output = (
        "12",
        "2",
        "5",
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
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
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

            # Получаем перехваченный вывод из print()
            captured_output = output_buffer.getvalue().rstrip()

            # Получаем функцию (cnt)
            cnt = getattr(user_module, 'cnt', None)
            # Получаем результат работы функции при прямом обращении
            answ = cnt(int(test_input[i]))

            # Проверяем результат перехваченного вывода and результат работы функции при прямом обращении
            if captured_output == expected_output[i] and answ == int(expected_output[i]):
                test_result.append(f"Получено:\n{captured_output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
