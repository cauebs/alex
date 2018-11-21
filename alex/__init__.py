from dataclasses import dataclass, field
from typing import Optional, Dict, Iterable, NamedTuple, List, Generator


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
    expected: List[str]


def alex(string: str) -> Generator[str, None, List[LexicalError]]:
    keywords = [
        'basic', 'num', 'real', 'id', 'true', 'false',
        'break', 'do', 'else', 'if', 'then', 'while'
    ]

    symbols = [
        '!', '!=', '&&', '(', ')', '+', '/', ';', '<', '<=', '=', '==', '>',
        '>=', '[', ']', '{', '||', '}', '−', '∗',
    ]

    automaton = tokens_to_trie(keywords + symbols)
    current = automaton

    errors = []

    for line_number, line in enumerate(string.splitlines()):
        for column_number, character in enumerate(line):
            # received one of the expected symbols
            if character in current.transitions:
                current = current.transitions[character]
                continue

            # didn't expect this symbol, but already had a valid token
            if current.accepts:
                yield current.accepts

            # go back to the beginning
            current = automaton
            if character in current.transitions:
                current = current.transitions[character]
                continue

            # no tokens start with this symbol
            errors.append(LexicalError(
                line_number,
                column_number,
                list(current.transitions.keys())
            ))

    # no more symbols available, but already had a valid token
    if current.accepts:
        yield current.accepts

    return errors
