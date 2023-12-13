from typing import Generator

import aoc

data = aoc.getInputForDay(13)
# data = aoc.getInputForDay(13, force_filepath="inputs/day13_example.txt")

Line = str
Grid = list[Line]

rawGrids = [grids.strip() for grids in data.split("\n\n") if len(grids.strip()) > 0]
grids: list[Grid] = [grid.split("\n") for grid in rawGrids]


def findMirrors(grid: Grid) -> list[dict[str, int]]:
    colFilled: list[set] = []
    for x in range(len(grid[0])):
        colFill = set()
        col = "".join(row[x] for row in grid)
        for y in range(len(grid)):
            if col[y] == "#":
                colFill.add(y)
        colFilled.append(colFill)

    rowFilled: list[set] = []
    for y in range(len(grid)):
        rowFill = set()
        row = grid[y]
        for x in range(len(grid[0])):
            if row[x] == "#":
                rowFill.add(x)
        rowFilled.append(rowFill)

    mirrors: list[dict[str, int]] = []

    # Test possible mirror lines
    # Horizontal
    for mirrorAfterY in range(len(grid) - 1):
        if len(mirrors) > 0 and mirrors[-1].get("y") == mirrorAfterY:
            # Already found
            break

        for deltaY in range(len(grid)):
            if mirrorAfterY - deltaY < 0 or mirrorAfterY + 1 + deltaY >= len(grid):
                mirrors.append({"y": mirrorAfterY})
                break

            line = rowFilled[mirrorAfterY - deltaY]
            mirrorLine = rowFilled[mirrorAfterY + 1 + deltaY]
            if line != mirrorLine:
                break

    # Vertical lines
    for mirrorAfterX in range(len(grid[0]) - 1):
        if len(mirrors) > 0 and mirrors[-1].get("x") == mirrorAfterX:
            # Already found
            break

        for deltaX in range(len(grid[0])):
            if mirrorAfterX - deltaX < 0 or mirrorAfterX + 1 + deltaX >= len(grid[0]):
                mirrors.append({"x": mirrorAfterX})
                break

            col = colFilled[mirrorAfterX - deltaX]
            mirrorCol = colFilled[mirrorAfterX + 1 + deltaX]
            if col != mirrorCol:
                break

    return mirrors


def mirrorValue(mirror):
    return (mirror["x"] + 1) if "x" in mirror else (100 * (mirror["y"] + 1))


part1Sum = 0
areaSum = 0
for gridIdx, grid in enumerate(grids):
    mirrors = findMirrors(grid)
    assert len(mirrors) == 1
    mirror = mirrors[0]
    # Debug print
    # print(gridIdx)
    # for y, line in enumerate(grid):
    #     print(line, end=(" <\n" if mirror.get("y") == y else "\n"))
    # if mirror.get("x"):
    #     print(" " * mirror["x"] + "^")
    # print(mirror)
    part1Sum += mirrorValue(mirror)

    areaSum += len(grid) * len(grid[0])

print("Part 1", part1Sum)

# Part 2
# Brute-force it: generate all smudges and find those that create new mirror lines


def yieldVariations(grid: Grid) -> Generator[Grid, None, None]:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            newGrid = []
            for rowIdx, row in enumerate(grid):
                if rowIdx != y:
                    newGrid.append(row)
                else:
                    smudge = "." if grid[y][x] == "#" else "#"
                    newGrid.append(row[:x] + smudge + row[x + 1 :])
            yield newGrid


part2Sum = 0
for grid in grids:
    mirrors = findMirrors(grid)
    assert len(mirrors) == 1
    originalMirror = mirrors[0]
    for otherGrid in yieldVariations(grid):
        otherMirrors = findMirrors(otherGrid)
        otherMirrors = [m for m in otherMirrors if m != originalMirror]
        if len(otherMirrors) == 1:
            newMirror = otherMirrors[0]
            part2Sum += mirrorValue(newMirror)
            break
    else:
        raise RuntimeError("Could not find other mirror!")
print("Part 2", part2Sum)
print(aoc.getTick())
