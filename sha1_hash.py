from itertools import zip_longest


def chunker(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def prepare_msg(message: str) -> bytes:
    message = message.encode()
    msg = message + b'\x80'  # append bit '1'
    # add '0' bits so there is place for 64-bit length of message
    msg += b'\x00' * (56 - len(msg) % 64)  # 64 - len - 8
    # add length of source message in bits
    msg += (len(message) * 8).to_bytes(length=8, byteorder='big')
    return msg


def mask(x):
    return x & 0xFFFFFFFF


def rotate_left(num, steps=1):
    """Left rotate a 32-bit integer n by b bits."""
    return mask(((num << steps) | (num >> (32 - steps))))


def sha1_hash(message: str) -> str:
    h = [
        0x67452301,
        0xEFCDAB89,
        0x98BADCFE,
        0x10325476,
        0xC3D2E1F0,
    ]
    # bits converted to bytes when needed
    msg: bytes = prepare_msg(message)
    for chunk in chunker(msg, 64, 0):
        w = [int.from_bytes(bytes(x), 'big') for x in chunker(chunk, 4)]
        for i in range(16, 80):
            w.append(rotate_left(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]))

        a, b, c, d, e = h
        for i in range(80):
            if i < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif i < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif i < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            temp = rotate_left(a, 5) + f + e + k + w[i]
            e = d
            d = c
            c = rotate_left(b, 30)
            b = a
            a = mask(temp)
        h = [mask(x + y) for x, y in zip(h, (a, b, c, d, e))]
    # return "%08x%08x%08x%08x%08x" % tuple(h)  # idk how that works
    return ''.join([f'{x:0{8}x}' for x in h])


def test_sha1_hash():
    # Test cases from wikipedia
    cases = (
        (
            'The quick brown fox jumps over the lazy dog',
            '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12',
        ),
        ('', 'da39a3ee5e6b4b0d3255bfef95601890afd80709'),
        (
            'В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!',
            '9e32295f8225803bb6d5fdfcc0674616a4413c1b',
        ),
        ('sha', 'd8f4590320e1343a915b6394170650a8f35d6926'),
    )

    for text, hash in cases:
        assert sha1_hash(text) == hash

    # Test on random data
    import hashlib
    import random

    for _ in range(100):
        case = str(random.random())
        tested = sha1_hash(case)
        correct = hashlib.sha1(case.encode()).hexdigest()
        assert tested == correct
