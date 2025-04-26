# 6_6_1 тест для задачи
def test_6_6_1(*args):
    # Ожидается
    expected = sorted(
        [
            'генератор множеств',
            'генератор словарей',
            'генератор списков',
            'генератор целых чисел в виде арифметической прогрессии',
        ]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
