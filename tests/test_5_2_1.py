# 5_2_1 тест для задачи
def test_5_2_1(*args):
    expected = dict(
        sorted(
            {
                'break': 'досрочное прерывание работы оператора цикла',
                'continue': 'пропуск одной итерации цикла',
                'else': 'блок операторов, исполняемых при штатном завершении цикла',
            }.items()
        )
    )

    user_output = dict(sorted(args[0].items()))
    assert expected == user_output, "Нет, это неправильный ответ."
