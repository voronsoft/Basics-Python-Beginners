# 3_7_11 тест для задачи
def test_3_7_11(*args):
    # Ожидается
    expected = sorted(["возникнет ошибка TypeError"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    # print(expected)
    # print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
