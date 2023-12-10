import aoc

data = aoc.getLinesForDay(9)

histories = []
for line in data:
    histories.append([int(val) for val in line.split(" ")])


def getNextValue(history):
    sequences = [[*history]]
    while not all([x == 0 for x in sequences[-1]]):
        newSeq = []
        for idx in range(len(sequences[-1]) - 1):
            newSeq.append(sequences[-1][idx + 1] - sequences[-1][idx])
        sequences.append(newSeq)

    sequences[-1].append(0)

    for seqIdx in range(len(sequences) - 2, -1, -1):
        sequences[seqIdx].append(sequences[seqIdx][-1] + sequences[seqIdx + 1][-1])

    return sequences[0][-1]


assert getNextValue([0, 3, 6, 9, 12, 15]) == 18
assert getNextValue([1, 3, 6, 10, 15, 21]) == 28
assert getNextValue([10, 13, 16, 21, 30, 45]) == 68

print("Part 1", sum([getNextValue(h) for h in histories]))


def getPrevValue(history):
    sequences = [[*history]]
    while not all([x == 0 for x in sequences[-1]]):
        newSeq = []
        for idx in range(len(sequences[-1]) - 1):
            newSeq.append(sequences[-1][idx + 1] - sequences[-1][idx])
        sequences.append(newSeq)

    sequences[-1].insert(0, 0)

    for seqIdx in range(len(sequences) - 2, -1, -1):
        sequences[seqIdx].insert(0, sequences[seqIdx][0] - sequences[seqIdx + 1][0])

    return sequences[0][0]


assert getPrevValue([10, 13, 16, 21, 30, 45]) == 5

print("Part 2", sum([getPrevValue(h) for h in histories]))
