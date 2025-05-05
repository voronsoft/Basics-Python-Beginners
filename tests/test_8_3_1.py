# 8_3_1 тест для задачи
def test_8_3_1(*args):
    # Ожидается
    expected = sorted(["отображает список установленных модулей для текущего интерпретатора"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."