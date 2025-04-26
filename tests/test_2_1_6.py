# 2_1_6 тест для задачи
def test_2_1_6(*args):

    expected = sorted(["множественным присваиванием"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
