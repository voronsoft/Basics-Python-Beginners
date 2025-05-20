# 7_4_6 тест для задачи
import importlib.util
import inspect
import os
import subprocess
import sys

from io import StringIO


def test_7_4_6(path_tmp_file: str, task_num_test: str):
    """Тестирование функции constructor:
    - Проверка наличия функции constructor
    - Проверка параметра tag
    - Проверка значения параметра tag по умолчанию
    """

    result = []  # Список для накопления результатов тестов

    try:
        result.append(f"-------------Тест structure ------------")

        # Проверяем существование файла
        if not os.path.exists(path_tmp_file):
            raise FileNotFoundError(f"Файл {path_tmp_file} не найден")

        # Сохраняем оригинальные потоки ввода/вывода
        original_stdin = sys.stdin
        original_stdout = sys.stdout

        # Подменяем stdin на фейковый с тестовыми данными
        test_input = "Работаем с функциями"
        sys.stdin = StringIO(test_input + "\n")
        # Заглушка для sys.stderr
        original_stderr = sys.stderr  # сохраняем оригинал
        sys.stderr = StringIO()  # подменяем на буфер

        # Перенаправляем stdout, чтобы не засорять вывод тестов
        sys.stdout = StringIO()

        try:
            # Загружаем пользовательский модуль
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(user_module)
        finally:
            # Восстанавливаем оригинальные потоки
            sys.stdin = original_stdin
            sys.stdout = original_stdout

        # Проверяем, что функция constructor присутствует
        if not hasattr(user_module, "constructor"):
            raise AttributeError("ОШИБКА функция 'constructor' не найдена в коде пользователя")
        else:
            result.append("Найдено: 'constructor'")

        func = user_module.constructor

        # --- Проверка параметров функции ---
        sig = inspect.signature(func)
        params = sig.parameters

        # --- Проверяем наличие параметра 'up'
        if "up" not in params:
            raise ValueError("ОШИБКА параметр 'up' не найден среди параметров функции")
        else:
            result.append("Найдено: 'up'")

        # Проверяем значение по умолчанию параметра 'up'
        if params["up"].default != True:
            raise ValueError("ОШИБКА параметр 'up' должен иметь значение по умолчанию 'True'")
        else:
            result.append("Найдено: up=True")

        # --- Проверяем наличие параметра 'tag'
        if "tag" not in params:
            raise ValueError("ОШИБКА параметр 'tag' не найден среди параметров функции")
        else:
            result.append("Найдено: 'tag'")

        result.append("")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_4_6_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_4_6_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Работаем с функциями",
        "Python is the best!",
    )
    # Ожидаемый результат
    expected_output = (
        "<DIV>Работаем с функциями</DIV>\n<div>Работаем с функциями</div>",
        "<DIV>Python is the best!</DIV>\n<div>Python is the best!</div>",
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Запускаем код пользователя, передавая ему входные данные через stdin
            process = subprocess.run(
                ["python", "-I", "-E", "-X", "utf8", path_tmp_file],  # Запускаем временный файл
                input=test_input[i],  # Передаём input
                text=True,  # Режим работы с текстом
                capture_output=True,  # Захватываем stdout и stderr
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                encoding="utf-8",  # Явно указываем кодировку
                timeout=5,  # Важно: ограничение времени выполнения кода
            )

            # Получаем результат (stdout)
            output = process.stdout.strip()
            # Получаем сообщения об ошибках
            error = process.stderr.strip()
            if error:  # Если есть ошибки в коде выводим
                raise ValueError(error)

            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            # Сравниваем результат с ожидаемым значением
            if output == expected_output[i]:
                test_result.append(f"Получено:\n{output}\n")

            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
