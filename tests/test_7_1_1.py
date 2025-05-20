# 7_1_1 тест для задачи
def test_7_1_1(*args):
    # Ожидается
    expected = sorted(['dp = print', 'fl = len', 'len', 'len(123)', 'print', 'print()'])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
