# 7_4_2 тест для задачи
import importlib.util
import inspect
import traceback


def test_7_4_2(path_tmp_file: str, task_num_test: str):
    """Функция тестирования функции get_rect_value из пользовательского файла"""

    # Входные данные: длина, ширина, tp (или без tp)
    test_input = (
        (15, 10, 0),  # Периметр: 2*(15+10) = 50
        (11, 33, 5),  # Площадь: 11*33 = 363
        (2, 12, -1),  # Площадь: 2*12 = 24
        (5, 10),  # Периметр: 2*(5+10) = 30
    )

    # Ожидаемые результаты
    expected_output = (
        50,
        363,
        24,
        30,
    )

    result = []  # Результаты тестов

    try:
        # Загружаем модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Проверяем наличие функции
        if not hasattr(user_module, "get_rect_value"):
            raise AttributeError("Функция 'get_rect_value' не найдена в коде пользователя")

        func = user_module.get_rect_value

        # --- ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА параметров функции ---
        sig = inspect.signature(func)
        params = sig.parameters  # словарь параметров

        # Проверка количества параметров у функции
        if len(params) != 3:
            raise ValueError(f"Ожидалось 3 параметра в функции, но найдено: {len(params)}")
        # Проверка, что tp есть в параметрах функции
        if "tp" not in params:
            raise ValueError("Параметр 'tp' не найден в списке параметров функции")

        # Проверяем, что tp имеет значение по умолчанию 0
        tp_param = params["tp"]
        if tp_param.default != 0:
            raise ValueError("Параметр 'tp' должен иметь значение по умолчанию 0")

        # Проходим по каждому тесту
        for i in range(len(test_input)):
            args = test_input[i]
            expected = expected_output[i]

            # Вызываем функцию и передаем входные значения для теста
            output = func(*args)

            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected}")

            if output == expected:
                test_result.append(f"Получено: {output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected}\nно получен: {output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
