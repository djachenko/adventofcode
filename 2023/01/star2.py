from pathlib import Path

REPLACEMENTS = [
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

REPLACEMENTS = {s: str(i + 1) for i, s in enumerate(REPLACEMENTS)}


def main():
    result = 0

    with Path("input.txt").open() as input_file:
        for line in input_file:
            line = line.strip()

            repl_finds = [(s, line.find(s)) for s in REPLACEMENTS]
            repl_finds = [(a, b) for a, b in repl_finds if b >= 0]
            repl_finds.sort(key=lambda x: x[1])

            if repl_finds:
                src, _ = repl_finds[0]
                line = line.replace(src, REPLACEMENTS[src], 1)

            repl_finds = [(s, line.rfind(s)) for s in REPLACEMENTS]
            repl_finds = [(a, b) for a, b in repl_finds if b >= 0]
            repl_finds.sort(key=lambda x: x[1], reverse=True)

            if repl_finds:
                src, _ = repl_finds[0]
                line = line.replace(src, REPLACEMENTS[src])

            digits = [c for c in line if c.isdigit()]

            calibration_value = int(digits[0] + digits[-1])

            result += calibration_value

    print(result)


if __name__ == '__main__':
    main()
