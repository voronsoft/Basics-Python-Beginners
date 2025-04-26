# 2_2_2 тест для задачи
def test_2_2_2(*args):
    expected = sorted(["вещественному"])
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
