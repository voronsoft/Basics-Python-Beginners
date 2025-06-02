# 5_6_5 тест для задачи
import subprocess
import sys

from utils.code_security_check import check_code_safety


def test_5_6_5(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "2 3 4 5 6\n3 2 7 8 9\n4 7 2 0 4\n5 8 0 2 1\n6 9 4 1 2",
        "1 3 4 5 6\n3 1 7 8 9\n4 7 1 0 4\n5 8 0 1 0\n6 9 4 0 1",
        "0 3 4 5 6\n3 0 7 8 9\n4 7 0 2 4\n5 4 0 0 1\n6 9 4 1 0",
        "7 3 4 5 1\n3 7 7 8 9\n4 7 7 0 3\n5 8 0 7 1\n6 9 4 1 7",
    )
    # Ожидаемый результат
    expected_output = (
        "ДА",
        "ДА",
        "НЕТ",
        "НЕТ",
    )

    result = []  # Список для накопления результатов тестов

    try:
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()

        # Проверка кода на безопасность
        check_code_safety(user_code, allowed_imports=["sys"], allowed_calls=["sys.stdin.readlines"])

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
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Сравниваем результат с ожидаемым значением
            if output == expected_output[i]:
                test_result.append(f"Получено: {output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
