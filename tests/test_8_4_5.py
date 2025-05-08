# 8_4_5 тест для задачи
def test_8_4_5(*args):
    # Ожидается
    expected = sorted(["panda_pack.panda.PND"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
