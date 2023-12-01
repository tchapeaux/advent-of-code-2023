# Generic functions for use in the puzzles solutions
# Instructions:
# 1. Create a environment.json file and enter your session token as AOC_TOKEN (get it from the dev tools)
# 2. In your scripts, use the following functions:
#     - getInputForDay()    get the raw input
#     - getLinesForDay()    get the input line by line
#     - getCellsForday()    get a 2D table from the input
# If you want to test against the examples, create an example file and use the force_filepath option

# This solution stores the input files to avoid spamming the AoC server
# see https://www.reddit.com/r/adventofcode/comments/3v64sb/aoc_is_fragile_please_be_gentle/

import os
import math
import time
import json
from typing import Any, Iterator, List, Optional, Tuple

GridType = List[List[Any]]

tickWhenLoaded: float = time.time()


def urlForDay(year: int, dayNbr: int) -> str:
    return f"https://adventofcode.com/{year}/day/{dayNbr}/input"


def filepathForDay(dayNbr: int) -> str:
    dayStr: str = str(dayNbr).rjust(2, "0")
    return f"inputs/day{dayStr}_input.txt"


def getInputForDay(dayNbr: int, force_filepath: Optional[str] = None) -> str:
    if force_filepath:
        with open(force_filepath) as f:
            return f.read()

    filepath = filepathForDay(dayNbr)
    if not os.path.exists(filepath):
        import requests

        with open("environment.json") as f:
            environment = json.loads(f.read())

        YEAR = int(environment["YEAR"])
        AOC_TOKEN = environment["AOC_TOKEN"]
        EMAIL = environment["EMAIL"]

        url = urlForDay(YEAR, dayNbr)
        cookies = dict(session=AOC_TOKEN)
        headers = {"User-Agent": "Custom script by " + EMAIL}
        r = requests.get(url, cookies=cookies, headers=headers)
        with open(filepath, "w") as f:
            f.write(r.text)

    with open(filepath) as f:
        return f.read()


def getLinesForDay(dayNbr: int, force_filepath=None) -> List[str]:
    raw = getInputForDay(dayNbr, force_filepath)
    return [l.strip() for l in raw.strip().split("\n")]


def getCellsForDay(dayNbr, force_filepath=None) -> List[List[str]]:
    linesInput = getLinesForDay(dayNbr, force_filepath)
    return [[c for c in l] for l in linesInput if len(l.strip()) > 0]


def getNumberCellsForDay(dayNbr, force_filepath=None) -> List[List[int]]:
    cellsInput = getCellsForDay(dayNbr, force_filepath)
    return [[int(c) for c in row] for row in cellsInput]


def get4Neighbors(grid: GridType, x: int, y: int) -> Iterator[Tuple[int, int, Any]]:
    """yield x, y, value for all N, S, E, W neighbors"""
    if y > 0:
        yield (x, y - 1, grid[y - 1][x])
    if y < len(grid) - 1:
        yield (x, y + 1, grid[y + 1][x])
    if x > 0:
        yield (x - 1, y, grid[y][x - 1])
    if x < len(grid[y]) - 1:
        yield (x + 1, y, grid[y][x + 1])


def get8Neighbors(grid: GridType, x: int, y: int) -> Iterator[Tuple[int, int, Any]]:
    """yield x, y, value for all N, S, E, W neighbors as well as NW, NE, SW, SE"""
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == dx == 0:
                continue
            if y + dy < 0 or y + dy > len(grid) - 1:
                continue
            if x + dx < 0 or x + dx > len(grid[y]) - 1:
                continue

            yield (x + dx, y + dy, grid[y + dy][x + dx])


def manhattanDistance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(y2 - y1) + abs(x2 - x1)


def getTick() -> float:
    return round(time.time() - tickWhenLoaded, 2)
