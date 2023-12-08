import math

import aoc

data = aoc.getLinesForDay(8)

# Parse input

instructions = data[0]
rulesRaw = data[2:]

rules = {}
for line in rulesRaw:
    [source, LR] = line.split(" = ")
    L = LR.split(", ")[0][1:]
    R = LR.split(", ")[1][:-1]
    rules[source] = (L, R)

# Explore paths


def getNbOfStepsForPath(startLocation, targetCondition):
    stepIdx = 0
    currentLocation = startLocation
    while stepIdx < 1000000:
        direction = instructions[stepIdx % len(instructions)]
        assert direction in "LR"
        if direction == "L":
            nextLocation = rules[currentLocation][0]
        else:
            nextLocation = rules[currentLocation][1]

        currentLocation = nextLocation
        stepIdx += 1

        if targetCondition(currentLocation):
            break

    return stepIdx


print("Part 1", getNbOfStepsForPath("AAA", lambda n: n == "ZZZ"))


# Part 2

# Assumption: each startNode (end with A) only encounters one endNode (end with Z) in its loop
# 🍀 We are lucky, the assumption is correct. We can simply use the LCM of each period

startNodesPeriods = []
for startNode in rules.keys():
    if startNode[-1] == "A":
        startNodesPeriods.append(getNbOfStepsForPath(startNode, lambda n: n[-1] == "Z"))


print("Part 2", math.lcm(*startNodesPeriods))
