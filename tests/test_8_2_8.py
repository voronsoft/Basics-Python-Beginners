# 8_2_8 тест для задачи
def test_8_2_8(*args):
    # Ожидается
    expected = sorted(['__name__ == __main__'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."