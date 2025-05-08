# 8_7_7 тест для задачи
def test_8_7_7(*args):
    # Ожидается
    expected = sorted(["writelines"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
