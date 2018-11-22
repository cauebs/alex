from dataclasses import dataclass, field
from typing import Optional, Dict, Iterable, NamedTuple, List, Generator
from string import whitespace, punctuation


@dataclass
class Trie:
    accepts: Optional[str] = None
    transitions: Dict[str, 'Trie'] = field(default_factory=dict)


def tokens_to_trie(tokens: Iterable[str]) -> Trie:
    root = Trie()

    for token in tokens:
        current = root

        for symbol in token:
            current = current.transitions.setdefault(symbol, Trie())

        current.accepts = token

    return root


class LexicalError(NamedTuple):
    line_number: int
    column_number: int
    message: str

    def __str__(self) -> str:
        return f'{self.line_number}:{self.column_number} - {self.message}'


def alex(string: str) -> Generator[str, None, List[LexicalError]]:
    tokens = [
        'basic', 'num', 'real', 'id', 'true', 'false', 'break', 'do', 'else',
        'if', 'then', 'while', '!', '!=', '&&', '(', ')', '+', '/', ';', '<',
        '<=', '=', '==', '>', '>=', '[', ']', '{', '||', '}', '−', '∗'
    ]

    automaton = tokens_to_trie(tokens)
    current = automaton

    separators = whitespace + punctuation
    previous = None
    panic = False
    errors = []

    pending = False

    for line_number, line in enumerate(string.splitlines(), start=1):
        for column_number, character in enumerate(line, start=1):
            pending = True

            # received one of the expected symbols
            if character in current.transitions:
                panic = False
                current = current.transitions[character]
                previous = character
                continue

            if panic:
                continue

            # didn't expect this symbol, but already had a valid token
            if current.accepts:
                yield current.accepts
                pending = False

                # after a token we expect only whitespace and punctuation
                if character not in separators and previous not in separators:
                    error = LexicalError(
                        line_number,
                        column_number,
                        (
                            'Expected whitespace or punctuation '
                            f'after {repr(current.accepts)}.'
                        ),
                    )
                    errors.append(error)
                    print(error)

                # now reset the automaton and give this character another go
                current = automaton
                if character in current.transitions:
                    panic = False
                    current = current.transitions[character]
                    previous = character
                    continue

            # no tokens start with this symbol
            if not panic and character not in whitespace:
                panic = True
                expected = current.transitions.keys()
                error = LexicalError(
                    line_number,
                    column_number,
                    (
                        f"Expected one of {{{', '.join(expected)}}}, "
                        f'got {repr(character)}.'
                    ),
                )
                errors.append(error)
                print(error)

            current = automaton

        previous = '\n'

    # ran out of characters, but already had a token
    if current.accepts:
        yield current.accepts
    # reached EOF while scanning
    elif pending:
        expected = current.transitions.keys()
        error = LexicalError(
            line_number,
            column_number,
            (
                f"Expected one of {{{', '.join(expected)}}}, "
                f'reached EOF.'
            ),
        )
        errors.append(error)
        print(error)

    return errors
