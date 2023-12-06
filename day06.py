import re

import aoc

data = aoc.getLinesForDay(6)


times = [int(x) for x in re.findall(r"(\d+)", data[0])]
distances = [int(x) for x in re.findall(r"(\d+)", data[1])]

print(times, distances)

assert len(times) == len(distances)

part1Acc = 1


def numberOfWays(raceTime, bestDistance):
    validWays = []
    for tPress in range(raceTime):
        myDistance = tPress * (raceTime - tPress)
        if myDistance > bestDistance:
            validWays.append(tPress)
    return len(validWays)


for raceTime, bestDistance in zip(times, distances):
    validWays = numberOfWays(raceTime, bestDistance)
    part1Acc *= validWays

print("Part 1", part1Acc)
print(aoc.getTick())


part2Time = int("".join([str(num) for num in times]))
part2Distance = int("".join([str(num) for num in distances]))

print("Part 2", numberOfWays(part2Time, part2Distance))
print(aoc.getTick())
