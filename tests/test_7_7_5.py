# 7_7_5 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_7_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    test_input = "7"

    result = []  # Список для накопления результатов тестов

    try:
        result.append(f"-------------Тест structure ------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(user_code)

        # Разбор кода в дерево AST
        tree = ast.parse(user_code)

        find_func = False
        is_recursive = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "fact_rec":
                find_func = node.name

                # Обход всех узлов внутри тела функции
                for inner_node in ast.walk(node):
                    # Ищем вызов этой же функции внутри неё самой
                    if isinstance(inner_node, ast.Call):
                        if isinstance(inner_node.func, ast.Name) and inner_node.func.id == "fact_rec":
                            is_recursive = True
                            break
                break

        if not find_func:
            raise ValueError("ОШИБКА: Не найдена функция 'fact_rec'")

        if not is_recursive:
            raise TypeError(f"ОШИБКА: '{find_func}' не является рекурсивной функцией")

        result.append(f"Функция найдена: '{find_func}'")
        result.append(f"Функция 'fact_rec': recursive")
        result.append(f"--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_7_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_7_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""

    # Входные данные
    test_input = (
        "6",
        "8",
        "1",
        "0",
    )
    expected_output = (
        720,
        40320,
        1,
        1,
    )

    result = []  # Для накопления текстовых отчётов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=test_input[i], capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем функцию из модуля
            fact_rec = getattr(user_module, "fact_rec")
            # Вызываем функцию с тестовым вводом
            answer = fact_rec(int(test_input[i]))
            # Получаем перехваченный вывод из stdout
            captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            if answer == expected_output[i]:
                test_result.append(f"Получено: {answer}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {answer}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
