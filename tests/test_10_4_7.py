# 10_4_7 тест для задачи
import importlib.util
import sys

from io import StringIO


def test_10_4_7(path_tmp_file: str, task_num_test: str):
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

        if "def get_data(value):" not in code:
            raise RuntimeError("ОШИБКА: В коде не найдена функция - get_data")

        result.append("Найдена функция - get_data, отлично.")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_10_4_7_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_10_4_7_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        0,
        1,
        -100.0,
        -101.0,
        100.0,
        101.0,
        "string",
        [],
        {}
    )

    # Ожидаемые данные вывода
    expected_output = (
        None,
        1,
        -100.0,
        None,
        100.0,
        None,
        "string",
        None,
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

            # Получаем функцию get_data из модуля
            get_data = getattr(user_module, "get_data")
            # Выполняем функцию
            answer = get_data(test_input[i])

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

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
