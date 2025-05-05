# 8_7_3 тест для задачи
def test_8_7_3(*args):
    # Ожидается
    expected = sorted(["write", "writelines"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."