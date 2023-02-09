import datetime
import multiprocessing
import secrets

from utils import wait_for_enter_and_clear as wait


def key_options(bit_len: int) -> int:
    return int('1' * bit_len, 2) + 1


def generate_random_key_value(bit_len: int) -> int:
    return secrets.randbits(bit_len)


def bruteforce(answer, start, max_n, flag):
    try:
        for i in range(start, max_n):
            if flag.value == 1:
                return
            if i == answer:
                flag.value = 1
                return True
    except KeyboardInterrupt:
        return


def bruteforce_one_core(answer, max_n):
    begin = datetime.datetime.now()
    print('Started at:', begin)

    res = bruteforce(answer, 0, max_n, multiprocessing.Value('i', 0))
    if not res:
        return

    end = datetime.datetime.now()
    print('Number found at:', end)
    print('It took only:', end - begin)


def bruteforce_multiprocessing(answer, max_n):
    cpus = multiprocessing.cpu_count()
    print('CPU count:', cpus)

    begin = datetime.datetime.now()
    print('Started at:', begin)

    chunks = []
    chunk_size = max_n // cpus
    for i in range(cpus):
        chunks.append([i * chunk_size, i * chunk_size + chunk_size])
    chunks[-1][1] += max_n % cpus

    processes = []
    flag = multiprocessing.Value('i', 0)
    for start, end in chunks:
        processes.append(
            multiprocessing.Process(target=bruteforce, args=(answer, start, end, flag))
        )
    [p.start() for p in processes]
    [p.join() for p in processes]

    end = datetime.datetime.now()
    print('Number found at:', end)
    print('It took only:', end - begin)


def test_key_options():
    assert key_options(8) == 256
    assert key_options(16) == 65_536


if __name__ == '__main__':
    bits = [pow(2, n) for n in range(3, 13)]

    print('Calculating the number of key options...')
    key_opts = [key_options(n) for n in bits]
    [print(f'{n} - {k}') for n, k in zip(bits, key_opts)]
    wait()

    print('Generating random values...')
    randoms = [generate_random_key_value(n) for n in bits]
    [print(f'{n} - {k}') for n, k in zip(bits, randoms)]
    wait()

    print('Brute forcing values to find a key.')
    print('Press Ctrl-C any time to stop process and go to the next bits length.')
    use_multiprocessing = input('Do you want to use multiple cores? (Y/n)')
    if use_multiprocessing in ['Y', 'y', '']:
        func = bruteforce_multiprocessing
    else:
        func = bruteforce_one_core

    for i, b in enumerate(bits):
        print('Bit length:', b)
        try:
            func(randoms[i], key_opts[i])
        except KeyboardInterrupt:
            continue
        finally:
            print()
