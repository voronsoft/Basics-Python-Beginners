# 0_0_0 тест для задачи
def test_0_0_0(*args):

    expected = dict(
        sorted(
            {
                '': '',
                '': '',
                '': '',
                '': '',
                '': '',
                '': '',
            }.items()
        )
    )

    user_output = dict(sorted(args[0].items()))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
