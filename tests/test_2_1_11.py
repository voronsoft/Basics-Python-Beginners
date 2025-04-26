# 2_1_11 тест для задачи
def test_2_1_11(*args):
    expected = sorted(["переменная type будет ссылаться на число 7"])
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
