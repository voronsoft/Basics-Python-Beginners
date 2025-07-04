# 7_10_4 тест для задачи
import importlib.util
import inspect

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_10_4(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие корректного замыкания)"""

    result = []

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
        with stream_interceptor(stdin_data="div\nПроверка", capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Получаем перехваченный вывод из stdout
        captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

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
        test_input = "текст"
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
            res = test_7_10_4_1(path_tmp_file, outer_func)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_10_4_1(path_tmp_file: str, outer_func):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "div\nСергей Балакирев",
        "p\nHello Python",
        "span\nHello Python",
    )
    # Ожидаемый результат
    expected_output = (
        "<div>Сергей Балакирев</div>",
        "<p>Hello Python</p>",
        "<span>Hello Python</span>",
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
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Проверяем прямой запуск функции
            tag, string = test_input[i].split("\n")  # Готовим тестовые данные для передачи в функции
            inn_fnc = outer_func(tag)
            # Получаем результат
            answer = inn_fnc(string)

            # Проверяем результат перехваченного вывода и то что возвращает функция при прямом обращении
            if captured_output == expected_output[i] and answer == expected_output[i]:
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
