# 10_3_7 тест для задачи
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_10_3_7(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Считываем код из временного файла
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Упрощённая проверка
        if "N = int(input())" not in code:
            raise RuntimeError("ОШИБКА: Переменные P и N не менять, единицы записывать в список P")

        result.append("Найдена функция - sample(), отлично.")

        if "P = [[0] * N for i in range(N)]" not in code:
            raise RuntimeError("ОШИБКА: Переменные P и N не менять, единицы записывать в список P")

        result.append("Найдена функция - sample(), отлично.")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_10_3_7_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_10_3_7_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""

    # Входные данные
    test_input = (
        "10",
        "7",
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

            # Получаем переменную P из модуля
            P = getattr(user_module, "P")

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")

            # Проверка правильности поля
            ok, message = check_field(P, M=10)
            if ok:
                test_result.append(f"Правильное решение !! {message}\n")
            else:
                raise RuntimeError(f"------------- FAIL Тест: {i + 1} --------\n" f"Ошибка: {message}")

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")


def check_field(P, M=10):
    """Проверка:
    - Ровно M единиц;
    - Единицы не касаются друг друга (в т.ч. по диагонали).
    """
    N = len(P)
    count_ones = 0

    for i in range(N):
        for j in range(N):
            if P[i][j] == 1:
                count_ones += 1
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < N and 0 <= nj < N and P[ni][nj] == 1:
                            return False, f"Единицы касаются: ({i},{j}) и ({ni},{nj})"

    if count_ones != M:
        return False, f"Ожидалось {M} единиц, но найдено: {count_ones}"

    return True, "Расстановка корректна"
