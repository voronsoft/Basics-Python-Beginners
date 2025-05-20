# 3_3_4 тест для задачи
def test_3_3_4(*args):
    expected = sorted(["ничего, возникнет ошибка ValueError"])
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
