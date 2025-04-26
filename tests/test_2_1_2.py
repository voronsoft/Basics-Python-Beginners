# 2_1_2 тест для задачи
def test_2_1_2(*args):

    expected = sorted(["связывает переменную с данными", "создает переменную, если ее ранее не было"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
