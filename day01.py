import re

import aoc

# data = aoc.getLinesForDay(1, force_filepath="inputs/day01_example.txt")
data = aoc.getLinesForDay(1)

part1Sum = 0


for line in data:
    line = re.sub(r"[a-z]", "", line)
    calibValue = int(line[0] + line[-1])
    part1Sum += calibValue

print("Part 1", part1Sum)
part2Sum = 0

for line in data:
    CAPTURE_MAP = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    capturedDigits = []
    for charIdx, char in enumerate(line):
        for pattern in CAPTURE_MAP.keys():
            if line[charIdx : charIdx + len(pattern)] == pattern:
                capturedDigits.append(CAPTURE_MAP[pattern])

    calibValue = int(str(capturedDigits[0]) + str(capturedDigits[-1]))
    part2Sum += calibValue

print("Part 2", part2Sum)

# x too low (bad string to int conversion)
# x too low (typo in regex)
# x too low (had to rewrite the whole part 2 to take merged digits into account (eg. oneight)
