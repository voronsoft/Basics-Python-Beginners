# 10_1_7 тест для задачи
import importlib.util
import sys

from io import StringIO


def test_10_1_7(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        if "16**1" not in code and "16**0" not in code:
            raise RuntimeError(
                "ОШИБКА: Используйте шаблонное выражение из задания пожалуйста\n"
                "Цель задания научить вас разбираться в этой области."
            )

        result.append("Вы умница все правильно сделали используя шаблон из задания!!!")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_10_1_7_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_10_1_7_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = ("0xcf",)

    # Ожидаемые данные вывода
    expected_output = (207,)

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            original_stdin = sys.stdin

            # Подменяем stdin (заглушка)
            sys.stdin = StringIO('')

            # Выполняем пользовательский модуль
            spec.loader.exec_module(user_module)

            # Получаем из модуля answer
            answer = getattr(user_module, "answer")

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Проверка
            if answer == expected_output[i]:
                test_result.append(f"Получено: {answer}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {answer}"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
