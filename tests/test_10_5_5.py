# 10_5_5 тест для задачи
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_10_5_5(path_tmp_file: str, task_num_test: str):
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
        if "match" not in code:
            raise RuntimeError("ОШИБКА: В коде не найдено -  match")

        result.append("Найдена функция - match, отлично.")

        if "case" not in code:
            raise RuntimeError("ОШИБКА: В коде не найдено -  case")

        result.append("Найдена функция - case, отлично.")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_10_5_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_10_5_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "1, Балакирев С.М., Python, 2100.0, 2023",
        "2, Зингаро. Д, Python без проблем, 1000.0, 2019",
        "1, Балакирев С.М., Python, 0",
        "4",
        "5, Яв, Python. Лучшие практики и инструменты, 1500.1, 2021",
        "5, Яв, Python. Лучшие практики и инструменты",
        "5, Яворски Михаил, Python. Лучшие практики и инструменты",
    )

    # Ожидаемые данные вывода
    expected_output = (
        "Yes",
        "No",
        "No",
        "No",
        "Yes",
        "No",
        "Yes",
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
            test_result.append(f"Ожидалось: {expected_output[i]}")

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
