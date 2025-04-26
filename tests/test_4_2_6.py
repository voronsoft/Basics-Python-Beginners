# 4_2_6 тест для задачи
import subprocess


def test_4_2_6(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные 
    test_input = (
        "8 31",
        "7 25",
        "2 28",
        "1 31",
        "3 31",
        "4 30",
        "5 31",
        "6 30",
        "7 31",
        "9 30",
        "10 31",
        "11 30",
        "8 1",
    )
    # Ожидаемый результат
    expected_output = (
        "08.30 09.01",
        "07.24 07.26",
        "02.27 03.01",
        "01.30 02.01",
        "03.30 04.01",
        "04.29 05.01",
        "05.30 06.01",
        "06.29 07.01",
        "07.30 08.01",
        "09.29 10.01",
        "10.30 11.01",
        "11.29 12.01",
        "07.31 08.02",
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
