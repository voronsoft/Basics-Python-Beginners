# 10_5_1 тест для задачи
def test_10_5_1(*args):
    # Ожидается
    expected = sorted(["Петр, Иванович, Сидоров"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
