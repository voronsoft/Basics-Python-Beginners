# 10_2_2 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_10_2_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Разбор кода в дерево AST
        tree = ast.parse(code)

        found_bitwise_or = False
        valid_mask_used = False
        var_values = {}

        # Сначала сохраняем переменные, в которых записаны значения маски
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                # Пример: mask = 0b1000
                if (
                    isinstance(node.targets[0], ast.Name)
                    and isinstance(node.value, ast.Constant)
                    and node.value.value in (8, 0b1000)
                ):
                    var_values[node.targets[0].id] = True

                # Пример: b = 1 << 3
                if (
                    isinstance(node.targets[0], ast.Name)
                    and isinstance(node.value, ast.BinOp)
                    and isinstance(node.value.op, ast.LShift)
                    and isinstance(node.value.left, ast.Constant)
                    and node.value.left.value == 1
                    and isinstance(node.value.right, ast.Constant)
                    and node.value.right.value == 3
                ):
                    var_values[node.targets[0].id] = True

        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
                found_bitwise_or = True

                # Прямое значение: 8 или 0b1000
                if isinstance(node.right, ast.Constant) and node.right.value in (8, 0b1000):
                    valid_mask_used = True

                # Сдвиг: 1 << 3
                if (
                    isinstance(node.right, ast.BinOp)
                    and isinstance(node.right.op, ast.LShift)
                    and isinstance(node.right.left, ast.Constant)
                    and node.right.left.value == 1
                    and isinstance(node.right.right, ast.Constant)
                    and node.right.right.value == 3
                ):
                    valid_mask_used = True

                # Переменная, в которую ранее было записано 8, 0b1000 или 1 << 3
                if isinstance(node.right, ast.Name):
                    if node.right.id in var_values:
                        valid_mask_used = True

        if not found_bitwise_or:
            raise RuntimeError("ОШИБКА: Не найдена операция побитового ИЛИ (|)")

        if not valid_mask_used:
            raise RuntimeError("ОШИБКА: Побитовая операция ИЛИ (|) используется не с маской 8 (0b1000 или 1 << 3)")

        result.append("Найдена операция побитового ИЛИ (|)")
        result.append("Маска задана корректно (8 / 0b1000 / 1 << 3 / переменная)")
        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_10_2_2_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_10_2_2_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "100",
        "22",
        "8",
    )

    # Ожидаемые данные вывода
    expected_output = (
        "108",
        "30",
        "8",
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
