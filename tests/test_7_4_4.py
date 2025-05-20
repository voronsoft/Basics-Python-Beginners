# 7_4_4 тест для задачи
import importlib.util
import inspect
import os
import subprocess
import sys

from io import StringIO


def test_7_4_4(path_tmp_file: str, task_num_test: str):
    """Тестирование функции transliterate:
    - Проверка наличия функции transliterate
    - Проверка параметра sep
    - Проверка значения параметра sep по умолчанию
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
        sys.stdin = StringIO(" ")
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

        # Проверяем, что функция transliterate присутствует
        if not hasattr(user_module, "transliterate"):
            raise AttributeError("ОШИБКА функция 'transliterate' не найдена в коде пользователя")
        else:
            result.append("Найдено: 'transliterate'")

        func = user_module.transliterate

        # --- Проверка параметров функции ---
        sig = inspect.signature(func)
        params = sig.parameters

        # Проверяем наличие параметра 'sep'
        if "sep" not in params:
            raise ValueError("ОШИБКА параметр 'sep' не найден среди параметров функции")
        else:
            result.append("Найдено: 'sep'")

        # Проверяем значение по умолчанию параметра 'sep'
        if params["sep"].default != "-":
            raise ValueError("ОШИБКА параметр 'sep' должен иметь значение по умолчанию '-'")
        else:
            result.append("Найдено: sep='-'")

        result.append("")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_4_4_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_4_4_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Лучший курс по Python!",
        "Я люблю Python",
        "Это очень круто",
    )
    # Ожидаемый результат
    expected_output = (
        "luchshiy-kurs-po-python!\nluchshiy+kurs+po+python!",
        "ya-lyublyu-python\nya+lyublyu+python",
        "eto-ochen-kruto\neto+ochen+kruto",
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
