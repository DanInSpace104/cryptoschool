from functools import lru_cache
from itertools import cycle
from string import ascii_letters, ascii_lowercase
from typing import Dict

Char = str


@lru_cache(maxsize=None)
def generate_vignere_table() -> Dict[Char, Dict[Char, Char]]:
    table = {}
    letter_cycle = cycle(ascii_lowercase)
    for a in ascii_lowercase:
        table[a] = {b: next(letter_cycle) for b in ascii_lowercase}
        next(letter_cycle)
    return table


def vigenere_cipher(text: str, key: str) -> str:
    vignere_table = generate_vignere_table()
    m = len(key)
    result = list(text)
    # that shift is needed because non letters is not counted, so index is different
    # at least it works that way on https://cryptii.com/pipes/vigenere-cipher
    delta = 0
    for i, char in enumerate(text):
        if char not in ascii_letters:
            delta += 1
            continue
        result[i] = vignere_table[char.lower()][key[i % m - delta % m]]
        if not char.islower():
            result[i] = result[i].upper()
    return ''.join(result)


def test_vignere_cipher():
    cases = (
        ('Hello', 'asdfg', 'Hwoqu'),
        ('Hello', 'aaaaa', 'Hello'),
        ('Thequick', 'asdfue', 'Tzhvomcc'),
        ('The quick', 'asdfue', 'Tzh vomcc'),
        (
            'The quick brown fox jumps over 13 lazy dogs.',
            'asdfue',
            'Tzh vomcc ewian xrc dymhv tpir 13 ddes hoyv.',
        ),
        (
            'The quick brown fox jumps over 13 lazy dogs.',
            'udfdhasdipoijqjnwefpoijsdoivijiwejcaojsdcoiajef',
            'Nkj tbiun jgcew vxk fyreg wewu 13 ziug mwcw.',
        ),
    )
    for text, key, encrypted in cases:
        assert vigenere_cipher(text, key) == encrypted
