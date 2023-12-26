from typing import NamedTuple
import string

import aoc

data = aoc.getLinesForDay(22)
# data = aoc.getLinesForDay(22, force_filepath="inputs/day22_example.txt")

Name = str


class Cube(NamedTuple):
    name: Name
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int


class Point(NamedTuple):
    x: int
    y: int
    z: int


cubes: set[Cube] = set()

for lineIdx, line in enumerate(data):
    cub1Raw, cub2Raw = line.split("~")
    cub1 = [int(val) for val in cub1Raw.split(",")]
    cub2 = [int(val) for val in cub2Raw.split(",")]
    name = string.ascii_letters[lineIdx % len(string.ascii_letters)]  # example naming
    name = "C" + str(len(cubes)).zfill(4)  # full input naming
    cubes.add(
        Cube(
            name,
            cub1[0],
            cub1[1],
            cub1[2],
            cub2[0],
            cub2[1],
            cub2[2],
        )
    )

print("Found", len(cubes), "cubes")


def yieldInnerPoints(c: Cube):
    for x in range(min(c.x1, c.x2), max(c.x1, c.x2) + 1):
        for y in range(min(c.y1, c.y2), max(c.y1, c.y2) + 1):
            for z in range(min(c.z1, c.z2), max(c.z1, c.z2) + 1):
                yield Point(x, y, z)


assert len(list(yieldInnerPoints(Cube("A", 1, 0, 0, 10, 0, 0)))) == 10


def doCubesIntersect(c1: Cube, c2: Cube) -> bool:
    if any(
        [
            max(c1.x1, c1.x2) < min(c2.x1, c2.x2),
            max(c2.x1, c2.x2) < min(c1.x1, c1.x2),
            max(c1.y1, c1.y2) < min(c2.y1, c2.y2),
            max(c2.y1, c2.y2) < min(c1.y1, c1.y2),
            max(c1.z1, c1.z2) < min(c2.z1, c2.z2),
            max(c2.z1, c2.z2) < min(c1.z1, c1.z2),
        ]
    ):
        return False

    return True


assert doCubesIntersect(Cube("A", 0, 0, 0, 1, 0, 0), Cube("B", 1, 0, 0, 1, 1, 0))


def getFallenCube(c: Cube, cubes: set[Cube]) -> Cube:
    # Return c if it falls by one step
    # c can be blocked by other cubes in cubes

    if min(c.z1, c.z2) == 1:
        touchesGround.add(c.name)
        return c

    newC = Cube(c.name, c.x1, c.y1, c.z1 - 1, c.x2, c.y2, c.z2 - 1)

    restOn[c.name] = set()
    for otherC in cubes:
        if otherC is c:
            continue

        if doCubesIntersect(newC, otherC):
            restOn[c.name].add(otherC.name)

    if len(restOn[c.name]) > 0:
        return c
    return newC


restOn: dict[Name, set[Name]] = dict()
touchesGround: set[Name] = set()

print("Stabilizing")
stabilizedCubesCnt = 0
while stabilizedCubesCnt != len(cubes):
    print("new step")
    stabilizedCubesCnt = 0
    newCubes: set[Cube] = set()
    for c in cubes:
        # Make cube fall by 1 step
        fallenCube = getFallenCube(c, cubes)
        newCubes.add(fallenCube)
        if fallenCube == c:
            stabilizedCubesCnt += 1

    print("Stabilized", stabilizedCubesCnt)
    cubes = newCubes


# for c in restOn:
#     print(c, restOn[c])

part1Count = 0
part2Count = 0
for c in cubes:
    if all(
        [
            (
                len(restOn[c2Name]) == 0
                or len(restOn[c2Name]) > 1
                or c.name not in restOn[c2Name]
                or c2Name in touchesGround
            )
            for c2Name in restOn.keys()
        ]
    ):
        part1Count += 1
    else:
        # Disintegrate c causes at least 1 cube to fall
        # Count the cascade reaction
        # print(c.name, "will cause falling cubes")
        fallenCubes: set[Name] = set([c.name])
        stabilized = False
        while not stabilized:
            stabilized = True
            for c2 in cubes:
                if c2 == c:
                    continue
                if c2.name not in restOn:
                    continue
                if c2.name in fallenCubes:
                    continue
                if all([restingC in fallenCubes for restingC in restOn[c2.name]]):
                    # print("\t", c2.name)
                    fallenCubes.add(c2.name)
                    stabilized = False
        part2Count += len(fallenCubes) - 1
print("Part 1", part1Count)
print("Part 2", part2Count)


# 924274 Too high
