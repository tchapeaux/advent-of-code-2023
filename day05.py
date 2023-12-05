import re
import aoc

data = aoc.getLinesForDay(5)
# data = aoc.getLinesForDay(5, force_filepath="inputs/day05_example.txt")


initialSeeds = [int(x) for x in re.findall(r"(\d+)", data[0])]
data = data[2:]  # remove initial seeds line

maps = {
    # Keys were hardcoded from the instructions
    "seed-to-soil": set(),
    "soil-to-fertilizer": set(),
    "fertilizer-to-water": set(),
    "water-to-light": set(),
    "light-to-temperature": set(),
    "temperature-to-humidity": set(),
    "humidity-to-location": set(),
}

currentMap = None

# Parse the mapping

for line in data:
    if len(line.strip()) == 0:
        continue

    for mapName in maps.keys():
        if mapName in line:
            currentMap = mapName
            break
    else:
        # Line containing a mapping
        digits = tuple(int(x) for x in line.split())
        assert len(digits) == 3
        maps[currentMap].add(digits)


def getDestination(sourceValue, mapping):
    for mapLine in mapping:
        [startDest, startSource, rangeLength] = mapLine
        if startSource < sourceValue < startSource + rangeLength:
            delta = sourceValue - startSource
            return startDest + delta
    return sourceValue


# Make initial seeds go through the crazy train (all maps in sequence)
currentElems = [initialSeeds]
for currentMap in maps.values():
    currentElems.append([getDestination(elem, currentMap) for elem in currentElems[-1]])

print("Part 1", min(currentElems[-1]))


# For Part 2, we will not consider individual seeds (too much seeds)
# So we will consider range of seeds instead
# range of seeds = tuple (initialSeed, rangeLength)

assert len(initialSeeds) % 2 == 0, len(initialSeeds)
initialSeedRanges = (
    (initialSeeds[2 * x], initialSeeds[2 * x + 1])
    for x in range(len(initialSeeds) // 2)
)


# Here I spent some time trying to check if I could simplify the ruleset by merging rules
# This was interesting but is ultimately useless :)
# So : snipping this code ✂️


def getDestinationRanges(oneSourceRange, mapping):
    # print("oneSourceRange", oneSourceRange)
    [sourceRangeStart, sourceRangeLength] = oneSourceRange
    sourceRangeEnd = sourceRangeStart + sourceRangeLength - 1

    # print("SOURCE\t", sourceRangeStart, sourceRangeEnd)

    assert sourceRangeLength >= 0, oneSourceRange
    if sourceRangeLength == 0:
        return []

    for mapRuleLine in mapping:
        [ruleStartDest, ruleStartSource, ruleRangeLength] = mapRuleLine
        ruleEndSource = ruleStartSource + ruleRangeLength - 1

        # sourceRange can overlap with the mapRuleLine rule in different ways

        # range fully contained in rule [ ( ) ]
        if (
            ruleStartSource <= sourceRangeStart <= ruleEndSource
            and sourceRangeEnd <= ruleEndSource
        ):
            # => return a single range
            deltaStart = sourceRangeStart - ruleStartSource
            return [(ruleStartDest + deltaStart, sourceRangeLength)]

        # Range going over the rule on the right [ ( ] )
        if (
            ruleStartSource < sourceRangeStart < ruleEndSource
            and sourceRangeEnd > ruleEndSource
        ):
            # => return the translated range on the left, and recursively handle the range on the right
            deltaStart = sourceRangeStart - ruleStartSource
            overLappingRangeLength = ruleEndSource - sourceRangeStart
            extraRange = (ruleEndSource + 1, sourceRangeLength - overLappingRangeLength)
            return [
                (ruleStartDest + deltaStart, overLappingRangeLength),
                *getDestinationRanges(extraRange, mapping),
            ]

        # Range going over the rule on the left ( [ ) ]
        if (
            sourceRangeStart < ruleStartSource
            and ruleStartSource < sourceRangeEnd < ruleEndSource
        ):
            # => return the translated range on the right, and recursively handle the range on the left
            deltaSource = ruleStartSource - sourceRangeStart
            overLappingRangeLength = sourceRangeLength - deltaSource
            extraRange = (sourceRangeStart, deltaSource)
            return [
                *getDestinationRanges(extraRange, mapping),
                (ruleStartDest, sourceRangeLength - deltaSource),
            ]

        # Range fully containing the rule ( [ ] )
        if sourceRangeStart <= ruleStartSource and sourceRangeEnd >= ruleEndSource:
            # => return the translated range in the middle, and recursively handle the range on both sides
            deltaLeft = ruleStartSource - sourceRangeStart
            deltaRight = sourceRangeEnd - ruleEndSource
            extraRangeLeft = (sourceRangeStart, deltaLeft)
            extraRangeRight = (sourceRangeEnd - deltaRight, deltaRight)

            return [
                *getDestinationRanges(extraRangeLeft, mapping),
                (ruleStartDest, ruleRangeLength),
                *getDestinationRanges(extraRangeRight, mapping),
            ]

        # Range outside of rule : () [] or [] ()
        # Check for other rules
        continue

    # No matching rule => dest = sourc
    return [oneSourceRange]


currentElemsRanges = [initialSeedRanges]
for currentMapName in maps.keys():
    print("=step", currentMapName)
    currentMap = maps[currentMapName]

    newCurrentElemsRanges = []
    for elemRange in currentElemsRanges[-1]:
        newRanges = getDestinationRanges(elemRange, currentMap)
        assert len(newRanges) >= 0
        newCurrentElemsRanges.extend(newRanges)

    print(sorted(newCurrentElemsRanges))
    currentElemsRanges.append(newCurrentElemsRanges)


minPositions = list(sorted(r[0] for r in currentElemsRanges[-1] if r[1] > 0))
print("Part 2", minPositions[0])
