from . import tokens_and_errors


def match_errors(errors, expected_locations):
    assert len(errors) == len(expected_locations)

    for e, (line, column) in zip(errors, expected_locations):
        assert e.line_number == line
        assert e.column_number == column


def test_1():
    tokens, errors = tokens_and_errors("! & 1")

    assert tokens == ['!', 'num']

    match_errors(errors, [
        (0, 3),
    ])


def test_2():
    tokens, errors = tokens_and_errors("123;123. 123;")

    assert tokens == ['num', ';', 'num', ';']

    match_errors(errors, [
        (0, 8),
    ])
