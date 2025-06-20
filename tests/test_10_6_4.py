# 10_6_4 тест для задачи
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_10_6_4(path_tmp_file: str, task_num_test: str):
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

        if "def parse_json(data)" not in code:
            raise RuntimeError("ОШИБКА: В коде не найдена функция - parse_json")

        result.append("Найдена функция - parse_json(data), отлично.")

        if "json_data" not in code:
            raise RuntimeError("ОШИБКА: В коде не найден словарь - json_data")

        result.append("Найден словарь - json_data, отлично.")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_10_6_4_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_10_6_4_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""

    # Входные данные
    test_input = (
        {'access': True, 'data': ['01.01.2024']},
        {'access': False, 'data': ['15.03.2025', {}, 1]},
        {'id': 10, 'data': ['xx', {'login': 'root'}, 1, 2]},
        {'id': 1, 'data': ['12.12.2022', {'email': 'admin@mail.com'}, 0, 0]},
        {'access': 'yes', 'data': ['05.05.2023']},
        {'access': True, 'data': '05.05.2023'},
        {'id': 7, 'data': ['22.04.2023', {'login': 'user7'}, 5, 3], 'access': False},
        {'data': [1, 2, 3]},
    )

    # Ожидаемые данные вывода
    expected_output = (
        (True, '01.01.2024'),
        (False, '15.03.2025'),
        (10, 'root'),
        None,
        None,
        None,
        (False, '22.04.2023'),  # приоритет шаблона с access
        None,
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=" ", capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем перехваченный вывод из stdout
            captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Получаем функцию parse_json из модуля
            parse_json = getattr(user_module, "parse_json")
            # Выполняем функцию
            answer = parse_json(test_input[i])

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Вход: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            if answer == expected_output[i]:
                test_result.append(f"Получено: {answer}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Вход: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {answer}"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
