import re

import aoc

data = aoc.getLinesForDay(2)
# data = aoc.getLinesForDay(2, force_filepath="inputs/day02_example.txt")


part1Sum = 0
MAX_VALUES = {"red": 12, "green": 13, "blue": 14}


def isFakeGame(draws, MAX_VALUES):
    for draw in draws:
        colors = [c.strip() for c in draw.split(",")]
        for c in colors:
            for COLOR in MAX_VALUES.keys():
                if COLOR in c:
                    value = int(re.findall(r"\d+", c)[0])
                    if value > MAX_VALUES[COLOR]:
                        return True
                    break
            else:
                raise Exception(f"Could not find color in {c}")
    return False


# Parse data and count fake games
for idx, line in enumerate(data):
    line = line.split(":")[1]
    draws = [d.strip() for d in line.split(";")]
    isFake = isFakeGame(draws, MAX_VALUES)
    part1Sum += 0 if isFake else (idx + 1)

print("Part 1", part1Sum)

# 7060 too high (bad logic which meant I was counting the number of balls)
# 2681 too high (bad instructions reading, I was counting the number of fake games instead of summing their IDs)

part2Sum = 0

for idx, line in enumerate(data):
    line = line.split(":")[1]
    draws = [d.strip() for d in line.split(";")]
    min_cubes = {"red": 0, "green": 0, "blue": 0}
    for draw in draws:
        colors = [c.strip() for c in draw.split(",")]
        for c in colors:
            for COLOR in MAX_VALUES.keys():
                if COLOR in c:
                    value = int(re.findall(r"\d+", c)[0])
                    if value > min_cubes[COLOR]:
                        min_cubes[COLOR] = value

    power = min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]
    part2Sum += power

print("Part 2", part2Sum)

# x too low (min_cubes should actually be the largest value observed for that color, not the smallest)
