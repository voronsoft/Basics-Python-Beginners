# 8_5_2 тест для задачи
def test_8_5_2(*args):
    # Ожидается
    expected = sorted(["dat/text.dat", "C:/python/course/dat/text.dat"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
