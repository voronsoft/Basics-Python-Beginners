# 0_0_0 тест для задачи
def test_0_0_0(*args):
    # Ожидается
    expected = sorted([""])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
