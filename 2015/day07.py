from aoc_components.input_getter import get_my_input
import re
from dataclasses import dataclass, field
from typing import Dict

inp = get_my_input(__file__)

_nil = object()


@dataclass
class Gate:
    out: str
    lhs: str
    op: str
    rhs: str
    gates: Dict[str, 'Gate'] = field(repr=False)
    _evaluated = _nil

    def reset(self):
        self._evaluated = _nil

    def eval(self):
        if self._evaluated is _nil:
            self._evaluated = self._eval(self.get)
        return self._evaluated

    def _eval(self, getter):
        if (not self.op) and (not self.rhs):
            return getter(self.lhs)
        if self.op == "NOT":
            return (~getter(self.lhs)) & ((2**16)-1)
        if self.op == "AND":
            return getter(self.lhs) & getter(self.rhs)
        if self.op == "OR":
            return getter(self.lhs) | getter(self.rhs)
        if self.op == "RSHIFT":
            return getter(self.lhs) >> getter(self.rhs)
        if self.op == "LSHIFT":
            return (getter(self.lhs) << getter(self.rhs))
        raise ZeroDivisionError()

    def get(self, gate: str) -> int:
        if gate.isnumeric():
            return int(gate)
        return self.gates[gate].eval()


r = re.compile(r"^(?P<not>NOT)? ?(?P<lhs>[a-z0-9]+) ?((?P<op>[A-Z]+) (?P<rhs>[a-z0-9]+))? -> (?P<out>[a-z]+)$")


def fill(gates: dict):
    global inp
    for l in inp.splitlines():
        m = r.match(l)
        if not m:
            raise RuntimeError()
        g = Gate(
            m.group("out"),
            m.group("lhs"),
            m.group("not") or m.group("op"),
            m.group("rhs"),
            gates
        )
        gates[m.group("out")] = g


def test():
    assert Gate("", "52154", "AND", "54154", None).eval() == 50058
    assert Gate("", "52154", "OR", "54154", None).eval() == 56250

    assert Gate("", "52154", "LSHIFT", "1", None).eval() == 104308
    assert Gate("", "52154", "RSHIFT", "3", None).eval() == 6519

    assert Gate("", "52154", "NOT", None, None).eval() == 13_381


if __name__ == "__main__":
    test()
    gates: Dict[str, 'Gate'] = {}
    fill(gates)
    a = gates['a'].eval()
    print(f"part 1: {a}")
    for g in gates.values():
        g.reset()
    gates["b"].lhs = str(a)
    print(f"part 2: {gates['a'].eval()}")
