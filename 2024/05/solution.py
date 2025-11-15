from pathlib import Path
import numpy as np


def read_input(s: str):
    numbers = {}
    for line in s.split("\n"):
        if line == "":
            break
        if not line:
            continue
        ordering = line.strip().split("|")
        first = int(ordering[0].strip())
        second = int(ordering[1].strip())
        if first in numbers:
            numbers[first].append(second)
        else:
            numbers[first] = [second]
    messages = []
    for line in s[s.find("\n\n") :].split("\n"):
        if line.strip():
            messages.append([int(c) for c in line.strip().split(",")])

    return numbers, messages


def check_message(message: list[int], rules: dict[int, list[int]]) -> int | None:
    # step backward through the numbers
    for i, num in enumerate(reversed(message)):
        if num in rules:
            # check the other numbers forward
            for j in range(len(message) - i):
                # if any number in the forward pass appears is the has to be before rule of that number
                # violation!
                if message[j] in rules[num]:
                    return None
    return message[len(message) // 2]


def reorder_faulty_message(
    faulty_message: list[int], rules: dict[int, list[int]]
) -> int:
    j = 0
    # bubble sort yeah!
    swapped = False
    while j < len(faulty_message) - 1 or swapped:
        swapped = False
        j = 0
        for i in range(len(faulty_message) - 1):
            if (
                faulty_message[i] in rules
                and faulty_message[i + 1] in rules[faulty_message[i]]
            ):
                faulty_message[i], faulty_message[i + 1] = (
                    faulty_message[i + 1],
                    faulty_message[i],
                )
                swapped = True
            j += 1
    return list(reversed(faulty_message))[len(faulty_message) // 2]


def solve1(path: Path) -> int:
    with open(path) as file:
        rules, messages = read_input(file.read())
        valid_sum = 0
        for idx, message in enumerate(messages):
            result = check_message(message, rules)
            if result is not None:
                valid_sum += result
    return valid_sum


def solve2(path: Path) -> int:
    with open(path) as file:
        rules, messages = read_input(file.read())
        valid_sum = 0
        for idx, message in enumerate(messages):
            result = check_message(message, rules)
            if result is None:
                result = reorder_faulty_message(message, rules)
                valid_sum += result
    return valid_sum


def test_read_rules():
    path = Path(__file__).parent / "sample_input.txt"
    assert solve1(path) == 143
    assert solve2(path) == 123


if __name__ == "__main__":
    print(f"Solution 1: {solve1(Path(__file__).parent / 'input.txt')}")
    print(f"Solution 2: {solve2(Path(__file__).parent / 'input.txt')}")
