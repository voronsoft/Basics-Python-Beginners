# 8_6_4 тест для задачи
def test_8_6_4(*args):
    # Ожидается
    expected = sorted(['with open(my_file.txt) as file: ...'])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
