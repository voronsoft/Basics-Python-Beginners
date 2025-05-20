# 7_7_8 тест для задачи
import ast
import importlib.util
import subprocess
import sys

from io import StringIO


def test_7_7_8(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    # Сохраняем оригинальные потоки ввода/вывода
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    # Подменяем stdin на фейковый с тестовыми данными
    test_input = "8 11 -6 3 0 1 1"
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

        # Получаем исходный код файла пользователя
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        # Список всех функций
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        if not functions:
            raise AttributeError("ОШИБКА: В коде не найдены функции")

        recursive_functions = []

        for func in functions:
            func_name = func.name
            is_recursive = False

            # Проверка: есть ли в теле функции вызов самой себя (проверка на рекурсивный вызов)
            for node in ast.walk(func):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id == func_name:
                        is_recursive = True
                        break

            if is_recursive:
                result.append(f"Функция '{func_name}': recursive")
                recursive_functions.append(func_name)
            else:
                result.append(f"Функция '{func_name}' — не рекурсивная (допустимо)")

        if not recursive_functions:
            raise TypeError("ОШИБКА: не найдены рекурсивные функции")

        result.append(f"--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_7_8_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_7_8_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "8 11 -6 3 0 1 1",
        "5 3 3 6 8 5 3 -10 343 53 7",
        "1 -1",
        "-10 -16 -10 -1 0 1 16 10 1",
    )

    # Ожидаемый результат
    expected_output = (
        "-6 0 1 1 3 8 11",
        "-10 3 3 3 5 5 6 7 8 53 343",
        "-1 1",
        "-16 -10 -10 -1 0 1 1 10 16",
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
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Сравниваем результат с ожидаемым значением
            if output == expected_output[i]:
                test_result.append(f"Получено: {output}\n")

            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
