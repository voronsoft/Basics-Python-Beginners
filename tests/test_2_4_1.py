# 2_4_1 тест для задачи
import subprocess


def test_2_4_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Ожидаемый результат
    expected_output = "7 -4 3"

    try:
        # Запускаем код пользователя
        process = subprocess.run(
            ["python", "-I", "-E", "-X", "utf8", path_tmp_file],  # Запуск в изолир среде: -I(изол), -E(игнор пер/окруж)
            text=True,  # Режим работы с текстом
            capture_output=True,  # Захватываем stdout и stderr
            encoding="utf-8",  # Явно указываем кодировку
        )

        # Получаем результат (stdout)
        output = process.stdout.strip("\n")

        # Формируем вывод теста
        test_result = list()
        test_result.append("---------------OK Тест --------------")
        test_result.append(f"Ожидалось: {expected_output}")

        # Сравниваем результат с ожидаемым значением
        if output == expected_output:
            test_result.append(f"Получено: {output}\n")
            test_result.append(f"{output} == {expected_output}")
        else:
            raise ValueError(
                f"------------- FAIL Тест --------\n" f"Ожидалось: {expected_output}\nно получен:{output}\n"
            )

        return True, "\n".join(test_result)  # Возвращаем статус и результат теста

    except Exception as e:
        # Добавляем информацию об ошибке
        error_info = f"Ошибка выполнения кода:\n\n{e}"
        raise RuntimeError(error_info)
