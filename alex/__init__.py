from dataclasses import dataclass, field
from string import ascii_letters, punctuation, whitespace
from typing import Dict, Generator, Iterable, List, NamedTuple, Optional

_TOKENS = [
    'basic', 'true', 'false', 'break', 'do', 'else',
    'if', 'then', 'while', '!', '!=', '&&', '(', ')', '+', '/', ';', '<',
    '<=', '=', '==', '>', '>=', '[', ']', '{', '||', '}', '−', '∗'
]

id_chars = ascii_letters + '_'


@dataclass
class Token:
    token: str
    code: str

    line_number: int
    column_start: int
    column_end: int


@dataclass
class State:
    accepts: Optional[str] = None
    transitions: Dict[str, 'State'] = field(default_factory=dict)


def tokens_to_trie(tokens: Iterable[str]) -> State:
    root = State()

    id = State()
    id.accepts = 'id'

    for c in id_chars:
        id.transitions[c] = id

    for token in tokens:
        current = root

        for symbol in token:
            s = State()

            if symbol in id_chars:
                s.accepts = 'id'

            current = current.transitions.setdefault(symbol, s)

        current.accepts = token

    def fill(state: State):
        if state == id:
            return

        for c in id_chars:
            state.transitions.setdefault(c, id)

        for (char, state) in state.transitions.items():
            if char in id_chars:
                fill(state)

    fill(root)

    return root


def create_automaton() -> State:
    root = tokens_to_trie(_TOKENS)

    first_num = State()
    num = State()
    dot = State()
    real = State()

    for n in '0123456789':
        root.transitions[n] = num
        first_num.transitions[n] = num
        num.transitions[n] = num
        dot.transitions[n] = real
        real.transitions[n] = real

    num.transitions['.'] = dot

    num.accepts = 'num'
    real.accepts = 'real'

    return root


class LexicalError(NamedTuple):
    line_number: int
    column_number: int
    message: str

    def __str__(self) -> str:
        return f'{self.line_number}:{self.column_number} - {self.message}'


def make_token(token, column_start, column_end, line_start, line_end, code):
    line = code[line_start]

    if line_start != line_end:
        column_end = len(line)

    return Token(
        token=token,
        column_start=column_start,
        column_end=column_end,
        line_number=line_start,
        code=line[column_start:column_end],
    )


def alex(string: str) -> Generator[Token, None, List[LexicalError]]:
    string = string.strip()

    automaton = create_automaton()
    current = automaton

    separators = whitespace + punctuation
    previous = None
    panic = False

    pending = False

    errors = []

    code = string.splitlines()

    for line_number, line in enumerate(code):
        for column_number, character in enumerate(line):
            if not pending and character in whitespace:
                panic = False
                continue

            if not pending:
                token_line_start = line_number
                token_column_start = column_number

            pending = True

            # received one of the expected symbols
            if character in current.transitions:
                panic = False
                current = current.transitions[character]
                previous = character
                continue

            # if in panic mode, just skip until it's possible to restart
            if panic:
                continue

            # didn't expect this symbol, but already had a valid token
            if current.accepts:
                yield make_token(
                    token=current.accepts,
                    column_start=token_column_start,
                    column_end=column_number,
                    line_start=token_line_start,
                    line_end=line_number,
                    code=code,
                )

                pending = False

                # after a token we expect only whitespace and punctuation
                if character not in separators and previous not in separators:
                    errors.append(LexicalError(
                        line_number,
                        column_number,
                        (
                            'Expected whitespace or punctuation '
                            f'after {repr(current.accepts)}.'
                        ),
                    ))

                # now reset the automaton and give this character another go
                current = automaton
                if character in whitespace:
                    continue

                if character in current.transitions:
                    token_line_start = line_number
                    token_column_start = column_number

                    pending = True
                    panic = False
                    current = current.transitions[character]
                    previous = character
                    continue

            # no tokens start with this symbol
            if not panic:
                panic = True
                pending = False
                expected = sorted(current.transitions.keys())
                errors.append(LexicalError(
                    line_number,
                    column_number,
                    (
                        f"Expected one of {{{', '.join(expected)}}}, "
                        f'got {repr(character)}.'
                    ),
                ))

            current = automaton

        previous = '\n'

    # ran out of characters, but already had a token
    if current.accepts:
        yield make_token(
            token=current.accepts,
            column_start=token_column_start,
            column_end=column_number + 1,
            line_start=token_line_start,
            line_end=line_number,
            code=code,
        )

    # reached EOF while scanning
    elif pending:
        expected = sorted(current.transitions.keys())
        errors.append(LexicalError(
            line_number,
            column_number,
            (
                f"Expected one of {{{', '.join(expected)}}}, "
                f'but reached EOF.'
            ),
        ))

    return errors
