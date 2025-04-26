# 6_6_6 тест для задачи
import importlib.util
import io
import sys


def test_6_6_6(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя с обработкой неупорядоченных множеств"""
    # Входные данные (3 варианта)
    test_inputs = (
        # Вариант 1
        "Пушкин: Сказка о рыбаке и рыбке\nЕсенин: Письмо к женщине\nТургенев: Муму\nПушкин: Евгений Онегин\nЕсенин: Русь",
        # Вариант 2
        "Толстой: Война и мир\nТолстой: Анна Каренина\nЧехов: Вишнёвый сад\nТолстой: Воскресение\nЧехов: Чайка",
        # Вариант 3
        "Достоевский: Преступление и наказание\nДостоевский: Идиот\nДостоевский: Братья Карамазовы",
    )

    # Ожидаемые результаты (в виде словарей с отсортированными списками вместо множеств)
    expected_outputs = (
        {
            'Пушкин': ['Евгений Онегин', 'Сказка о рыбаке и рыбке'],
            'Есенин': ['Письмо к женщине', 'Русь'],
            'Тургенев': ['Муму'],
        },
        {'Толстой': ['Анна Каренина', 'Война и мир', 'Воскресение'], 'Чехов': ['Вишнёвый сад', 'Чайка']},
        {'Достоевский': ['Братья Карамазовы', 'Идиот', 'Преступление и наказание']},
    )

    result = []  # Список для накопления результатов тестов
    result.append(
        "___________ !!!PS: ___________\n"
        "Так как множества неупорядоченная коллекция при тестировании множество было переведено в список.\n"
        "Что бы при тестировании было проще сравнивать ваш ответ с ожидаемым.\n"
        "Но при выводе об успешном решении мы перевели список в множество.\n"
        "______________________________\n\n"
    )

    try:
        for i, input_data in enumerate(test_inputs, 1):
            # 1. Динамическая загрузка модуля пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)
            sys.modules["user_module"] = user_module

            # 2. Имитация ввода через stdin
            sys.stdin = io.StringIO(input_data)
            spec.loader.exec_module(user_module)

            # 3. Проверка существования словаря d
            if not hasattr(user_module, "d"):
                raise ValueError("В коде отсутствует словарь 'd'.")

            # 4. Нормализация результатов:
            #    - Преобразуем множества в отсортированные списки
            #    - Это нужно потому что множества неупорядоченны и их строковые представления могут различаться
            user_d_sorted = {author: sorted(books) for author, books in user_module.d.items()}
            expected_d = expected_outputs[i - 1]

            # 5. Формирование отчета
            test_result = [
                f"--------------- Тест: {i} --------------",
                f"Входные данные:\n{input_data}",
                f"Ожидалось:\n{str(expected_d).replace("[", "{").replace("]", "}")}",
            ]

            # 6. Сравнение нормализованных данных
            if user_d_sorted == expected_d:
                # Подмена скобок для красивого вывода (без изменения данных)
                pretty_output = str(user_d_sorted).replace("[", "{").replace("]", "}")
                test_result.extend([f"Получено:\n{pretty_output}", "Тест пройден успешно!\n"])
                result.append("\n".join(test_result))
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i} --------\n"
                    f"Входные данные:\n{input_data}\n"
                    f"Ожидалось:\n{str(expected_d).replace("[", "{").replace("]", "}")}\n"
                    f"но получен:\n{str(user_d_sorted).replace("[", "{").replace("]", "}")}\n"
                )

        return True, "\n".join(result)
    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
    finally:
        sys.stdin = sys.__stdin__  # Важно: восстанавливаем оригинальный stdin
