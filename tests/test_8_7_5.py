# 8_7_5 тест для задачи
def test_8_7_5(*args):
    # Ожидается
    expected = sorted(["некоторые записываемые данные могут быть потеряны"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."