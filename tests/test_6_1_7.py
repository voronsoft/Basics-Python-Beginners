# 6_1_7 тест для задачи
import subprocess
import sys

from utils.code_security_check import check_code_safety


def test_6_1_7(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "+71234567890 +71234567854 +61234576890 +52134567890 +21235777890 +21234567110 +71232267890",
        "+71234447890 +61234567854 +71234576890 +52134567890 +21235777890 +51234567110 +21232267890",
    )
    # Ожидаемый результат
    expected_output = (
        "('+2', ['+21235777890', '+21234567110']) ('+5', ['+52134567890']) ('+6', ['+61234576890']) ('+7', ['+71234567890', '+71234567854', '+71232267890'])",
        "('+2', ['+21235777890', '+21232267890']) ('+5', ['+52134567890', '+51234567110']) ('+6', ['+61234567854']) ('+7', ['+71234447890', '+71234576890'])",
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

        return True, "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
