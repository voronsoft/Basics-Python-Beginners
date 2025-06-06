# 7_9_5 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_9_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(user_code)

        # Разбор в AST
        tree = ast.parse(user_code)

        func_found = False

        for node in ast.walk(tree):
            # Поиск определения функции create_global
            if isinstance(node, ast.FunctionDef):
                if node.name == "create_global":
                    func_found = True

        if not func_found:
            raise RuntimeError("ОШИБКА: В коде не найдена функция 'create_global'")

        result.append("Найдена функция 'create_global'")
        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_7_9_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_9_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = ("Сергей Балакирев", "Разработчик молодец", "77", "10")
    # Ожидаемый результат
    expected_output = ("Сергей Балакирев", "Разработчик молодец", "77", "10")

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

            # Получаем функцию create_global из модуля пользователя
            create_global = getattr(user_module, 'create_global')
            # Выполняем функцию
            create_global(test_input[i])

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: TOTAL={expected_output[i]}")

            if not hasattr(user_module, 'TOTAL'):
                raise AttributeError("ОШИБКА: глобальная переменная TOTAL не создана")

            if user_module.TOTAL == expected_output[i]:
                test_result.append(f"Получено: TOTAL={user_module.TOTAL}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: TOTAL={expected_output[i]}\nно получен: TOTAL={user_module.TOTAL}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
