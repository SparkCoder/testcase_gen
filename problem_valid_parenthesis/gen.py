from typing import Callable

import random


def solution(std_input: str) -> str:
    LR_map = {
        ')': '(',
        '}': '{',
        ']': '[',
    }
    stack = []

    for c in std_input.strip():
        if c in LR_map.values():
            stack.append(c)
        elif c in LR_map.keys():
            if len(stack) == 0:
                return 'false'
            top = stack.pop()
            if top != LR_map[c]:
                return 'false'
    return 'true' if len(stack) == 0 else 'false'


def generate_inputs(index: int) -> str:
    random.seed(index)
    rand_yes_no: Callable = lambda: random.randint(1, 100) > 50

    L = '({['
    R = ')}]'
    max_len = 10**4
    max_len = 10

    seq = ''

    stack = []
    count = random.randint(1, max_len / 2)

    while count > 0:
        close = rand_yes_no()
        if close and len(stack) > 0:
            closed = stack.pop()
            seq += R[closed]
            continue
        pick = random.randint(0, len(L)-1)
        stack.append(pick)
        seq += L[pick]
        count -= 1

    while len(stack) > 0:
        closed = stack.pop()
        seq += R[closed]

    fail = rand_yes_no()
    if fail:
        rem_count = random.randint(1, len(seq) - 1)
        rem_count = rem_count-1 if (rem_count % 2) == 0 else rem_count
        for _ in range(rem_count):
            cut_i = random.randint(0, len(seq) - 1)
            seq = seq[:cut_i] + seq[cut_i + 1:]

    return seq
