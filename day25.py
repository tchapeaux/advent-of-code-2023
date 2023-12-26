from typing import Deque
from collections import deque

import aoc

lines = aoc.getLinesForDay(25)
# lines = aoc.getLinesForDay(25, force_filepath="inputs/day25_example.txt")

Node = str
Edge = tuple[Node, Node]

edges: set[Edge] = set()
nodes: set[Node] = set()

for line in lines:
    source, rest = line.split(": ")
    nodes.add(source)
    dests = rest.split(" ")
    for d in dests:
        # Use alphabetical sort to have a canonical format
        canonical = tuple(sorted([source, d]))
        edges.add((canonical[0], canonical[1]))
        nodes.add(d)

print("Parsed", len(nodes), "nodes")
print("Parsed", len(edges), "edges")

# Iterate over all 3 edges
stepCnt = 0
totalStep = len(edges) * (len(edges) - 1) * (len(edges) - 2)
for e1 in edges:
    for e2 in edges:
        for e3 in edges:
            if e1 == e2 or e2 == e3 or e1 == e3:
                continue

            stepCnt += 1
            print(e1, e2, e3, stepCnt, totalStep)
            print(aoc.getTick())

            restEdges1: set[Edge] = set(e for e in edges if e not in (e1, e2, e3))

            buffer1: Deque[Edge] = deque()
            bucket1: set[Node] = set()
            buffer1.append(list(restEdges1)[0])

            while len(buffer1) > 0:
                currentEdge: Edge = buffer1.pop()
                n1, n2 = currentEdge[0], currentEdge[1]
                if n1 not in bucket1:
                    bucket1.add(n1)
                    for edgeFrom1 in (e for e in restEdges1 if n1 in e):
                        buffer1.append(edgeFrom1)

                if n2 not in bucket1:
                    bucket1.add(n2)
                    for edgeFrom2 in (e for e in restEdges1 if n2 in e):
                        buffer1.append(edgeFrom2)

            if len(bucket1) == len(nodes):
                continue  # did not disconnect graph

            restNodes2 = set(n for n in nodes if n not in bucket1)
            restEdges2 = set(
                e for e in restEdges1 if e[0] in restNodes2 and e[1] in restNodes2
            )

            buffer2: Deque[Edge] = deque()
            bucket2: set[Node] = set()
            buffer2.append(list(restEdges2)[0])

            while len(buffer2) > 0:
                currentEdge: Edge = buffer2.pop()
                n1, n2 = currentEdge[0], currentEdge[1]
                if n1 not in bucket2:
                    bucket2.add(n1)
                    for edgeFrom1 in (e for e in restEdges2 if n1 in e):
                        buffer2.append(edgeFrom1)

                if n2 not in bucket2:
                    bucket2.add(n2)
                    for edgeFrom2 in (e for e in restEdges2 if n2 in e):
                        buffer2.append(edgeFrom2)

            print("buckets", len(bucket1), len(bucket2), "for", len(nodes))

            if (
                len(bucket1) > 0
                and len(bucket2) > 0
                and len(bucket1) + len(bucket2) == len(nodes)
            ):
                print("FOUND", e1, e2, e3, len(bucket1) * len(bucket2))
                exit(0)
            else:
                print("found cut with more than one bucket", e1, e2, e3)
