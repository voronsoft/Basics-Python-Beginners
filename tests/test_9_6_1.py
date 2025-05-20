# 9_6_1 тест для задачи
def test_9_6_1(*args):
    # Ожидается
    expected = sorted(
        [
            "метод sort сортирует список, для которого вызывается",
            "метод sort применим только к спискам (среди базовых типов данных)",
            "функция sorted возвращает отсортированный список для итерируемого объекта",
        ]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))
    # print(expected)
    # print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
