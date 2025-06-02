# 3_4_5 тест для задачи
import subprocess
import sys

from utils.code_security_check import check_code_safety


def test_3_4_5(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Проверяем, есть ли в коде raw-строка (r", r', r''', r""")
    with open(path_tmp_file, "r", encoding="utf-8") as f:
        user_code = f.read()

    # Проверяем, содержит ли код хотя бы одну raw-строку вида:
    raw_string_prefixes = ('r"', "r'", 'r"""', "r'''")
    has_raw_string = any(prefix in user_code for prefix in raw_string_prefixes)

    if not has_raw_string:
        raise ValueError(
            "------------- FAIL Тест -------------\n"
            "Вы не использовали raw-строки в своем коде.\nЯ проверил ваш код, не хитрите )))"
        )

    # Входные данные
    test_input = (r"C:\WINDOWS\System32\drivers\etc\hosts",)
    # Ожидаемый результат
    expected_output = (r"C:\WINDOWS\System32\drivers\etc\hosts",)

    result = []  # Список для накопления результатов тестов

    try:
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()
        check_code_safety(user_code)

        for i in range(len(test_input)):
            # Запускаем код пользователя, передавая ему входные данные через stdin
            process = subprocess.run(
                [
                    "python",
                    "-I",
                    "-E",
                    "-X",
                    "utf8",
                    path_tmp_file,
                ],
                input=test_input[i],
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

            test_result = [
                f"--------------- OK Тест: {i + 1} --------------",
                f"Входные данные: {test_input[i]}",
                f"Ожидалось: {expected_output[i]}",
            ]

            if output == expected_output[i]:
                test_result.extend([f"\nПолучено: {output}", f'{output} == {expected_output[i]}'])
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} -------------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)
    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
