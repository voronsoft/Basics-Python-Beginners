# 8_3_2 тест для задачи
def test_8_3_2(*args):
    # Ожидается
    expected = sorted(["pip install Django", "pip install -r requirements.txt", "pip install Django==2.1.2"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
