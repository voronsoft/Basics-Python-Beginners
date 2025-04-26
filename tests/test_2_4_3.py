# 2_4_3 тест для задачи
import subprocess


def test_2_4_3(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Ожидаемый результат
    expected_output = "Hello Balakirev"

    try:
        # Чтение кода из файла
        with open(path_tmp_file, "r", encoding="utf-8") as file:
            user_code = file.read()

        # Подсчитываем количество вхождений слова 'print' в коде
        print_count = user_code.count("print(")

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
        test_result.append(f"Ожидалось:\n{expected_output}")

        # Проверяем результат и количество вызовов print
        if output == expected_output and print_count == 2:
            test_result.append(f"Получено:\n{output}")
            test_result.append(f"Количество вызовов print: {print_count}")
        else:
            raise ValueError(
                f"------------- FAIL Тест --------\n"
                f"Ожидалось:\n{expected_output}\n"
                f"но получен:\n{output}\n"
                f"Количество вызовов print: {print_count}\n"
            )

        return True, "\n".join(test_result)  # Возвращаем статус и результат теста

    except Exception as e:
        # Добавляем информацию об ошибке
        error_info = f"Ошибка выполнения кода:\n\n{e}"
        raise RuntimeError(error_info)
