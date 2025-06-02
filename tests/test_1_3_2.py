# 1_3_2 тест для задачи
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_1_3_2(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    expected_output = "13"  # Ожидаемый результат
    result = []  # Список для накопления результатов тестов

    try:
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()
        check_code_safety(user_code)

        # Импортируем модуль пользователя
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data="", capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем перехваченный вывод из stdout
            captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

        # Формируем отчет по тесту
        test_result = []
        test_result.append(f"---------------OK Тест: --------------")
        test_result.append(f"Ожидалось: {expected_output}")

        if captured_output == expected_output:
            test_result.append(f"Получено: {captured_output}\n")
        else:
            raise ValueError(
                f"------------- FAIL Тест: --------\n"
                f"Ожидалось: {expected_output}\n"
                f"Получено: {captured_output}\n"
            )

        result.append("\n".join(test_result))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n{error_info}")
