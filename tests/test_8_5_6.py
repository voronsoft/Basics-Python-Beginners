# 8_5_6 тест для задачи
def test_8_5_6(*args):
    # Ожидается
    expected = sorted(["устанавливает позицию файла в начало"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
