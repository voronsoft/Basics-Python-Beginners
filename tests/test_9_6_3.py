# 9_6_3 тест для задачи
import importlib.util


def test_9_6_3(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        {'cat': 'кот', 'horse': 'лошадь', 'tree': 'дерево', 'dog': 'собака', 'book': 'книга'},
        {'zebra': 'зебра', 'apple': 'яблоко', 'monkey': 'обезьяна'},
        {'a': 'А', 'b': 'Б', 'c': 'В'},
    )

    # Ожидаемые данные вывода
    expected_output = (
        ['дерево', 'лошадь', 'собака', 'кот', 'книга'],
        ['зебра', 'обезьяна', 'яблоко'],
        ['В', 'Б', 'А'],
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(user_module)

            # Получаем список lst для проверки из модуля
            get_sort = getattr(user_module, "get_sort")
            # Выполняем функцию с тестовыми данными
            answer = get_sort(test_input[i])

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            if answer == expected_output[i]:
                test_result.append(f"Получено: {answer}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получено: {answer}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
