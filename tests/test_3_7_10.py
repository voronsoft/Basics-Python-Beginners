# 3_7_10 тест для задачи
def test_3_7_10(*args):
    # Ожидается
    expected = sorted(["False"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
