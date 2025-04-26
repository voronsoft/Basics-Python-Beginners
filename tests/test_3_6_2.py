# 3_6_2 тест для задачи
def test_3_6_2(*args):
    expected = sorted(["[ ]", "list()"])
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
