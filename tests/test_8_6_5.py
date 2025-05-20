# 8_6_5 тест для задачи
def test_8_6_5(*args):
    # Ожидается
    expected = sorted(["всегда после выполнения блоков try и except"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    # print(expected)
    # print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
