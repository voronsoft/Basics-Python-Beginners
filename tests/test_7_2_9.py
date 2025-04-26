# 7_2_9 тест для задачи
import importlib.util
import io
import sys
from contextlib import redirect_stdout


def test_7_2_9(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные и ожидаемые результаты (точно как у вас)
    test_input = (
        "56 34 -30 22 1 4 10",
        "100 80 70 50 22",
    )
    expected_output = (
        "-1680",
        "2200",
    )

    result = []  # Список для накопления результатов тестов

    # Настройка модуля
    spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
    user_module = importlib.util.module_from_spec(spec)
    sys.modules["user_module"] = user_module

    try:
        for i in range(len(test_input)):
            test_result = [
                f"---------------OK Тест: {i + 1} --------------",
                f"Входные данные: {test_input[i]}",
                f"Ожидалось: {expected_output[i]}",
            ]

            # Имитируем ввод и выполняем код, перехватывая вывод
            sys.stdin = io.StringIO(test_input[i])
            output_io = io.StringIO()
            with redirect_stdout(output_io):
                spec.loader.exec_module(user_module)

            # Проверяем наличие списка digs
            if not hasattr(user_module, "digs"):
                raise ValueError(f"------------- FAIL Тест {i + 1} --------\nСписок 'digs' не найден")

            # Получаем вывод из консоли
            output = output_io.getvalue().strip()
            test_result.append(f"Получено: {output}")

            # Сравниваем результат с ожидаемым значением
            if output != expected_output[i]:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\n"
                    f"Получено: {output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)
    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
    finally:
        sys.stdin = sys.__stdin__