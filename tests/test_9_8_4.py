# 9_8_4 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_9_8_4(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Разбор в AST
        tree = ast.parse(code)

        func_found = False
        isinstance_used = False

        for node in ast.walk(tree):
            # Поиск определения функции get_even_sum с аргументами
            if isinstance(node, ast.FunctionDef):
                if node.name == "get_even_sum" and len(node.args.args) == 1:
                    func_found = True

            # Поиск вызова isinstance(...)
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "isinstance":
                    isinstance_used = True

        if not func_found:
            raise RuntimeError("ОШИБКА: В коде не найдена функция get_even_sum(it)")

        result.append("Найдена функция get_even_sum(it)")

        if not isinstance_used:
            raise RuntimeError("ОШИБКА: В коде не найден вызов функции isinstance")

        result.append("Найден вызов функции isinstance")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_9_8_4_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_8_4_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        [1, 2, 3, "a", True, 4, -5, "c", -4, 5],
        {5, 6, 7, '8', 12, '-4'},
        (10, "f", '33', True, 12),
        ['1', True, False, 2.01, 2.01],
    )

    # Ожидаемые данные вывода
    expected_output = (
        2,
        18,
        22,
        0,
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
            # Заглушка для sys.stderr
            original_stderr = sys.stderr  # сохраняем оригинал
            sys.stderr = StringIO()  # подменяем на буфер

            # Выполняем пользовательский модуль
            spec.loader.exec_module(user_module)

            # Получаем из модуля get_even_sum
            get_even_sum = getattr(user_module, "get_even_sum")
            # Выполняем
            answer = get_even_sum(test_input[i])
            print("lst", answer)

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
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
