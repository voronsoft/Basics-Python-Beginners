# 6_3_1 тест для задачи
def test_6_3_1(*args):
    # Ожидается
    expected = sorted(['(1, 2, True, False)', '(False,)', 'tuple(python)'])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
