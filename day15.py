import aoc

data: str = aoc.getInputForDay(15)
# data: str = aoc.getInputForDay(15, force_filepath="inputs/day15_example.txt")

steps: list[str] = data.strip().split(",")


def hashString(theString: str) -> int:
    current = 0
    for c in theString:
        current += ord(c)
        current *= 17
        current %= 256
    return current


assert hashString("HASH") == 52

hashes: list[int] = []
for step in steps:
    hashes.append(hashString(step))

print("Part 1", sum(hashes))

# x too low (forgot to remove \n from input)

NB_BOXES = 256

Lens = tuple[str, int]
Box = list[Lens]

boxes: list[Box] = []
for _ in range(NB_BOXES):
    boxes.append([])


def applyStep(step: str, boxes: list[Box]):
    if "=" in step:
        name, focalLength = step.split("=")
        focalLength = int(focalLength)

        boxIdx = hashString(name)
        box = boxes[boxIdx]

        if name in [l[0] for l in box]:
            boxes[boxIdx] = [((name, focalLength) if l[0] == name else l) for l in box]
        else:
            box.append((name, focalLength))

    if "-" in step:
        name = step.split("-")[0]
        boxIdx = hashString(name)
        box = boxes[boxIdx]

        boxes[boxIdx] = [l for l in box if l[0] != name]


for stepIdx, step in enumerate(steps):
    applyStep(step, boxes)

for boxIdx, box in enumerate(boxes):
    if len(box) > 0:
        print(boxIdx, box)

part2Sum = 0
for boxIdx in range(len(boxes)):
    box: Box = boxes[boxIdx]
    for lensIdx in range(len(box)):
        lens: Lens = box[lensIdx]
        power = (boxIdx + 1) * (lensIdx + 1) * lens[1]
        part2Sum += power

print("Part 2", part2Sum)
