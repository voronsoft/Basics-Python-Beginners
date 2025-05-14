# 10_1_5 тест для задачи
def test_10_1_5(*args):
    # Ожидается
    expected = sorted(['-0b1101', '0b111', '0o45', '45.6'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
