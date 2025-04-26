# 2_1_5 тест для задачи
def test_2_1_5(*args):

    expected = sorted(["каскадным присваиванием"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
