# 8_2_7 тест для задачи
def test_8_2_7(*args):
    # Ожидается
    expected = sorted(["panda.kungfu.KUNGFU"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
