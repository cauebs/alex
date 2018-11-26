from alex import alex


def tokens_and_errors(string):
    errors = None

    def do_it():
        nonlocal errors
        errors = yield from alex(string)

    tokens = list(t.token for t in do_it())

    return tokens, errors
