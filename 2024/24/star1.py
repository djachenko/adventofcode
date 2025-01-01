from abc import abstractmethod
from typing import Dict

from utils import read_by_line


class Gate:
    @abstractmethod
    def evaluate(self, mapping: Dict[str, 'Gate']) -> bool:
        return False


class UnaryGate(Gate):
    def __init__(self, value: bool):
        self.__value = value

    def evaluate(self, mapping: Dict[str, 'Gate']) -> bool:
        return self.__value


class AndGate(Gate):
    def __init__(self, left: str, right: str):
        self.__left = left
        self.__right = right

    def evaluate(self, mapping: Dict[str, 'Gate']) -> bool:
        return mapping[self.__left].evaluate(mapping) and mapping[self.__right].evaluate(mapping)


class OrGate(Gate):
    def __init__(self, left: str, right: str):
        self.__left = left
        self.__right = right

    def evaluate(self, mapping: Dict[str, 'Gate']) -> bool:
        return mapping[self.__left].evaluate(mapping) or mapping[self.__right].evaluate(mapping)


class XorGate(Gate):
    def __init__(self, left: str, right: str):
        self.__left = left
        self.__right = right

    def evaluate(self, mapping: Dict[str, 'Gate']) -> bool:
        return mapping[self.__left].evaluate(mapping) != mapping[self.__right].evaluate(mapping)


def main():
    mapping = {}

    stream = read_by_line()

    for line in stream:
        if not line:
            break

        name, value = line.split(": ")
        value = value == "1"

        mapping[name] = UnaryGate(value)

    for line in stream:
        left, type_, right, _, name = line.split()

        match type_:
            case "AND":
                gate = AndGate(left, right)
            case "OR":
                gate = OrGate(left, right)
            case "XOR":
                gate = XorGate(left, right)
            case _:
                assert False

        mapping[name] = gate

    z_names = [name for name in mapping if name.startswith("z")]
    z_names.sort(reverse=True)

    result = 0

    for name in z_names:
        gate = mapping[name]

        value = gate.evaluate(mapping)

        result <<= 1

        if value:
            result += 1

    print(result)


if __name__ == '__main__':
    main()
