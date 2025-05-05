# 6_3_2 тест для задачи
def test_6_3_2(*args):
    # Ожидается
    expected = sorted(
        ['неизменяемый тип данных', 'расходует меньше памяти, чем списки', 'упорядоченная коллекция данных']
    )
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
