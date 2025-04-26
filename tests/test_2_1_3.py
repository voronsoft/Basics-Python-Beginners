# 2_1_3 тест для задачи
def test_2_1_3(*args):
    expected = sorted(["a = 6", "a = b = 0"])
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
