# 3_7_8 тест для задачи
def test_3_7_8(*args):
    # Ожидается
    expected = sorted(["True"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
