# 2_2_12 тест для задачи
def test_2_2_12(*args):
    expected = sorted(["int"])
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
