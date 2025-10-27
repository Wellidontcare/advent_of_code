import numpy as np


def solve(input_path: str):
    id_data = np.loadtxt(input_path, dtype=np.int32)
    left = np.sort(id_data[:, 0])
    right = np.sort(id_data[:, 1])
    return np.sum(np.abs(left - right)) 

def test_example():
    assert solve("example_input.txt") == 11

if __name__ == "__main__":
    print(solve("./input.txt"))
