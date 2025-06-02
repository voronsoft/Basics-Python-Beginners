# 5_5_1 тест для задачи
def test_5_5_1(*args):
    # Ожидается
    expected = sorted(['iter(7)', 'iter(True)'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
