import re

import aoc


data = aoc.getCellsForDay(3)
# data = aoc.getCellsForDay(3, force_filepath="inputs/day03_example.txt")

# Trick:
# Add a space after each line to avoid border effects (= complex logic when a number is at the end of a line)
data = [line + ["."] for line in data]


# Parse the structure to extract numbers and symbols info

listOfNumbers = []  # tuple: (value, y, xStart, xEnd)
listOfSymbols = []  # tuple: (value, y, x)

currentNumberStart = None  # temp var when reading a number

for y, line in enumerate(data):
    for x, cell in enumerate(line):
        if re.match(r"\d", cell):
            if currentNumberStart is None:
                currentNumberStart = (y, x)
        else:
            if currentNumberStart is not None:
                numberStart = currentNumberStart[1]
                number = int("".join(line[numberStart:x]))
                listOfNumbers.append((number, y, numberStart, x - 1))
                # print("Added", listOfNumbers[-1])
                currentNumberStart = None

            if cell != ".":
                listOfSymbols.append((cell, y, x))


def isTwoCellsAdjacent(y1, x1, y2, x2):
    # We assume (y1, x1) and (y2, x2) are different
    # Note that adjacent = horizontal, vertical or diagonal
    return abs(y2 - y1) <= 1 and abs(x2 - x1) <= 1


def isAdjacent(numberInfo, symbolInfo):
    numY = numberInfo[1]
    for numX in range(numberInfo[2], numberInfo[3] + 1):
        if isTwoCellsAdjacent(numY, numX, symbolInfo[1], symbolInfo[2]):
            return True
    return False


def isPartNumber(numberInfo, listOfSymbols):
    for symbolInfo in listOfSymbols:
        if isAdjacent(numberInfo, symbolInfo):
            return True
    return False


listOfPartNumbers = [
    numberInfo
    for numberInfo in listOfNumbers
    if isPartNumber(numberInfo, listOfSymbols)
]

print("Part 1", sum([numberInfo[0] for numberInfo in listOfPartNumbers]))

# x too low (I was just counting the parts and not adding their values)


# Part 2


def getGearRatio(symbolInfo, listOfPartNumbers):
    """If symbolInfo is not a gear, return None"""

    if symbolInfo[0] != "*":
        return None

    adjacents = []
    for numberInfo in listOfPartNumbers:
        if isAdjacent(numberInfo, symbolInfo):
            adjacents.append(numberInfo)
    if len(adjacents) == 2:
        return adjacents[0][0] * adjacents[1][0]
    return None


part2Accumulator = 0
for symbolInfo in listOfSymbols:
    gearRatio = getGearRatio(symbolInfo, listOfPartNumbers)
    print(symbolInfo, gearRatio)
    part2Accumulator += gearRatio or 0

print("Part 2", part2Accumulator)
