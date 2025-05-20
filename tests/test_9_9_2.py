# 9_9_2 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_9_9_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Разбор в AST
        tree = ast.parse(code)

        any_all_used = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Поиск вызова any(...)
                if isinstance(node.func, ast.Name) and node.func.id == "any":
                    any_all_used = True
                # Поиск вызова all(...)
                elif isinstance(node.func, ast.Name) and node.func.id == "all":
                    any_all_used = True

        if not any_all_used:
            raise RuntimeError("ОШИБКА: В коде не найдена функция any/all")

        result.append("Найдена функция all/any")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_9_9_2_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_9_2_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "8.2 -11.0 20 3.4 -1.2",
        "2.3 4.2 5.0 6.8 -7.12 8.8",
        "6.1 8.1 100.1 4.0",
    )

    # Ожидаемые данные вывода
    expected_output = (
        "True",
        "True",
        "False",
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

            # Возвращаем stdin в исходное состояние
            sys.stdout = original_stdout

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Проверка формирования списка
            if captured_output == expected_output[i]:
                test_result.append(f"Получено: {captured_output}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {captured_output}"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
