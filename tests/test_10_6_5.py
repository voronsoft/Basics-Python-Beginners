# 10_6_5 тест для задачи
import importlib.util
import sys

from io import StringIO


def test_10_6_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

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
            res = test_10_6_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_10_6_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""

    # Входные данные
    test_input = (
        {'id': 2, 'access': True, 'data': ['26.05.2023', {'login': '1234', 'email': 'xxx@mail.com'}, 2000, 56.4]},
        {'id': 3, 'access': True, 'data': ['01.01.2022', {'login': 'admin', 'email': 'admin@example.com'}, 0, 0]},
        {'id': 4, 'access': False, 'data': ['x', {'login': 'guest', 'email': 'guest@net'}, 1, 2]},
        {'id': 5, 'access': True, 'data': ['x', {'login': 1234, 'email': 'bad@mail.com'}, 1, 2]},
        {'id': 6, 'access': True, 'data': ['x', {'login': 'yes', 'email': None}, 1, 2]},
        {'id': 7, 'access': True, 'data': ['x', {'email': 'no_login@mail.com'}, 1, 2]},
    )

    # Ожидаемые данные вывода
    expected_output = (
        ('1234', 'xxx@mail.com'),
        ('admin', 'admin@example.com'),
        (4, 'guest'),
        (5, 1234),
        (6, 'yes'),
        None,
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
            sys.stdin = StringIO("")

            # Создаем буфер для перехвата вывода
            output_buffer = StringIO()

            # Перенаправляем stdout в буфер
            sys.stdout = output_buffer

            # Выполняем пользовательский модуль
            spec.loader.exec_module(user_module)

            # Получаем перехваченный вывод из print()
            captured_output = output_buffer.getvalue().strip()

            # Возвращаем stdout в исходное состояние
            sys.stdout = original_stdout

            # Получаем функцию parse_json из модуля
            parse_json = getattr(user_module, "parse_json")
            # Выполняем функцию с соответствующим словарем
            answer = parse_json(test_input[i])

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            if answer == expected_output[i]:
                test_result.append(f"Получено: {answer}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Вход:\n{test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {answer}"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
