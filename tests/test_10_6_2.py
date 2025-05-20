# 10_6_2 тест для задачи
def test_10_6_2(*args):
    # Ожидается
    expected = sorted(
        [
            "case {'marks': ms, 'age': age, 'fio': fio} if age == 22: ...",
            "case {'marks': ms, 'age': age} if age == 22: ...",
            "case {'marks': m, 'age': 22}: ...",
        ]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))
    # print(expected)
    # print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
