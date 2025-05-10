# 9_3_4 тест для задачи
import importlib.util
import sys

from io import StringIO


def test_9_3_4(path_tmp_file: str, generator_funcs: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "house=дом car=машина men=человек tree=дерево",
        "1=one 2=two 5=five",
    )
    # Ожидаемый результат
    expected_output = (
        (('house', 'дом'), ('car', 'машина'), ('men', 'человек'), ('tree', 'дерево')),
        (('1', 'one'), ('2', 'two'), ('5', 'five')),
    )
    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Подменяем stdin с тестовыми данными
            sys.stdin = StringIO(test_input[i])

            # Создаем буфер для перехвата вывода
            output_buffer = StringIO()
            # Сохраняем оригинальный stdout
            original_stdout = sys.stdout
            # Перенаправляем stdout в буфер
            sys.stdout = output_buffer

            spec.loader.exec_module(user_module)

            # Получаем перехваченный вывод из print()
            captured_output = output_buffer.getvalue().rstrip()
            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            tp = getattr(user_module, "tp")  # Получаем функцию из модуля
            # Выполняем функцию, что бы получить первые 5ть результатов для проверки
            print("tp", tp)
            # Проверяем результат
            if tp == expected_output[i]:
                test_result.append(f"Получено: {tp}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{tp}\n"
                )

            if tp != expected_output[i]:
                raise ValueError(
                    f"------------- FAIL Тест проверка что возвращает функция: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {tp}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
