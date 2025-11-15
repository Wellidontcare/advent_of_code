from pathlib import Path
import numpy as np
import numpy.ma as ma

# use a masked array to get around the variable col count of the input data
def read_input_as_masked_array(input_data):
    # pad with nan to max row length
    data = [[int(col) for col in line.strip().split(' ') if col] for line in input_data.split('\n') if line]
    max_len = max([len(line) for line in data])
    for line in data:
        if len(line) < max_len:
            line.extend([float('nan')]*(max_len - len(line)))
    return ma.array(np.array(data), mask=np.isnan(np.array(data)))


def line_is_safe(reactor_data, axis=None):
    adjacent_diffs = np.diff(reactor_data)
    safe = np.all(adjacent_diffs < 0, axis=axis) | np.all(adjacent_diffs > 0, axis=axis)
    abs_adjacent_diffs = np.abs(adjacent_diffs)
    return safe & np.all((abs_adjacent_diffs != 0) & (abs_adjacent_diffs < 4), axis=axis)

def solve1(input_file_path) -> int:
    with open(input_file_path) as file:
        reactor_data = read_input_as_masked_array(file.read())
        safe = line_is_safe(reactor_data, axis=1)
        return np.count_nonzero(safe)

def solve2(input_file_path) -> int:
    with open(input_file_path) as file:
        reactor_data = read_input_as_masked_array(file.read())
        safe_lines = 0
        for line in reactor_data:
            line_safe = False
            for i in range(len(line) + 1):
                if i != 0:
                    value = line[i - 1]
                    line[i - 1] = ma.masked
                if line.count() < 2:
                    continue
                compressed = line.compressed()
                safe = line_is_safe(compressed)
                if i != 0:
                    line[i - 1] = value
                line_safe = line_safe or safe

                if line_safe:
                    break
            if line_safe:
                safe_lines += 1
        return safe_lines

def test_example():
    assert solve1(Path(__file__).parent/"example_input.txt") == 2
    assert solve2(Path(__file__).parent/"example_input.txt") == 4

if __name__ == "__main__":
    print(f"Solution 1: {solve1(Path(__file__).parent/"input.txt")}")
    print(f"Solution 2: {solve2(Path(__file__).parent/"input.txt")}")