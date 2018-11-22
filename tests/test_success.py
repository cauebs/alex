from . import tokens_and_errors


def test_1():
    assert tokens_and_errors("""
    {
        basic id;
        basic[num][num] id;
    }
    """) == (
        [
            '{',

            'basic',
            'id',
            ';',

            'basic',
            '[',
            'num',
            ']',
            '[',
            'num',
            ']',
            'id',
            ';',

            '}'
        ],
        []
    )


def test_2():
    assert tokens_and_errors("""
        id == num;
        id==num;
        id <= num;
        id<=num;
    """) == (
        [
            'id',
            '==',
            'num',
            ';',

            'id',
            '==',
            'num',
            ';',

            'id',
            '<=',
            'num',
            ';',

            'id',
            '<=',
            'num',
            ';',
        ],
        []
    )


def test_3():
    assert tokens_and_errors("""
        if(id==id)then
            id = num;else{
            }
    """) == (
        [
            'if',
            '(',
            'id',
            '==',
            'id',
            ')',
            'then',

            'id',
            '=',
            'num',
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
        ;while; (;id !=; id;) {
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
            'id',
            '!=',
            ';',
            'id',
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
