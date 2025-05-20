# 6_4_1 тест для задачи
def test_6_4_1(*args):
    # Ожидается
    expected = sorted(
        [
            'set()',
            'set([1, 2, 3, 2, 1])',
            '{1, 1, 5, 5, True, 1}',
        ]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
