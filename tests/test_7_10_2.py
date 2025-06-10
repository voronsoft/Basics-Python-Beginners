# 7_10_2 тест для задачи
import importlib.util
import inspect

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_10_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие замыкания)"""

    result = []  # Список для накопления результатов тестов

    try:
        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(user_code)

        result.append(f"-------------Тест structure ------------")

        # Импортируем модуль пользователя
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data="0", capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Получаем перехваченный вывод из stdout
        captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

        # Проверка наличия функции counter_add
        if not hasattr(user_module, "counter_add"):
            raise AttributeError("ОШИБКА: Функция 'counter_add' не найдена")

        # Получаем функцию из модуля
        counter_add = getattr(user_module, "counter_add")

        # Проверка, что функция объявлена строго как сказано в задаче -def counter_add(): (c аргументоm)
        sig = inspect.signature(counter_add)
        params = sig.parameters
        if len(params) != 1:
            raise ValueError(f"ОШИБКА: Функция 'counter_add' должна принимать 1 аргумент.")

        # Проверяем что это функция (вызываемая - callable)
        if not callable(counter_add):
            raise TypeError("ОШИБКА: 'counter_add' должна быть функцией")

        # Вызываем counter_add и проверяем, что возвращается функция
        inner_func = counter_add(None)
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
            res = test_7_10_2_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")


def test_7_10_2_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "5",
        "0",
        "-2",
        "-4",
    )
    # Ожидаемый результат
    expected_output = (
        "7",
        "2",
        "0",
        "-2",
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

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Получаем функцию cnt из модуля пользователя
            counter_add = getattr(user_module, 'counter_add')
            # Получаем результат работы функции при прямом обращении
            func = counter_add(2)
            cnt = func(int(test_input[i]))

            # Проверяем результат перехваченного вывода and результат работы функции при прямом обращении
            if captured_output == expected_output[i] and cnt == int(expected_output[i]):
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
