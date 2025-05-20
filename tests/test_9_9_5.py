# 9_9_5 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_9_9_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Разбор в AST
        tree = ast.parse(code)

        func_found = True
        any_all_used = False

        for node in ast.walk(tree):
            # Поиск определения функции is_free с аргументами
            if isinstance(node, ast.FunctionDef):
                if node.name == "is_free" and len(node.args.args) == 1:
                    func_found = True

            if isinstance(node, ast.Call):
                # Поиск вызова any(...)
                if isinstance(node.func, ast.Name) and node.func.id == "any":
                    any_all_used = True
                # Поиск вызова all(...)
                elif isinstance(node.func, ast.Name) and node.func.id == "all":
                    any_all_used = True

        if not func_found:
            raise RuntimeError("ОШИБКА: В коде не найдена функция is_free(..)")

        result.append("Найдена функция is_free(..)")

        if not any_all_used:
            raise RuntimeError("ОШИБКА: В коде не найдена функция any/all")

        result.append("Найдена функция all/any")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_9_9_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_9_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "# x o\nx # x\no o #",
        "o x o\nx x x\no o x",
        "x # o\nx o x\nx x o",
    )

    # Ожидаемые данные вывода
    expected_output = (
        True,
        False,
        True,
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            original_stdin = sys.stdin

            # Подменяем stdin (заглушка)
            sys.stdin = StringIO('')

            # Выполняем пользовательский модуль
            spec.loader.exec_module(user_module)

            # Получаем из модуля is_free
            is_free = getattr(user_module, "is_free")
            # Выполняем
            answer = is_free(test_input[i])

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Проверка формирования списка
            if answer == expected_output[i]:
                test_result.append(f"Получено: {answer}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {answer}"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
