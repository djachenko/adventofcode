from utils import read_by_line

ADV = 0
BXL = 1
BST = 2
JNZ = 3
BXC = 4
OUT = 5
BDV = 6
CDV = 7


def main():
    stream = read_by_line()

    registers = {}

    for line in stream:
        if not line:
            break

        name, value = line.split(": ")

        name = name.split(" ")[1]
        value = int(value)

        registers[name] = value

    program_line = next(stream)
    program = program_line.split(": ")[1].split(",")
    program = [int(s) for s in program]

    instruction_pointer = 0
    out_values = []

    def combo_operand(i: int):
        i = i + 1

        value = program[i]

        if value in range(4):
            return value

        if value == 4:
            return registers["A"]

        if value == 5:
            return registers["B"]

        if value == 6:
            return registers["C"]

        assert False

    def literal_operand(i: int):
        return program[i + 1]

    def dv(register_to_store: str) -> None:
        numerator = registers["A"]
        operand = combo_operand(instruction_pointer)

        result = numerator >> operand

        registers[register_to_store] = result

    while True:
        if instruction_pointer not in range(len(program)):
            break

        instruction = program[instruction_pointer]

        if instruction == ADV:
            dv("A")
        elif instruction == BDV:
            dv("B")
        elif instruction == CDV:
            dv("C")
        elif instruction == BXL:
            b_value = registers["B"]
            operand = literal_operand(instruction_pointer)

            result = b_value ^ operand

            registers["B"] = result
        elif instruction == BST:
            operand = combo_operand(instruction_pointer)

            operand %= 8

            registers["B"] = operand
        elif instruction == JNZ:
            a_value = registers["A"]

            if a_value != 0:
                operand = literal_operand(instruction_pointer)

                instruction_pointer = operand

                registers["B"] = -3487
                registers["C"] = 3489348

                continue
        elif instruction == BXC:
            b_value = registers["B"]
            c_value = registers["C"]

            result = b_value ^ c_value

            registers["B"] = result
        elif instruction == OUT:
            operand = combo_operand(instruction_pointer)

            operand %= 8

            out_values.append(operand)

        instruction_pointer += 2

    print(",".join(str(value) for value in out_values))


if __name__ == '__main__':
    main()
