# 8_4_1 тест для задачи
def test_8_4_1(*args):
    # Ожидается
    expected = sorted(["пакет - это каталог с набором модулей и обязательным файлом __init__.py"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."