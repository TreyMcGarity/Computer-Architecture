"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = len(self.ram) - 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    # stack functions
    def push(self, value):
        print("pushed:", value)
        self.sp -= 1
        self.ram[self.sp] = value

    def pop(self):
        if self.sp < len(self.ram) - 1:
            value = self.ram[self.sp]
            self.sp += 1
            return value

    def load(self):
        """Load a program into memory."""

        address = 0
        program = []

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    if line == '' or line[0] =='#':
                        continue
                    
                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, base = 2)
                        program.append(value)

                    except ValueError:
                        print(f"Unknown number {str_value} on line: 45")

        except FileNotFoundError:
            print(f"File not found {sys.argv[1]}")

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD": # example..
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # DAY 1:
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        # Day 2:
        MUL = 0b10100010
        # Day 3:
        PUSH = 0b01000101
        POP = 0b01000110
        # Day 4:
        CALL = 0b01010000
        RET = 0b00010001

        halted = False

        while not halted:
            instruction = self.ram_read(self.pc)

            if instruction == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_num] = value
                self.pc += 3
            
            elif instruction == PRN:
                reg_num = self.ram[self.pc + 1]
                print(self.reg[reg_num])
                self.pc += 2

            elif instruction == MUL:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3 

            elif instruction == PUSH:
                reg_num = self.ram[self.pc + 1]
                self.push(self.reg[reg_num])
                self.pc += 2

            elif instruction == POP:
                reg_num = self.ram[self.pc + 1]
                self.pop()
                self.pc += 2

            elif instruction == CALL:
                reg_num = self.ram[self.pc + 1]
                self.push(self.reg[reg_num])
                self.pc = self.reg[reg_num]

            elif instruction == RET:
                self.pc = self.pop()

            elif instruction == HLT:
                halted = True