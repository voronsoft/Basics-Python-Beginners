# 3_2_4 тест для задачи
def test_3_2_4(*args):

    expected = sorted(["ничего, будет ошибка IndexError"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
