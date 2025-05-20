# 2_4_1 тест для задачи
import subprocess
import sys


def test_2_4_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Ожидаемый результат
    expected_output = "7 -4 3"

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(1):
            # Запускаем код пользователя
            process = subprocess.run(
                [
                    "python",
                    "-I",
                    "-E",
                    "-X",
                    "utf8",
                    path_tmp_file,
                ],  # Запуск в изолир среде: -I(изол), -E(игнор пер/окруж)
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

            # Формируем вывод теста
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Ожидалось: {expected_output}")

            # Сравниваем результат с ожидаемым значением
            if output == expected_output:
                test_result.append(f"Получено: {output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} -------------\n"
                    f"Ожидалось: {expected_output}\nно получен:{output}\n"
                )
            result.append("\n".join(test_result))

        return True, "\n".join(result)  # Возвращаем статус и результаты тестов

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = f"Ошибка выполнения кода:\n\n{e}"
        raise RuntimeError(error_info)
