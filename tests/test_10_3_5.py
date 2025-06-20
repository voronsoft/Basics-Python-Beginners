# 10_3_5 тест для задачи
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_10_3_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Считываем код из временного файла
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code, allowed_imports=["sys"], allowed_calls=["sys.stdin.readlines"])

        # Упрощённая проверка
        if "shuffle" not in code:
            raise RuntimeError("ОШИБКА: В коде не найдена функция - shuffle()")

        result.append("Найдена функция - shuffle(), отлично.")

        if "zip" not in code:
            raise RuntimeError("ОШИБКА: В коде не найдена функция - zip()")

        result.append("Найдена функция - zip(), отлично.")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_10_3_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_10_3_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "1 2 3 4\n5 6 7 8\n9 8 6 7",
        "4 5 6 3 5 6\n5 4 3 2 0 1\n1 2 3 4 5 6\n0 3 2 4 5 6",
    )

    # Ожидаемые данные вывода
    expected_output = (
        "4 1 3 2\n8 5 7 6\n7 9 6 8",
        "6 3 6 4 5 5\n3 2 1 5 0 4\n3 4 6 1 5 2\n2 4 6 0 5 3",
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
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            # Проверка формирования списка
            if captured_output == expected_output[i]:
                test_result.append(f"Получено:\n{captured_output}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получено:\n{captured_output}"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
