# 10_3_7 тест для задачи
import importlib.util
import sys

from io import StringIO


def test_10_3_7(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

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

    import importlib.util
    import sys

    from io import StringIO

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

            original_stdin = sys.stdin
            original_stdout = sys.stdout

            # Подменяем stdin с тестовыми данными
            sys.stdin = StringIO(test_input[i])

            # Создаем буфер для перехвата вывода
            output_buffer = StringIO()
            sys.stdout = output_buffer

            # Удаляем модуль из кэша, при повторном импорте
            if "user_module" in sys.modules:
                del sys.modules["user_module"]

            # Выполняем пользовательский модуль
            spec.loader.exec_module(user_module)

            # Возвращаем stdout и stdin обратно
            sys.stdout = original_stdout
            sys.stdin = original_stdin

            # Получаем переменную P из модуля
            P = getattr(user_module, "P")

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")

            # Проверка правильности поля
            ok, message = check_field(P, M = 10)
            if ok:
                test_result.append(f"Правильное решение !! {message}\n")
            else:
                raise RuntimeError(f"------------- FAIL Тест: {i + 1} --------\n" f"Ошибка: {message}")

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")


def check_field(P, M = 10):
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

    print(count_ones, repr(count_ones))
    print(M, repr(M))
    if count_ones != M:
        return False, f"Ожидалось {M} единиц, но найдено: {count_ones}"

    return True, "Расстановка корректна"
