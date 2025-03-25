from framework.aoc import *


def star1() -> Output:
    result = 0

    for line in INPUT.lines:
        line = line.strip()

        digits = [c for c in line if c.isdigit()]

        calibration_value = int(digits[0] + digits[-1])

        result += calibration_value

    return result


def star2() -> Output:
    replacements = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]

    replacements = {s: str(i + 1) for i, s in enumerate(replacements)}
    result = 0

    for line in INPUT.lines:
        line = line.strip()

        repl_finds = [(s, line.find(s)) for s in replacements]
        repl_finds = [(a, b) for a, b in repl_finds if b >= 0]
        repl_finds.sort(key=lambda x: x[1])

        if repl_finds:
            src, _ = repl_finds[0]
            line = line.replace(src, replacements[src], 1)

        repl_finds = [(s, line.rfind(s)) for s in replacements]
        repl_finds = [(a, b) for a, b in repl_finds if b >= 0]
        repl_finds.sort(key=lambda x: x[1], reverse=True)

        if repl_finds:
            src, _ = repl_finds[0]
            line = line.replace(src, replacements[src])

        digits = [c for c in line if c.isdigit()]

        calibration_value = int(digits[0] + digits[-1])

        result += calibration_value

    return result


if __name__ == '__main__':
    run(star1, star2)
