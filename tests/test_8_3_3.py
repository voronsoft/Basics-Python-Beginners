# 8_3_3 тест для задачи
def test_8_3_3(*args):
    # Ожидается
    expected = sorted(["создает текстовый файл со списком установленных модулей и номерами их версий"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
