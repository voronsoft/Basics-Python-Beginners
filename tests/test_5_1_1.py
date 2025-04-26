# 5_1_1 тест для задачи
def test_5_1_1(*args):

    expected = dict(
        sorted(
            {
                'заголовок цикла': 'оператор цикла с условием цикла',
                'итерация': 'однократное выполнение тела цикла',
                'тело цикла': 'набор операторов, выполняемых в цикле',
            }.items()
        )
    )

    user_output = dict(sorted(args[0].items()))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
