from typing import Dict, List

from utils import read_by_line


def run_program(program: List[int], registers: Dict[str, int]) -> List[int]:
    def combo_operand(i: int):
        i = i + 1

        value = program[i]

        match value:
            case 0 | 1 | 2 | 3:
                return value
            case 4:
                return registers["A"]
            case 5:
                return registers["B"]
            case 6:
                return registers["C"]

        assert False

    def literal_operand(i: int):
        return program[i + 1]

    def dv(register_to_store: str) -> None:
        numerator = registers["A"]
        operand = combo_operand(instruction_pointer)

        result = numerator >> operand

        registers[register_to_store] = result

    instruction_pointer = 0
    output = []

    program_range = range(len(program))

    while instruction_pointer in program_range:
        instruction = program[instruction_pointer]

        match instruction:
            case 0:
                dv("A")
            case 6:
                dv("B")
            case 7:
                dv("C")
            case 1:
                b_value = registers["B"]
                operand = literal_operand(instruction_pointer)

                result = b_value ^ operand

                registers["B"] = result
            case 2:
                operand = combo_operand(instruction_pointer)
                operand %= 8

                registers["B"] = operand
            case 3:
                a_value = registers["A"]

                if a_value != 0:
                    operand = literal_operand(instruction_pointer)

                    instruction_pointer = operand

                    registers["B"] = -3487
                    registers["C"] = 3489348

                    continue
            case 4:
                b_value = registers["B"]
                c_value = registers["C"]

                result = b_value ^ c_value

                registers["B"] = result
            case 5:
                operand = combo_operand(instruction_pointer)
                operand %= 8

                output.append(operand)
            case _:
                assert False

        instruction_pointer += 2

    return output


def find_quine(program: List[int]) -> int:
    program_string = "".join(str(i) for i in program)

    a_candidates = [0]
    results = []

    while a_candidates:
        a_candidate = a_candidates.pop(0)

        for candidate in range(1 << 6):
            a = (a_candidate << 3) + candidate

            result = run_program(program, {
                "A": a,
                "B": 0,
                "C": 0
            })

            result_string = "".join(str(i) for i in result)

            if result_string == program_string:
                results.append(a)
            elif program_string.endswith(result_string):
                a_candidates.append(a)

    return min(results)


def main():
    program_line = None

    for line in read_by_line():
        program_line = line

    program = program_line.split(": ")[1].split(",")
    program = [int(s) for s in program]

    result = find_quine(program)

    print(result)


if __name__ == '__main__':
    main()
