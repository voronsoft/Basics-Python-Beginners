# 3_1_2 тест для задачи
def test_3_1_2(*args):

    expected = sorted(['тройных двойных', 'тройных одинарных'])
    user_output = sorted(args[0].split(";_"))
    # print(111, user_output)
    # print(222, expected)
    assert expected == user_output, "Нет, это неправильный ответ."
