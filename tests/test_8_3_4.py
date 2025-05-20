# 8_3_4 тест для задачи
def test_8_3_4(*args):
    # Ожидается
    expected = sorted(["для поиска сторонних модулей (для их последующей установки)"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
