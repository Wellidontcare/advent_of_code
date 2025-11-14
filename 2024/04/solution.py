import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import scipy.signal as sig


def create_match_mask():
    base = np.vectorize(lambda x: ord(x) if x else 0)(
        np.array(
            [["\0", "\0", "\0", "\0"], ["X", "M", "A", "S"], ["\0", "\0", "\0", "\0"]],
            dtype=str,
        )
    ).astype(np.int32)
    diagonal = np.vectorize(lambda x: ord(x) if x else 0)(
        np.array(
            [
                ["X", "\0", "\0", "\0"],
                ["\0", "M", "\0", "\0"],
                ["\0", "\0", "A", "\0"],
                ["\0", "\0", "\0", "S"],
            ],
            dtype=str,
        )
    ).astype(np.int32)

    return [
        base,
        np.fliplr(base),
        np.rot90(base),
        np.flipud(np.rot90(base)),
        diagonal,
        np.fliplr(diagonal),
        np.flipud(diagonal),
        np.fliplr(np.flipud(diagonal)),
    ], sum(ord(c) ** 2 for c in "XMAS")


def create_match_mask_2():
    d = np.vectorize(lambda x: ord(x) if x else 0)(
        np.array([["M", "\0", "\0"], ["\0", "A", "\0"], ["\0", "\0", "S"]], dtype=str)
    ).astype(np.int32)
    d2 = np.vectorize(lambda x: ord(x) if x else 0)(
        np.array([["\0", "\0", "M"], ["\0", "A", "\0"], ["S", "\0", "\0"]], dtype=str)
    ).astype(np.int32)
    d3 = np.vectorize(lambda x: ord(x) if x else 0)(
        np.array([["S", "\0", "\0"], ["\0", "A", "\0"], ["\0", "\0", "M"]], dtype=str)
    ).astype(np.int32)
    d4 = np.vectorize(lambda x: ord(x) if x else 0)(
        np.array([["\0", "\0", "S"], ["\0", "A", "\0"], ["M", "\0", "\0"]], dtype=str)
    ).astype(np.int32)
    templates = [d + d2, d3 + d4, d + d4, d2 + d3]
    for t in templates:
        t[1, 1] = ord("A")
    return templates, sum(ord(c) ** 2 for c in "MASMS")


def solve(path, template_func):
    with open(path) as file:
        data = []
        for line in file.read().split("\n"):
            data.append([ord(c) for c in line])
        data = np.array(data)
        full_count = 0
        templates, match_num = template_func()
        for template in templates:
            res = sig.correlate2d(data, template, mode="full")
            count = np.count_nonzero(res == match_num)
            full_count += count
        return full_count


def solve1(path):
    return solve(path, create_match_mask)


def solve2(path):
    return solve(path, create_match_mask_2)


def test_xmas():
    path = Path(__file__).parent / "sample_input.txt"
    assert solve1(path) == 18
    assert solve2(path) == 9


if __name__ == "__main__":
    path = Path(__file__).parent / "input.txt"
    print(f"Solution 1: {solve1(path)}")
    print(f"Solution 2: {solve2(path)}")
