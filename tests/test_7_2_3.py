# 7_2_3 тест для задачи
import importlib.util
import sys


def test_7_2_3(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Проверяем, есть ли в коде 'def is_large('
    with open(path_tmp_file, "r", encoding="utf-8") as f:
        user_code = f.read()

    if "def is_large(" not in user_code:
        raise ValueError(
            "------------- FAIL Тест -------------\n" "В коде не найдено объявление функции 'def is_large('"
        )

    # Входные данные
    test_input = (
        "Я люблю Python!",
        "Оса",
        "Мы",
    )
    # Ожидаемый результат
    expected_output = (
        "True",
        "True",
        "False",
    )

    result = []  # Список для накопления результатов тестов

    # Загружаем модуль пользователя
    spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
    user_module = importlib.util.module_from_spec(spec)
    sys.modules["user_module"] = user_module
    spec.loader.exec_module(user_module)

    try:
        for i in range(len(test_input)):
            test_result = [
                f"---------------OK Тест: {i + 1} --------------",
                f"Входные данные: {test_input[i]}",
                f"Ожидалось: {expected_output[i]}",
            ]

            # Проверяем наличие функции
            if not hasattr(user_module, "is_large"):
                raise ValueError(f"------------- FAIL Тест {i + 1} --------\nФункция 'is_large' не найдена")

            # Вызываем функцию и получаем результат
            output = str(user_module.is_large(test_input[i]))
            test_result.append(f"Получено: {output}")

            # Сравниваем результат с ожидаемым значением
            if output != expected_output[i]:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\n"
                    f"Получено: {output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)
    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
