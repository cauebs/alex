from . import tokens_and_errors


def match_errors(errors, expected_locations):
    assert len(errors) == len(expected_locations)

    for e, (line, column) in zip(errors, expected_locations):
        assert e.line_number == line
        assert e.column_number == column


def test_1():
    tokens, errors = tokens_and_errors("b")

    assert tokens == []

    match_errors(errors, [
        (1, 1),
    ])


def test_2():
    tokens, errors = tokens_and_errors("basicid")

    assert tokens == ['basic', 'id']

    match_errors(errors, [
        (1, 6),
    ])


def test_3():
    tokens, errors = tokens_and_errors("ifwhil")

    assert tokens == ['if']

    match_errors(errors, [
        (1, 3),
        (1, 6),
    ])


def test_4():
    tokens, errors = tokens_and_errors("ifwhil id then")

    assert tokens == ['if', 'id', 'then']

    print(errors)
    match_errors(errors, [
        (1, 3),
        (1, 7),
    ])


def test_5():
    tokens, errors = tokens_and_errors("! & num")

    assert tokens == ['!', 'num']

    match_errors(errors, [
        (1, 4),
    ])
