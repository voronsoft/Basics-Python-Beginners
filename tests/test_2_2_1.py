# 2_2_1 тест для задачи
def test_2_2_1(*args):
    expected = sorted(["целочисленному"])
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Увы, это неправильный ответ."
