# 7_3_1 тест для задачи
import importlib.util
import traceback


def test_7_3_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования функции get_nod(a, b) из пользовательского файла"""

    # Тестовые данные
    test_input = (
        (15, 121050),
        (11, 33),
        (2, 1001),
    )
    expected_output = (
        15,
        11,
        1,
    )

    result = []  # Список для накопления результатов тестов

    try:
        # Загружаем модуль пользователя по пути
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Проверяем, есть ли нужная функция
        if not hasattr(user_module, "get_nod"):
            raise AttributeError("Функция 'get_nod' не найдена в коде пользователя")

        # Проходим по каждому тесту
        for i in range(len(test_input)):
            a, b = test_input[i]  # Распаковываем аргументы
            expected = expected_output[i]

            # Вызываем функцию
            output = user_module.get_nod(a, b)

            # Формируем отчет по тесту
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            if output == expected:
                test_result.append(f"Получено: {output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{traceback.format_exc()}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
