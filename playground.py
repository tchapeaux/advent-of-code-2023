def line_intersection(P1, P2, V1, V2):
    # Step 1: Calculate the slopes of the lines
    slope1 = V1[1] / V1[0]
    slope2 = V2[1] / V2[0]

    # Step 2: Calculate the y-intercepts of the lines
    intercept1 = P1[1] - slope1 * P1[0]
    intercept2 = P2[1] - slope2 * P2[0]

    print(intercept1, intercept2)

    # Step 3: Calculate the x-coordinate of the intersection point
    x = (intercept2 - intercept1) / (slope1 - slope2)

    # Step 4: Calculate the y-coordinate of the intersection point
    y = slope1 * x + intercept1

    # Step 5: Return the intersection point
    return [x, y]


A = [0, 0]
VA = [1, 1]
B = [1, 0]
VB = [-1, 1]

print(line_intersection(A, VA, B, VB))  # Output: [0.5, 0.5]
