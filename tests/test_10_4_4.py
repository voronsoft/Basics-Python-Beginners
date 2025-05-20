# 10_4_4 тест для задачи
def test_10_4_4(*args):
    # Ожидается
    expected = sorted(["Ошибка загрузки страницы"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
