# 3_6_10 тест для задачи
import subprocess
import sys

from utils.code_security_check import check_code_safety


def test_3_6_10(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Проверяем, есть ли в коде переменная book
    with open(path_tmp_file, "r", encoding="utf-8") as f:
        user_code = f.read()

    # Проверка кода на безопасность
    check_code_safety(user_code)

    # Проверка, что book создается как список
    # Проверка, что используется выражение в коде - print(*lst)
    if 'print(*lst)' not in user_code:
        raise ValueError(
            "------------- FAIL Тест -------------\n"
            "Вы не использовали 'print(*lst)' в своем коде.\n"
            "Да вы могли бы решить и другим способом, не спорю )\n"
            "Важно что бы в вашей памяти закреплялись конструкции нового типа\n"
            "или те конструкции которые вы могли подзабыть!\n"
            "Это важный момент в обучении или повторении."
        )

    # Входные данные
    test_input = (
        "52 65 64 54 68 59 42 63",
        "54 68 59 42 63",
        "1 2 3 4 5 6 7 8 9",
        "-10 25 -40 50",
    )
    # Ожидаемый результат
    expected_output = (
        "68 65 64 63 59 54 52 42",
        "68 63 59 54 42",
        "9 8 7 6 5 4 3 2 1",
        "50 25 -10 -40",
    )

    result = []  # Список для накопления результатов тестов

    try:
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
                ],  # Запуск в изолир среде: -I(изол), -E(игнор пер/окруж)
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
