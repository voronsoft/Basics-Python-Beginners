# 7_6_1 тест для задачи
def test_7_6_1(*args):
    # Ожидается
    expected = sorted(['[2, 3, 4]'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."