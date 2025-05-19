# 1_3_2 тест для задачи
import subprocess
import sys


def test_1_3_2(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя для вывода строки 'Hello Python!'"""
    expected_output = "13"  # Ожидаемый результат
    result = []  # Список для накопления результатов тестов

    try:
        # Запускаем код пользователя без входных данных
        process = subprocess.run(
            ["python", "-I", "-E", "-X", "utf8", path_tmp_file],
            text=True,
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )

        # Получаем результат (stdout)
        output = process.stdout.strip()
        test_result = list()
        test_result.append(f"--------------- OK Тест --------------")
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
