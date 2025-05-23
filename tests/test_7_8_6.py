# 7_8_6 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_7_8_6(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    # Сохраняем оригинальные потоки ввода/вывода
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    # Подменяем stdin на фейковый с тестовыми данными
    test_input = "5 4 -3 4 5 -24 -6 9 0"
    sys.stdin = StringIO(test_input)
    # Заглушка для sys.stderr
    original_stderr = sys.stderr  # сохраняем оригинал
    sys.stderr = StringIO()  # подменяем на буфер
    # Перенаправляем stdout, чтобы не засорять вывод тестов
    sys.stdout = StringIO()

    result = []

    try:
        result.append(f"-------------Тест structure ------------")

        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
        # Восстановим стандартные потоки
        sys.stdin = original_stdin
        sys.stdout = original_stdout

        # Проверяем что есть необходимые атрибуты в коде пользователя
        if not hasattr(user_module, "digs"):
            raise AttributeError("ОШИБКА: переменная 'digs' не найдена в коде пользователя")

        # Читаем исходный код
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        lambda_found = any(isinstance(node, ast.Lambda) for node in ast.walk(tree))

        if not lambda_found:
            raise TypeError("ОШИБКА: в коде отсутствует использование лямбда-функции")

        result.append("В коде найдена лямбда-функция")
        result.append("--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_8_6_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_8_6_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "5 4 -3 4 5 -24 -6 9 0",
        "5 4 3 -1 0 -2",
        "-5 -4 -1 0 -2 5",
    )
    # Ожидаемый результат
    expected_output = (
        "5 4 -3 4 5 -24 -6 9 0\n-3 -24 -6\n5 4 4 5 9 0\n5 4 4 5",
        "5 4 3 -1 0 -2\n-1 -2\n5 4 3 0\n5 4 3",
        "-5 -4 -1 0 -2 5\n-5 -4 -1 -2\n0 5\n5",
    )

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
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

            # Получаем перехваченный вывод
            captured_output = output_buffer.getvalue().rstrip()

            print("captured_output", repr(captured_output), type(captured_output))
            print(f"expected_output[{i}]", repr(expected_output[i]), type(expected_output[i]))

            if captured_output == expected_output[i]:
                test_result.append(f"Получено: {captured_output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
