# 8_6_2 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_8_6_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Парсим код в AST-дерево
        tree = ast.parse(code)

        # Проходим по всем узлам дерева
        has_try_except = any(isinstance(node, ast.Try) for node in ast.walk(tree))

        if has_try_except:
            result.append("Блок найден: try/except")
            result.append("--------------OK structure -------------\n")
        else:
            raise ValueError("ОШИБКА: Не найден блок в коде: try/except")

        # Дополнительно — тест выполнения кода
        try:
            res = test_8_6_2_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_8_6_2_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""

    # Ожидаемый результат
    expected_output = 'File Not Found'

    result = []  # Список для накопления результатов тестов

    try:
        # Импортируем модуль пользователя
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data=" ", capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Получаем перехваченный вывод из stdout
        captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

        # Проверяем результат
        test_result = list()
        test_result.append(f"---------------OK Тест --------------")
        test_result.append(f"Ожидалось: {expected_output}")

        # Проверяем результат перехваченного вывода
        if captured_output == expected_output:
            test_result.append(f"Получено: {captured_output}\n")
        else:
            raise ValueError(
                f"------------- FAIL Тест --------\n" f"Ожидалось: {expected_output}\nно получен: {captured_output}\n"
            )

        result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
