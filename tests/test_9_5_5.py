# 9_5_5 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_9_5_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Разбор кода в дерево AST
        tree = ast.parse(code)

        zip_used = False
        lst_used = False

        # Проход по дереву AST
        for node in ast.walk(tree):
            # Проверка на вызовы функций (zip(...))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == 'zip':
                    zip_used = True

            # Проверка на использование переменной lst
            if isinstance(node, ast.Name) and node.id == 'lst':
                lst_used = True

        # Сообщения, если чего-то не хватает
        if not zip_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции zip.")
        if not lst_used:
            raise ValueError("ОШИБКА: В коде не найден lst.")

        result.append("Найден вызов функции zip()")
        result.append("Найдена переменная lst")
        result.append("--------------OK structure -------------\n")

        # Выполнение функционального теста
        try:
            res = test_9_5_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_5_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Sergey Balakirev",
        "GUI wxPython",
    )

    # Ожидаемые данные вывода
    expected_output = (
        [('S', 0), ('e', 1), ('r', 2), ('g', 3), ('e', 4), ('y', 5), (' ', 6), ('B', 7), ('a', 8), ('l', 9)],
        [('G', 0), ('U', 1), ('I', 2), (' ', 3), ('w', 4), ('x', 5), ('P', 6), ('y', 7), ('t', 8), ('h', 9)],
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            original_stdin = sys.stdin
            original_stdout = sys.stdout

            # Подменяем stdin с тестовыми данными
            sys.stdin = StringIO(test_input[i])
            # Заглушка для sys.stderr
            original_stderr = sys.stderr  # сохраняем оригинал
            sys.stderr = StringIO()  # подменяем на буфер
            # Создаем буфер для перехвата вывода
            output_buffer = StringIO()

            # Перенаправляем stdout в буфер
            sys.stdout = output_buffer

            # Выполняем пользовательский модуль
            spec.loader.exec_module(user_module)

            # Получаем перехваченный вывод из print()
            captured_output = output_buffer.getvalue().strip()

            # Получаем список lst для проверки из модуля
            lst_user_code = getattr(user_module, "lst")

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            if lst_user_code == expected_output[i]:
                test_result.append(f"Получено:\n{lst_user_code}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получено:\n{lst_user_code}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
