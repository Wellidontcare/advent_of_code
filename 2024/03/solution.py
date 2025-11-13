import numpy as np
import re
from pathlib import Path

def solve(test_file_path: Path) -> int:
    mul_regex = re.compile(r"mul\((\d+),(\d+)\)")
    with open(test_file_path) as file:
        matches = mul_regex.findall(file.read())
        return sum([int(a)*int(b) for a, b in matches])

def solve2(test_file_path: Path):
    mul_regex = re.compile(r"mul\((\d+),(\d+)\)")
    # we have to match lazy
    dont_regex = re.compile(r"don't\(\)[\s\S]*?do\(\)")
    with open(test_file_path) as file:
        # remove all blocks that are enclosed in don't()...do()
        cleaned = dont_regex.sub("", file.read())
        # remove the last don't which may not be enabled again
        cleaned = cleaned[:str.rfind(cleaned, "don't()")]
        matches = mul_regex.findall(cleaned)
        return sum([int(a)*int(b) for a, b in matches])


def test_regex():
    assert solve(Path(__file__).parent/"test_input.txt") == 161

def test_regex2():
    assert solve2(Path(__file__).parent/"test_input_2.txt") == 48


if __name__ == "__main__":
    print(f"Solution 1: {solve(Path(__file__).parent/"input.txt")}")
    print(f"Solution 2: {solve2(Path(__file__).parent/"input.txt")}")