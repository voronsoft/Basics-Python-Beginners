# 2_1_1 тест для задачи
def test_2_1_1(*args):

    expected = sorted(["ссылка на объект в памяти"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
