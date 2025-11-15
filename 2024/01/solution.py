import numpy as np
from pathlib import Path


def solve1(input_path: Path):
    id_data = np.loadtxt(input_path, dtype=np.int32)
    left = np.sort(id_data[:, 0])
    right = np.sort(id_data[:, 1])
    return np.sum(np.abs(left - right)) 

def solve2(input_path: Path):
    id_data = np.loadtxt(input_path, dtype=np.int32)
    left = np.sort(id_data[:, 0])
    right = np.sort(id_data[:, 1])

    rep = np.repeat(left[:, np.newaxis], len(left), axis=1)
    return np.sum(np.sum(rep == right, axis=1) * left)


def test_example():
    assert solve1(Path(__file__).parent/"example_input.txt") == 11
    assert solve2(Path(__file__).parent/"example_input.txt") == 31

if __name__ == "__main__":
    print(f"Solution 1: {solve1(Path(__file__).parent/"input.txt")}")
    print(f"Solution 2: {solve2(Path(__file__).parent/"input.txt")}")