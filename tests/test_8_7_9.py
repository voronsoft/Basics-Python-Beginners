# 8_7_9 тест для задачи
def test_8_7_9(*args):
    # Ожидается
    expected = sorted(["pickle.dump(d, file)"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."