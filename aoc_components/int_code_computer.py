from collections import deque
from enum import Enum
from os.path import isfile
from typing import Any, Callable, NoReturn, Optional, Sequence, Union


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class CompoundOpCode:
    def __init__(self, value):
        value = str(value)
        value = ("0" * (5 - len(value))) + value
        self.value = value

    def __str__(self):
        return f'{self.__class__.__name__}("{self.value}")'

    __repr__ = __str__

    @property
    def oc(self):
        """real op code"""
        return int(self.value[3:])

    def mode(self, p: int):
        return Mode(int(self.value[3 - p]))

    @property
    def mode3(self):
        return self.mode(3)

    @property
    def mode2(self):
        return self.mode(2)

    @property
    def mode1(self):
        return self.mode(1)


class IntCodeComputer:
    """A 'Computer' to run the AoC 2019 IntCodes.
    It uses a dict, to allow simple arbitrary memory access without KeyErrors.

    Params:
        code: the IntCode in either:
            - Sequence[int]
            - str (filename or list of ints)
            - dict-memory-map (like from another computer)
        inputs: ints that should be first used, if the program asks for input
        async_inputs: instead of using the prompt, the .run() loop exists and waits for input via .input(int)
        write_cmd: if output should be printed to the commandline
        name: for debugging
        output_consumer: function that handles outputs (instead of default print)
    """
    def __init__(self, code: Union[Sequence[int], str, dict], inputs: Optional[Sequence[int]] = None,
                 async_inputs: bool = False, write_cmd: bool = True, name: Optional[Any] = None,
                 output_consumer: Optional[Callable[[int], NoReturn]] = None):
        self.code = self._parse_code(code)
        self.inputs = deque(inputs or [])
        self.output = deque()
        self.ip = 0
        self.async_inputs = async_inputs
        self.halt = False
        self.write_cmd = write_cmd
        self.waiting_for_input = False
        self.name = str(name)
        self.relative_base = 0
        self.print = output_consumer if output_consumer else self._print
        self._output_receiver = output_consumer

    def __str__(self):
        if self.name:
            return f"{self.__class__.__name__}<{self.name}>"
        return f"{self.__class__.__name__}(<code>, {self.inputs}, {self.async_inputs}, {self.write_cmd})"

    __repr__ = __str__

    def copy(self, new_name: Optional[Any] = None):
        """spawns a new independent instance with the exact memory copy"""
        name = new_name or (f"{self.name}-copy" if self.name else None)
        new = IntCodeComputer(self.code.copy(), self.inputs.copy(), self.async_inputs, self.write_cmd,
                              name, self._output_receiver)
        new.ip = self.ip
        new.relative_base = self.relative_base
        new.waiting_for_input = self.waiting_for_input
        new.halt = self.halt
        return new

    def _get_code(self, index, default=0):
        if index < 0:
            raise IndexError(f"Memory Index < 0!: {index}")
        return self.code.get(index, default)

    def _get_address_from_parameter(self, param: int):
        mode = self.current_op_code.mode(param)
        if mode == Mode.IMMEDIATE:
            return self.ip + param
        if mode == Mode.POSITION:
            return self._get_code(self.ip + param)
        if mode == Mode.RELATIVE:
            return self.relative_base + self._get_code(self.ip + param)

    def _set(self, param_num: int, value: int):
        rw_addr = self._get_address_from_parameter(param_num)
        if rw_addr < 0:
            raise IndexError(f"Memory rw_addr < 0!: {rw_addr}")
        self.code[rw_addr] = value

    def _get(self, param_num: int):
        r_addr = self._get_address_from_parameter(param_num)
        return self._get_code(r_addr)

    def input(self, value: int):
        """add a value to the queue"""
        self.inputs.append(value)
        self.waiting_for_input = False

    def _get_next_input(self, text) -> Optional[int]:
        if self.inputs:
            return self.inputs.popleft()
        if self.async_inputs:
            self.waiting_for_input = True
            return None
        return int(input(text))

    def _print(self, i: int):
        self.output.append(i)
        if self.write_cmd:
            print(i)

    def last_(self, n: int = 1):
        if not self.output:
            return None
        _v = [self.output.pop() for _ in range(n)]
        return _v[0] if n == 1 else _v

    def run(self, input_i: Optional[int] = None):
        """start/continue execution"""
        if input_i:
            self.input(input_i)
        while not (self.halt or self.waiting_for_input):
            op_code = self.current_op_code
            func = getattr(self, f"_op_{op_code.oc}", None)
            if not func:
                print(f"ERROR: OP Code '{op_code}'/'{op_code.oc}' at self.ip '{self.ip}' unknown", self.code)
                return
            func()
        return self.halt

    @property
    def current_op_code(self):
        return CompoundOpCode(self.code[self.ip])

    @staticmethod
    def _parse_code(code: Union[Sequence[int], str, dict]):
        if isinstance(code, dict):
            return code.copy()
        if isinstance(code, str):
            if isfile(code):
                with open(code, "r") as f:
                    code = f.read()
            if "," in code:
                code = [int(_) for _ in code.replace(" ", "").replace("\n", "")
                        .replace("\r", "").replace("[", "").replace("]", "").split(",")]
            else:
                raise ValueError(f"cannot interpret code-string")
        return {k: v for k, v in enumerate(code)}

    def _op_99(self):
        self.halt = True
        self.waiting_for_input = False

    def _op_1(self):
        self._set(3, self._get(1) + self._get(2))
        self.ip += 4

    def _op_2(self):
        self._set(3, self._get(1) * self._get(2))
        self.ip += 4

    def _op_3(self):
        i = self._get_next_input("input new number>")
        if not self.waiting_for_input:
            self._set(1, i)
            self.ip += 2

    def _op_4(self):
        val = self._get(1)
        self.print(val)
        self.ip += 2

    def _op_5(self):
        val = self._get(1)
        if val != 0:
            self.ip = self._get(2)
        else:
            self.ip += 3

    def _op_6(self):
        val = self._get(1)
        if val == 0:
            self.ip = self._get(2)
        else:
            self.ip += 3

    def _op_7(self):
        new = int(self._get(1) < self._get(2))
        self._set(3, new)
        self.ip += 4

    def _op_8(self):
        new = int(self._get(1) == self._get(2))
        self._set(3, new)
        self.ip += 4

    def _op_9(self):
        self.relative_base += self._get(1)
        self.ip += 2
