import aoc

data: list[str] = aoc.getLinesForDay(7)
# data: list[str] = aoc.getLinesForDay(7, force_filepath="inputs/day07_example_2.txt")

Card = str
Hand = tuple[Card, Card, Card, Card, Card]

hands: list[Hand] = []
bids: list[int] = []

for line in data:
    h, b = line.split()
    hands.append((h[0], h[1], h[2], h[3], h[4]))
    bids.append(int(b))

TYPE_ORDER = [
    "HIGH_CARD",
    "ONE_PAIR",
    "TWO_PAIR",
    "THREE_OF_A_KIND",
    "FULL_HOUSE",
    "FOUR_OF_A_KIND",
    "FIVE_OF_A_KIND",
]


def getHandType(hand: Hand):
    for card in hand:
        if hand.count(card) == 5:
            return "FIVE_OF_A_KIND"
        if hand.count(card) == 4:
            return "FOUR_OF_A_KIND"
        if hand.count(card) == 3:
            rest = [otherCard for otherCard in hand if otherCard != card]
            assert len(rest) == 2
            if rest[0] == rest[1]:
                return "FULL_HOUSE"
            return "THREE_OF_A_KIND"
        if hand.count(card) == 2:
            rest = [otherCard for otherCard in hand if otherCard != card]
            assert len(rest) == 3
            [restA, restB, restC] = rest
            if restA == restB == restC:
                return "FULL_HOUSE"
            if restA != restB and restB != restC and restA != restC:
                return "ONE_PAIR"
            if restA == restB and restA != restC:
                return "TWO_PAIR"
            if restA == restC and restA != restB:
                return "TWO_PAIR"
            if restB == restC and restB != restA:
                return "TWO_PAIR"
            raise Exception(f"What is this {hand} {restA} {restB} {restC}")

    assert len(set(hand)) == len(hand)
    return "HIGH_CARD"


def getCardScore(card):
    return list(
        reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"])
    ).index(card)


rankedHands = sorted(
    hands,
    key=lambda h: (TYPE_ORDER.index(getHandType(h)), *map(getCardScore, h)),
)


part1Sum = 0

for rank, hand in enumerate(rankedHands):
    initialIdx = hands.index(hand)
    bid = bids[initialIdx]
    part1Sum += (rank + 1) * bid
    # print(rank + 1, "".join(hand), str(bid).zfill(3), getHandType(hand))

print("Part 1", part1Sum)

# Too low (only looked at the first card to solve ties)
# Too high (sorting function was buggy)
# Too low (rank starts at 1)
# Not the right answer (sorting function was still buggy)
# Not the right answer (edge cases between two pairs and full house)
# Not the right answer (other edge case between two pairs and full house)


def getCardScorePart2(card: Card):
    return list(
        reversed(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"])
    ).index(card)


def getJokerizedHand(hand: Hand):
    # Assumption: for ranking, jokers can always be replaced by the biggest pair
    jokersCount = hand.count("J")
    if jokersCount == 0:
        return [*hand]

    if jokersCount == 5:
        return ["A", "A", "A", "A", "A"]

    rest = [c for c in hand if c != "J"]
    uniqCards = set(rest)

    uniqCardsCount = {c: hand.count(c) for c in uniqCards}
    biggestPairCard = max((count, card) for (card, count) in uniqCardsCount.items())[1]
    jokerizedHand = [c if c != "J" else biggestPairCard for c in hand]
    return jokerizedHand


rankedHandsPart2 = sorted(
    hands,
    key=lambda h: (
        TYPE_ORDER.index(getHandType(getJokerizedHand(h))),
        *map(getCardScorePart2, h),
    ),
)

part2Sum = 0
for rank, hand in enumerate(rankedHandsPart2):
    initialIdx = hands.index(hand)
    bid = bids[initialIdx]
    part2Sum += (rank + 1) * bid
    # print(
    #     rank + 1, "".join(hand), str(bid).zfill(3), getHandType(getJokerizedHand(hand))
    # )

print("Part 2", part2Sum)
