# 3_6_8 тест для задачи
import subprocess
import sys

from utils.code_security_check import check_code_safety


def test_3_6_8(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Проверяем, есть ли в коде переменная book
    with open(path_tmp_file, "r", encoding="utf-8") as f:
        user_code = f.read()

    # Проверка кода на безопасность
    check_code_safety(user_code)

    # Проверка, что book создается как список
    if not any(i in user_code for i in ("book = list(", "book = [")):
        raise ValueError("------------- FAIL Тест -------------\n" "Переменная 'book' должна быть списком (list).\n")

    # Проверка, что используется выражение в коде - print(book)
    if 'print(book)' not in user_code:
        raise ValueError("------------- FAIL Тест -------------\n" "Вы не использовали 'print(book)' в своем коде.\n")

    # Входные данные
    test_input = (
        "Мастер и Маргарита\nБулгаков\n233\n435.45",
        "Сияние\nКинг\n456\n675.33",
        "Хроники Эмбера\nЖелязны\n240\n540.25",
    )
    # Ожидаемый результат
    expected_output = (
        "['Мастер и Маргарита', 'Желязны', 870.9]",
        "['Сияние', 'Желязны', 1350.66]",
        "['Хроники Эмбера', 'Желязны', 1080.5]",
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
