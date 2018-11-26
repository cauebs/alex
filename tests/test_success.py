from . import tokens_and_errors


def test_1():
    assert tokens_and_errors("""
    {
        while if;
        while[123][123] if;
    }
    """) == (
        [
            '{',

            'while',
            'if',
            ';',

            'while',
            '[',
            'num',
            ']',
            '[',
            'num',
            ']',
            'if',
            ';',

            '}'
        ],
        []
    )


def test_2():
    assert tokens_and_errors("""
        if == 1;
        if==564;
        if <= 4353;
        if<=543;
    """) == (
        [
            'if',
            '==',
            'num',
            ';',

            'if',
            '==',
            'num',
            ';',

            'if',
            '<=',
            'num',
            ';',

            'if',
            '<=',
            'num',
            ';',
        ],
        []
    )


def test_3():
    assert tokens_and_errors("""
        if(if==if)then
            if = 11.111;else{
            }
    """) == (
        [
            'if',
            '(',
            'if',
            '==',
            'if',
            ')',
            'then',

            'if',
            '=',
            'real',
            ';',
            'else',
            '{',

            '}',
        ],
        []
    )


def test_4():
    assert tokens_and_errors("") == (
        [],
        []
    )


def test_5():
    assert tokens_and_errors("""
        ;while; (;if !=; if;) {
            if (==) then else
            true false;break
        };;;;
    """) == (
        [
            ';',
            'while',
            ';',
            '(',
            ';',
            'if',
            '!=',
            ';',
            'if',
            ';',
            ')',
            '{',

            'if',
            '(',
            '==',
            ')',
            'then',
            'else',
            'true',
            'false',
            ';',
            'break',

            '}',
            ';',
            ';',
            ';',
            ';',
        ],
        []
    )


def test_6():
    assert tokens_and_errors("=>") == (
        [
            '=',
            '>',
        ],
        []
    )


def test_7():
    assert tokens_and_errors("i") == (
        ['id'],
        []
    )


def test_8():
    assert tokens_and_errors("ife") == (
        ['id'],
        []
    )
