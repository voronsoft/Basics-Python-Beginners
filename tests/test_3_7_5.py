# 3_7_5 тест для задачи
import subprocess


def test_3_7_5(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Проверяем, содержит ли код список из задачи m = [2, 3, 5, 5, 2, 2, 3, 3, 4, 5, 4, 4]
    with open(path_tmp_file, "r", encoding="utf-8") as f:
        user_code = f.read()
        print(5644, user_code)

    string = "m = [2, 3, 5, 5, 2, 2, 3, 3, 4, 5, 4, 4]"

    if string not in user_code:
        raise ValueError(
            "------------- FAIL Тест -------------\n"
            "Вы не использовали в коде\nm = [2, 3, 5, 5, 2, 2, 3, 3, 4, 5, 4, 4]"
        )

    # Входные данные (в этой задаче ввода нет)
    test_input = ""

    # Ожидаемый результат
    expected_output = "[3, 2, 2, 5, 5]"

    result = []  # Список для накопления результатов тестов

    try:
        # Запускаем код пользователя
        process = subprocess.run(
            ["python", "-I", "-E", "-X", "utf8", path_tmp_file],  # Запуск в изолир среде: -I(изол), -E(игнор пер/окруж)
            input=test_input,  # Передаём input (пустую строку)
            text=True,  # Режим работы с текстом
            capture_output=True,  # Захватываем stdout и stderr
            encoding="utf-8",  # Явно указываем кодировку
        )

        # Получаем результат (stdout)
        output = process.stdout.strip()
        test_result = list()
        test_result.append("---------------OK Тест: 1 --------------")
        test_result.append(f"Входные данные: m = [2, 3, 5, 5, 2, 2, 3, 3, 4, 5, 4, 4]")
        test_result.append(f"Ожидалось: {expected_output}")

        # Сравниваем результат с ожидаемым значением
        if output == expected_output:
            test_result.append(f"Получено: {output}\n")
            test_result.append(f'{output} == {expected_output}\n')
        else:
            raise ValueError(
                f"------------- FAIL Тест: 1 --------\n"
                f"Входные данные: m = [2, 3, 5, 5, 2, 2, 3, 3, 4, 5, 4, 4]\n"
                f"Ожидалось: {expected_output}\nно получен: {output}\n"
            )

        result.append("\n".join(test_result))

        return True, "\n".join(result)  # Возвращаем статус и результаты тестов

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
