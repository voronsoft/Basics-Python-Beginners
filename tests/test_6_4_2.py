# 6_4_2 тест для задачи
def test_6_4_2(*args):
    # Ожидается
    expected = sorted(
        [
            'может хранить только данные неизменяемых типов',
            'неупорядоченная коллекция данных',
            'относится к изменяемому типу данных',
        ]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
