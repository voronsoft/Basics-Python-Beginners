# 3_1_1 тест для задачи
def test_3_1_1(*args):
    expected = sorted(['двойных', 'одинарных', 'тройных двойных (строка)', "тройных одинарных ('''строка''')"])
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
