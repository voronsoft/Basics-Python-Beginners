# 10_5_2 тест для задачи
def test_10_5_2(*args):
    # Ожидается
    expected = sorted(["2"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
