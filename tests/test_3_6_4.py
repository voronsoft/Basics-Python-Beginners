# 3_6_4 тест для задачи
import subprocess


def test_3_6_4(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Проверяем, есть ли в коде if условие
    with open(path_tmp_file, "r", encoding="utf-8") as f:
        user_code = f.read()
        print(user_code)

    # Проверяем, содержит ли код хотя бы одну f-строку вида:
    string_prefixes = ('if', 'elif', 'else')
    has_raw_string = any(prefix in user_code for prefix in string_prefixes)

    if has_raw_string:
        raise ValueError(
            "------------- FAIL Тест -------------\n"
            "В условии написано НЕ использовать условные операторы !\nЯ проверил ваш код, не хитрите )))"
        )

    # Входные данные
    test_input = (
        "Берлин Париж Рим Мадрид",
        "Вена Прага Братислава Варшава",
        "Афины София Будапешт Белград",
    )
    # Ожидаемый результат
    expected_output = (
        "True",
        "False",
        "False",
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
                encoding="utf-8",  # Явно указываем кодировку
                timeout=3,  # Важно: ограничение времени выполнения кода
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
