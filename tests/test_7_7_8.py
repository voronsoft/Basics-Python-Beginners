# 7_7_8 тест для задачи
import ast
import subprocess
import sys

from utils.code_security_check import check_code_safety


def test_7_7_8(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

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
            if isinstance(node, ast.FunctionDef):
                find_func = node.name

                # Обход всех узлов внутри тела функции
                for inner_node in ast.walk(node):
                    # Ищем вызов этой же функции внутри неё самой
                    if isinstance(inner_node, ast.Call):
                        if isinstance(inner_node.func, ast.Name) and inner_node.func.id == find_func:
                            is_recursive = True
                            break
                break

        if not find_func:
            raise ValueError("ОШИБКА: Не найдена функция в коде")

        if not is_recursive:
            raise TypeError(f"ОШИБКА: '{find_func}' не является рекурсивной функцией")

        result.append(f"Функция найдена: '{find_func}'")
        result.append(f"Функция '{find_func}': recursive")
        result.append(f"--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_7_8_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_7_8_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "8 11 -6 3 0 1 1",
        "5 3 3 6 8 5 3 -10 343 53 7",
        "1 -1",
        "-10 -16 -10 -1 0 1 16 10 1",
    )

    # Ожидаемый результат
    expected_output = (
        "-6 0 1 1 3 8 11",
        "-10 3 3 3 5 5 6 7 8 53 343",
        "-1 1",
        "-16 -10 -10 -1 0 1 1 10 16",
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Запускаем код пользователя, передавая ему входные данные через stdin
            process = subprocess.run(
                ["python", "-I", "-E", "-X", "utf8", path_tmp_file],  # Запускаем временный файл
                input=test_input[i],  # Передаём input
                text=True,  # Режим работы с текстом
                capture_output=True,  # Захватываем stdout и stderr
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                encoding="utf-8",  # Явно указываем кодировку
                timeout=5,  # Важно: ограничение времени выполнения кода
            )

            # Получаем результат (stdout)
            output = process.stdout.strip()
            # Получаем сообщения об ошибках
            error = process.stderr.strip()
            if error:  # Если есть ошибки в коде выводим
                raise ValueError(error)

            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Сравниваем результат с ожидаемым значением
            if output == expected_output[i]:
                test_result.append(f"Получено: {output}\n")

            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
