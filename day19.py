from typing import NamedTuple
import re

import aoc

data = aoc.getInputForDay(19)
# data = aoc.getInputForDay(19, force_filepath="inputs/day19_example.txt")
# data = aoc.getInputForDay(19, force_filepath="inputs/day19_simple.txt")

Rule = str
Result = str  # A or R


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


[workflowsRaw, partsRaw] = data.split("\n\n")


workflows: dict[str, tuple[Rule, ...]] = {}
for line in workflowsRaw.strip().split("\n"):
    [name, rest] = line.split("{")
    rest = rest[:-1]
    rules = rest.split(",")
    workflows[name] = tuple(Rule(r) for r in rules)

print("Parsed", len(workflows), "workflows")

parts: list[Part] = []
for line in partsRaw.strip().split("\n"):
    values = line[1:-1].split(",")
    partDict = {}
    for val in values:
        prop, propVal = val.split("=")
        partDict[prop] = int(propVal)
    parts.append(Part(partDict["x"], partDict["m"], partDict["a"], partDict["s"]))

print("Parsed", len(parts), "parts")


def exploreWorkflows(part: Part, wfName: str = "in") -> Result:
    if wfName in "AR":
        return wfName

    rules = workflows[wfName]

    for rule in rules:
        if rule in "AR":
            return rule

        if ":" in rule:
            condition, targetName = rule.split(":")

            if "<" in condition:
                prop, val = condition.split("<")
                if getattr(part, prop) < int(val):
                    return exploreWorkflows(part, wfName=targetName)
            elif ">" in condition:
                prop, val = condition.split(">")
                if getattr(part, prop) > int(val):
                    return exploreWorkflows(part, wfName=targetName)
            else:
                raise RuntimeError(f"Unexpected condition {condition}")
        else:
            if re.match(r"\w+", rule):
                return exploreWorkflows(part, wfName=rule)
    else:
        raise RuntimeError(f"Could not resolve rule {rules}")


accepted: set[Part] = set()
rejected: set[Part] = set()

for part in parts:
    result: Result = exploreWorkflows(part)
    assert result in "AR"
    if result == "A":
        accepted.add(part)
    else:
        rejected.add(part)


def getPartScore(part: Part) -> int:
    return part.x + part.m + part.a + part.s


print("Part 1", sum([getPartScore(p) for p in accepted]))

# for Part 2, we work with ranges of parts


class PartRange(NamedTuple):
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]


def sizeOfRange(pRange: PartRange) -> int:
    return (
        (pRange.x[1] - (pRange.x[0] - 1))
        * (pRange.m[1] - (pRange.m[0] - 1))
        * (pRange.a[1] - (pRange.a[0] - 1))
        * (pRange.s[1] - (pRange.s[0] - 1))
    )


fullRange = PartRange((1, 4000), (1, 4000), (1, 4000), (1, 4000))


def exploreWorkflowsRanges(
    partRange: PartRange, wfName: str = "in"
) -> list[tuple[PartRange, Result]]:
    if wfName in "AR":
        return [(partRange, wfName)]

    rules = workflows[wfName]

    rangesQueue: list[tuple[PartRange, int]] = [
        (partRange, 0)
    ]  # queue of mapping from partial ranges to rule idx
    rangesResults: list[tuple[PartRange, Result]] = []

    while len(rangesQueue) > 0:
        currentItem = rangesQueue.pop(0)
        currentPartRange, currentRuleIdx = currentItem
        rule = rules[currentRuleIdx]

        if rule in "AR":
            rangesResults.append((currentPartRange, rule))

        elif ":" in rule:
            condition, targetName = rule.split(":")

            if "<" in condition:
                prop, val = condition.split("<")
                val = int(val)
                minProp = getattr(currentPartRange, prop)[0]
                maxProp = getattr(currentPartRange, prop)[1]
                if minProp < val:
                    newRange = (minProp, min(maxProp, val - 1))
                    smallerRange = PartRange(
                        currentPartRange.x if prop != "x" else newRange,
                        currentPartRange.m if prop != "m" else newRange,
                        currentPartRange.a if prop != "a" else newRange,
                        currentPartRange.s if prop != "s" else newRange,
                    )

                    rangesResults.extend(
                        exploreWorkflowsRanges(smallerRange, wfName=targetName)
                    )
                if maxProp >= val:
                    newRange = (max(val, minProp), maxProp)
                    restRange = PartRange(
                        currentPartRange.x if prop != "x" else newRange,
                        currentPartRange.m if prop != "m" else newRange,
                        currentPartRange.a if prop != "a" else newRange,
                        currentPartRange.s if prop != "s" else newRange,
                    )

                    rangesQueue.append((restRange, currentRuleIdx + 1))
            elif ">" in condition:
                prop, val = condition.split(">")
                val = int(val)
                minProp = getattr(currentPartRange, prop)[0]
                maxProp = getattr(currentPartRange, prop)[1]
                if maxProp > val:
                    newRange = (max(minProp, val + 1), maxProp)
                    biggerRange = PartRange(
                        currentPartRange.x if prop != "x" else newRange,
                        currentPartRange.m if prop != "m" else newRange,
                        currentPartRange.a if prop != "a" else newRange,
                        currentPartRange.s if prop != "s" else newRange,
                    )

                    rangesResults.extend(
                        exploreWorkflowsRanges(biggerRange, wfName=targetName)
                    )
                if minProp <= val:
                    newRange = (minProp, min(maxProp, val))
                    restRange = PartRange(
                        currentPartRange.x if prop != "x" else newRange,
                        currentPartRange.m if prop != "m" else newRange,
                        currentPartRange.a if prop != "a" else newRange,
                        currentPartRange.s if prop != "s" else newRange,
                    )
                    rangesQueue.append((restRange, currentRuleIdx + 1))

            else:
                raise RuntimeError(f"Unexpected condition {condition}")
        elif rule in workflows:
            rangesResults.extend(exploreWorkflowsRanges(currentPartRange, wfName=rule))
        else:
            raise RuntimeError(f"Unrecognized rule {rule}")

    return rangesResults


results = exploreWorkflowsRanges(fullRange)

for r in results:
    print(r[1], r[0])

acceptedCount = 0
rejectedCount = 0
for range, result in results:
    if result == "A":
        acceptedCount += sizeOfRange(range)
    else:
        assert result == "R"
        rejectedCount += sizeOfRange(range)

print(
    "Accepted",
    acceptedCount,
    "rejected",
    rejectedCount,
    "sum",
    acceptedCount + rejectedCount,
    "vs",
    sizeOfRange(fullRange),
)

print("Part 2", acceptedCount)
