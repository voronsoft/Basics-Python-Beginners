# 7_6_2 тест для задачи
def test_7_6_2(*args):
    # Ожидается
    expected = sorted(['print(1, 2, 3)'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."