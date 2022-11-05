from typing import Tuple

import random


def check(inp: str, out: str) -> bool:
    comp = {
        '(': ')',
        '[': ']',
        '{': '}',
    }
    win = {
        'false': False,
        'true': True
    }
    stack = []
    for c in inp:
        if c in comp.keys():
            stack.append(c)
        elif not stack:
            return not win[out]
        elif comp[stack.pop()] != c:
            return not win[out]
    if stack:
        return not win[out]
    return win[out]


def generate(index: int) -> Tuple[str, str]:
    L = '({['
    R = ')}]'

    seq = ''
    max_len = 10**4

    random.seed(index)
    def gen_rand(): return (random.randint(1, 100) > 50)

    fail = gen_rand()
    if fail:
        spc = gen_rand()
        if spc:
            seq = random.choice(L if gen_rand() else R)
        else:
            odd = gen_rand()
            if odd:
                count = (random.randint(1, max_len//2) * 2) - 1
                seq = ''.join((random.choice(L if random.randint(
                    1, 100) > 50 else R)) for _ in range(count))
            else:
                count = random.randint(1, max_len//4) * 2
                choices = [random.randint(0, len(L) - 1) for _ in range(count)]
                L_l = [L[i] for i in choices]
                R_l = [R[i] for i in choices[::-1]]
                seq_l = [v for v in L_l]
                mutation_count = random.randint(1, count)
                if mutation_count > 0:
                    for _ in range(mutation_count):
                        mutation_index = random.randint(0, len(seq_l)-1)
                        seq_l = seq_l[:mutation_index] + \
                            [R_l.pop(random.randint(0, len(R_l)-1))] + \
                            seq_l[mutation_index:]
                seq_l += R_l
                seq = ''.join(seq_l)
    else:
        count = random.randint(1, max_len//2)
        choices = [random.randint(0, len(L) - 1) for _ in range(count)]
        seq = ''.join([L[i] for i in choices]) + \
            ''.join([R[i] for i in choices[::-1]])
    return seq, str(not fail).lower()
