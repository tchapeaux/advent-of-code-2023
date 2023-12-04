import aoc

cards = aoc.getLinesForDay(4)
# cards = aoc.getLinesForDay(4, force_filepath="inputs/day04_example.txt")

pointsTotal = 0
pointsPerCard = []
nbOfCards = [1] * len(cards)

for idx, line in enumerate(cards):
    # Parse content
    line = line.split(": ")[1]  # Remove prefix
    [valids, haves] = line.split(" | ")
    valids = [int(x) for x in valids.split(" ") if len(x) > 0]
    haves = [int(x) for x in haves.split(" ") if len(x) > 0]

    # Find matches
    intersects = set(valids).intersection(set(haves))

    # Attribute points (Part 1)
    pointsPerCard.append(pow(2, len(intersects) - 1) if len(intersects) > 0 else 0)

    # Generate more cards (Part 2)
    for _i in range(len(intersects)):
        nextCardIdx = idx + _i + 1
        if (nextCardIdx) < len(cards):
            nbOfCards[nextCardIdx] += nbOfCards[idx]


print("Part 1", sum(pointsPerCard))

# x too low (forgot the 2^i formula)

print("Part 2", sum(nbOfCards))

# x too high (forgot a +1 when counting the next cards)
