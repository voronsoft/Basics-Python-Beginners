# 2_4_11 тест для задачи
import subprocess
import sys

from utils.code_security_check import check_code_safety


def test_2_4_11(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""

    # Ожидаемый результат
    expected_output = "3.142"

    result = []  # Список для накопления результатов тестов

    try:
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()

        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(user_code)

        # Запускаем код пользователя, передавая ему входные данные через stdin
        process = subprocess.run(
            ["python", "-I", "-E", "-X", "utf8", path_tmp_file],  # Запуск в изолир среде: -I(изол), -E(игнор пер/окруж)
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
        test_result.append(f"---------------OK Тест --------------")
        test_result.append(f"Ожидалось: {expected_output}")

        # Сравниваем результат с ожидаемым значением
        if output == expected_output:
            test_result.append(f"Получено: {output}\n")

        else:
            raise ValueError(
                f"------------- FAIL Тест: 1 -------------\nОжидалось: {expected_output}\nно получен: {output}\n"
            )

        result.append("\n".join(test_result))

        return True, "\n".join(result)  # Возвращаем статус и результаты тестов

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
