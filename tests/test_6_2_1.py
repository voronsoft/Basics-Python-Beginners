# 6_2_1 тест для задачи
def test_6_2_1(*args):
    # Ожидается
    expected = sorted(['d.copy()', 'dict(d)'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
