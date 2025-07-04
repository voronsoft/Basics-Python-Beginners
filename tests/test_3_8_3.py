# 3_8_3 тест для задачи
import subprocess

from utils.code_security_check import check_code_safety


def test_3_8_3(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Проверяем, есть ли в коде 'cities = ["Токио", "Берлин", "Париж"]'
    with open(path_tmp_file, "r", encoding="utf-8") as f:
        user_code = f.read()

    # Проверка кода на безопасность
    check_code_safety(user_code)

    if 'cities = ["Токио", "Берлин", "Париж"]' not in user_code:
        raise ValueError(
            '------------- FAIL Тест -------------\n'
            'В коде не найдено: cities = ["Токио", "Берлин", "Париж"]\nЯ проверил ваш код, не хитрите )))'
        )
    # Проверяем, есть ли в коде print(*cities
    if "print(*cities" not in user_code:
        raise ValueError('------------- FAIL Тест -------------\n' 'В коде не найдено: print(*cities')

    # Ожидаемый результат
    expected_output = 'Токио Лондон Берлин Париж'

    result = []  # Список для накопления результатов тестов

    try:

        # Запускаем код пользователя, передавая ему входные данные через stdin
        process = subprocess.run(
            ["python", "-I", "-E", "-X", "utf8", path_tmp_file],  # Запуск в изолир среде: -I(изол), -E(игнор пер/окруж)
            input="",  # Передаём input
            text=True,  # Режим работы с текстом
            capture_output=True,  # Захватываем stdout и stderr
            encoding="utf-8",  # Явно указываем кодировку
        )

        # Получаем результат (stdout)
        output = process.stdout.strip()
        test_result = list()
        test_result.append(f"---------------OK Тест --------------")
        test_result.append(f"Ожидалось: {expected_output}")

        # Сравниваем результат с ожидаемым значением
        if output == expected_output:
            test_result.append(f"Получено: {output}\n")
        else:
            raise ValueError(
                f"------------- FAIL Тест --------\n" f"Ожидалось: {expected_output}\nно получен: {output}\n"
            )

        result.append("\n".join(test_result))

        return True, "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
