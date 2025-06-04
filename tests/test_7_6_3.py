# 7_6_3 тест для задачи
import ast
import subprocess
import sys

from utils.code_security_check import check_code_safety


def test_7_6_3(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие декоратора)"""

    result = []  # Список для накопления результатов тестов

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Парсим код в дерево
        tree = ast.parse(code)
        # Искомые переменные в коде
        required_vars = {"x", "y", "z"}
        # Найденные переменные в коде
        found_vars = set()

        # Ищем только присваивания (ast.Name + ast.Store)
        for node in ast.walk(tree):
            # Находим все переменные которые определены в коде
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                # Добавляем в множество которое отсеет дубли
                found_vars.add(node.id)

        # Проверяем, что все нужные переменные есть
        missing_vars = required_vars - found_vars
        if missing_vars:
            raise ValueError(f"В коде отсутствуют обязательные переменные: {", ".join(missing_vars)}\n")

        result.append(f"Найдены переменные: {found_vars}")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_6_3_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_6_3_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "56 4 -23 2 0 3 5",
        "1 2 3 4 5 6 7",
        "10 20 30 40 50 60 70",
    )
    # Ожидаемый результат
    expected_output = (
        "56 4 -23 2",
        "1 2 3 4",
        "10 20 30 40",
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
