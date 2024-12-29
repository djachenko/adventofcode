from dataclasses import dataclass

from utils import read_by_line, find


@dataclass
class Gate:
    left: str
    type_: str
    right: str
    out: str

    @staticmethod
    def from_string(string: str) -> 'Gate':
        left, type_, right, _, out = string.split()

        if left.startswith("y"):
            left, right = right, left

        return Gate(left=left, right=right, type_=type_, out=out)

    def __repr__(self) -> str:
        return f"\"{self.out}: {self.left} {self.type_} {self.right}\""


@dataclass
class Register:
    x_xor_y: Gate = None
    x_and_y: Gate = None
    shift_bit_or: Gate = None
    shift_bit_and: Gate = None
    z: Gate = None


def main():
    stream = read_by_line()

    for line in stream:
        if not line:
            break

    gate_list = [Gate.from_string(g) for g in stream]

    registers = []

    for i in range(46):
        def find_z(gate: Gate) -> bool:
            out = gate.out

            return out.startswith("z") and int(out[1:]) == i

        def find_a(gate: Gate) -> bool:
            left = gate.left

            return gate.type_ == "XOR" and left.startswith("x") and int(left[1:]) == i

        def find_b(gate: Gate) -> bool:
            left = gate.left

            return gate.type_ == "AND" and left.startswith("x") and int(left[1:]) == i

        x_xor_y = find(gate_list, find_a)
        x_and_y = find(gate_list, find_b)
        z = find(gate_list, find_z)

        def find_sb_or(gate: Gate) -> bool:
            return gate.type_ == "OR" and (gate.left == x_and_y.out or gate.right == x_and_y.out)

        def find_sb_and(gate: Gate) -> bool:
            return gate.type_ == "AND" and (gate.left == x_xor_y.out or gate.right == x_xor_y.out)

        if x_and_y is not None:
            shift_bit_or = find(gate_list, find_sb_or)
        else:
            shift_bit_or = None

        if x_xor_y is not None:
            shift_bit_and = find(gate_list, find_sb_and)
        else:
            shift_bit_and = None

        reg = Register(
            x_xor_y=x_xor_y,
            x_and_y=x_and_y,
            z=z,
            shift_bit_or=shift_bit_or,
            shift_bit_and=shift_bit_and
        )

        registers.append(reg)

    registers[0].shift_bit_or = registers[0].x_and_y

    for i in range(1, len(registers)):
        reg = registers[i]
        prev_reg = registers[i - 1]

        assert reg.z.type_ == "XOR"
        assert (reg.z.left == reg.x_xor_y.out) != (reg.z.right == reg.x_xor_y.out)
        assert (reg.z.left == prev_reg.shift_bit_or.out) != (reg.z.right == prev_reg.shift_bit_or.out)

        assert (reg.shift_bit_or.left == reg.x_and_y.out) != (reg.shift_bit_or.right == reg.x_and_y.out)
        assert (reg.shift_bit_or.left == reg.shift_bit_and.out) != (reg.shift_bit_or.right == reg.shift_bit_and.out)

        assert (reg.shift_bit_and.left == reg.x_xor_y.out) != (reg.shift_bit_and.right == reg.x_xor_y.out)

        assert (reg.shift_bit_and.left == prev_reg.shift_bit_or.out) != (reg.shift_bit_and.right == prev_reg.shift_bit_or.out)


if __name__ == '__main__':
    main()
