# 7_5_1 тест для задачи
def test_7_5_1(*args):
    # Ожидается
    expected = sorted(
        [
            'def func(*args): pass',
            'def func(*args, **kwargs): pass',
            'def func(*args, type=True, **kwargs): pass',
            'def func(x, *args, type=True, **kwargs): pass',
            'def func(x, y, *args): pass',
        ]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))
    # print(expected)
    # print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
