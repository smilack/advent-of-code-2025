import parser12


def area(present):
    return sum([sum(row) for row in present])


if __name__ == "__main__":
    tree = parser12.get_input()
    parser12.print_presents(tree["presents"])
    parser12.print_regions(tree["regions"])

    present_areas = [area(p) for _, p in sorted(tree["presents"].items())]

    ub = 0
    for i, ((w, h), req) in enumerate(tree["regions"]):
        ar = w * h
        total_area = sum([req[i] * present_areas[i] for i in range(len(req))])
        if total_area < ar:
            ub += 1
            possible = "✅"
        else:
            possible = "✗"
        print(
            f"Region {i} area: {ar}. Total present area: {total_area}. Solution possible? {possible}"
        )

    print("Upper bound:", ub)

    print("Part 1:")

    print("Part 2:")
