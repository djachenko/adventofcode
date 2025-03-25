from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable, Tuple, Dict

from framework.aoc import *
from framework.aoc import INPUT


class Gate:
    pass


@dataclass
class ValueGate(Gate):
    value: int


@dataclass
class UnaryGate(Gate):
    value: str


class NotGate(UnaryGate):
    pass


class PassGate(UnaryGate):
    pass


@dataclass
class BinaryGate(Gate):
    left: str
    right: str


class AndGate(BinaryGate):
    pass


class OrGate(BinaryGate):
    pass


@dataclass
class ShiftGate(Gate):
    gate: str
    value: int


class RshiftGate(ShiftGate):
    pass


class LshiftGate(ShiftGate):
    pass


def parse_gate(gate: str) -> Gate:
    if gate.isdigit():
        value = int(gate)

        return ValueGate(value)
    elif "NOT" in gate:
        value = gate.split()[1]

        return NotGate(value)

    elif "AND" in gate:
        left, _, right = gate.split()

        return AndGate(left, right)
    elif "OR" in gate:
        left, _, right = gate.split()

        return OrGate(left, right)
    elif "RSHIFT" in gate:
        left, _, value = gate.split()
        value = int(value)

        return RshiftGate(left, value)
    elif "LSHIFT" in gate:
        left, _, value = gate.split()
        value = int(value)

        return LshiftGate(left, value)
    elif "  " not in gate:
        return PassGate(gate)
    else:
        assert False


@dataclass
class GateVisitor:
    mapping: Dict[str, Gate]

    @abstractmethod
    def visit(self, root: str):
        pass

    def __hash__(self):
        return hash(id(self))


class EvaluateVisitor(GateVisitor):
    @lru_cache(maxsize=None)
    def visit(self, root: str) -> int:
        if root not in self.mapping:
            return int(root)

        gate = self.mapping[root]

        if isinstance(gate, ValueGate):
            return gate.value
        elif isinstance(gate, NotGate):
            return ~ self.visit(gate.value)
        elif isinstance(gate, PassGate):
            return self.visit(gate.value)
        elif isinstance(gate, AndGate):
            return self.visit(gate.left) & self.visit(gate.right)
        elif isinstance(gate, OrGate):
            return self.visit(gate.left) | self.visit(gate.right)
        elif isinstance(gate, RshiftGate):
            return self.visit(gate.gate) >> gate.value
        elif isinstance(gate, LshiftGate):
            return self.visit(gate.gate) << gate.value
        else:
            assert False


def parse_gates() -> Iterable[Tuple[str, Gate]]:
    for line in INPUT.lines:
        gate, out = line.split(" -> ")

        yield out, parse_gate(gate)


gates = list(parse_gates())
ROUNDER = 2 ** 16 - 1


@lru_cache()
def star1() -> Output:
    mapping = dict(gates)
    visitor = EvaluateVisitor(mapping)

    return visitor.visit("a") & ROUNDER


def star2() -> Output:
    mapping = dict(gates)
    mapping["b"] = ValueGate(star1())

    visitor = EvaluateVisitor(mapping)

    return visitor.visit("a") & ROUNDER


if __name__ == '__main__':
    run(star1, star2)
