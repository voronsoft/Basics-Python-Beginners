# 2_3_1 тест для задачи
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_2_3_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = ("-5\n", "-6\n", "3\n")
    # Ожидаемый результат
    expected_output = ("5", "6", "3")

    result = []  # Список для накопления результатов тестов

    try:
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()
        check_code_safety(user_code)

        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=test_input[i], capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля
                # Получаем перехваченный вывод из stdout
                captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Сравниваем результат с ожидаемым значением
            if captured_output == expected_output[i]:
                test_result.append(f"Получено: {captured_output}\n")

            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} -------------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {captured_output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
