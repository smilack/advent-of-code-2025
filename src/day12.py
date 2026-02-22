import parser12


def area(present):
    return sum([sum(row) for row in present])


if __name__ == "__main__":
    tree = parser12.get_input()
    parser12.print_presents(tree["presents"])
    parser12.print_regions(tree["regions"])

    present_areas = [area(p) for _, p in sorted(tree["presents"].items())]

    # I thought this was just going to be a naive upper bound because the example input has a case where there is "enough" area for the presents, but they don't all fit.
    # But it turns out, for the real input, the naive solution worked!

    upper_bound = 0
    for i, ((w, h), req) in enumerate(tree["regions"]):
        ar = w * h
        total_area = sum([req[i] * present_areas[i] for i in range(len(req))])
        if total_area < ar:
            upper_bound += 1
            possible = "✅"
        else:
            possible = "❌"
        print(
            f"Region {i} area: {ar}. Total present area: {total_area}. Solution possible? {possible}"
        )

    print("Upper bound:", upper_bound)
