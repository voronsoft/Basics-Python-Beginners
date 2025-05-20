# 8_7_10 тест для задачи
def test_8_7_10(*args):
    # Ожидается
    expected = sorted(["d = pickle.load(file)"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
