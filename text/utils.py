from unicodedata import normalize


def clean_text(text):
    """
    Returns a cleaned up copy of a string by removing non-ASCII characters
    and converting the text to lower case, thus making it easier to compare strings.

    By removing non-ASCII characters, accentuation marks and emojis
    are also removed, among others.

    :param str text: the text that will be cleaned up
    :return str: the cleaned up text

    >>> clean_text('[MáTRÍCÚLÃ] ç:/ áàãâä! éèêë? íìîï, óòõôö; úùûü ªº 🧓\U0001F4C3.')
    '[matricula] c:/ aaaaa! eeee? iiii, ooooo; uuuu ao .'
    """
    return remove_accentuation(text).lower()


def remove_accentuation(txt):
    """
    Removes all non-ASCII characters from a string, which includes
    accentuation marks and emojis. When possible it replaces the
    characters with an ASCII alternative, thus 'ã' becomes 'a' and
    'ª' becomes 'a'.
    Based on https://wiki.python.org.br/RemovedorDeAcentos

    >>> remove_accentuation('[ACENTUAÇÃO] ç:/ áàãâä! éèêë? íìîï, óòõôö; úùûü ªº 🧓\U0001F4C3.')
    '[ACENTUACAO] c:/ aaaaa! eeee? iiii, ooooo; uuuu ao .'
    """
    return normalize('NFKD', txt).encode('ascii', 'ignore').decode('utf-8')


if __name__ == '__main__':
    # run the tests described in the docstrings
    from doctest import testmod
    testmod()
