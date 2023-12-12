import functools

import aoc

Hint = tuple[int, ...]

data = aoc.getLinesForDay(12)
data = aoc.getLinesForDay(12, force_filepath="inputs/day12_example.txt")
# data = aoc.getLinesForDay(12, force_filepath="inputs/day12_one_line.txt")

lines: list[str] = []
hints: list[Hint] = []

# Parsing

for line in data:
    _l, _h = line.split()
    lines.append(_l)
    hints.append(tuple([int(x) for x in _h.split(",")]))


@functools.cache
def countValidReplacements(line: str, hint: Hint) -> int:
    # print(line, hint)
    if len(line) == 0:
        # print("empty line")
        return 1 if len(hint) == 0 else 0

    if len(hint) == 0:
        # print("empty hints")
        return 1 if "#" not in line else 0

    if sum(hint) > line.count("#") + line.count("?"):
        # print("not enough pounds")
        return 0

    if line.count("#") > sum(hint):
        # print("too much pounds")
        return 0

    count = 0
    while line[0] == ".":
        line = line[1:]

    assert line[0] in "#?"
    firstPatternLength = hint[0]
    pattern = line[:firstPatternLength]
    firstCharAfterPattern = (
        line[firstPatternLength] if len(line) > firstPatternLength else "."
    )
    if "." in pattern or firstCharAfterPattern == "#":
        # Cannot replace here
        if line[0] == "#":
            # print("dead end")
            return 0
        assert line[0] == "?"
        # skip and do not count
        # print("must skip")
        return countValidReplacements(line[1:], hint)
    if len(pattern) == pattern.count("#") and firstCharAfterPattern == ".":
        # Pattern is hardcoded, skip it
        # print("must consume (harcoded)")
        return countValidReplacements(line[firstPatternLength:], hint[1:])

    # Pattern is achievable at this location
    if line[0] == "?":
        # We have two possibilities : replace it now or not
        countReplaceNow = countValidReplacements(
            line[firstPatternLength + 1 :], hint[1:]
        )
        # If we skip, we need to skip until the next "." or "?"
        skipLenght = 1
        while skipLenght < len(line) and line[skipLenght] == "#":
            skipLenght += 1
        countSkipThisChar = countValidReplacements(line[skipLenght:], hint)
        # print("multiverse")
        # print(line, hint, countReplaceNow, "+", countSkipThisChar)
        count = countReplaceNow + countSkipThisChar
    else:
        assert line[0] == "#"
        # Pattern must be consumed immediately
        # print("must consume (starts with #)")
        return countValidReplacements(line[firstPatternLength + 1 :], hint[1:])

    return count


# Count part 1
part1Sums = []

for idx, (line, hint) in enumerate(zip(lines, hints)):
    lineSum = 0
    part1Sums.append(countValidReplacements(line, hint))

print("Part 1", sum(part1Sums))
print(aoc.getTick())


# Validate logic with example
assert countValidReplacements("???.###", (1, 1, 3)) == 1
assert countValidReplacements(".??..??...?##.", (1, 1, 3)) == 4
assert countValidReplacements("?#?#?#?#?#?#?#?", (1, 3, 1, 6)) == 1
assert countValidReplacements("????.#...#...", (4, 1, 1)) == 1
assert countValidReplacements("????.######..#####.", (1, 6, 5)) == 4
assert countValidReplacements("?###????????", (3, 2, 1)) == 10


def unfoldLine(line):
    return "?".join([line] * 5)


def unfoldHint(hint):
    return tuple([*hint * 5])


# Count part 2
part2Sums = []
for idx, (line, hint) in enumerate(zip(lines, hints)):
    line = unfoldLine(line)
    hint = unfoldHint(hint)
    part2Sums.append(countValidReplacements(line, hint))

print("Part 2", sum(part2Sums))
print(aoc.getTick())

# Answer is too low for input but works on all examples
# Unfortunately I don't have more time to debug it :(
