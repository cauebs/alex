from alex import alex


def tokens_and_errors(string):
    errors = None

    def do_it():
        nonlocal errors
        errors = yield from alex(string)

    tokens = list(do_it())

    return tokens, errors
