import sys

LDI = 0b10000010
PRN = 0b01000111  # Print
HLT = 0b00000001  # Halt
MUL = 0b10100010  # Multiply
ADD = 0b10100000  # Addition
SUB = 0b10100001  # Subtraction
DIV = 0b10100011  # Division
PUSH = 0b01000101  # Stack Push
POP = 0b01000110  # Stack Pop
SP = 7  # Stack pointer
RET = 0b00010001
CALL = 0b01010000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.flags = 0

    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]
        address = 0

        try:
            with open(filename) as f:
                for line in f:
                    line = line.split("#")[0].strip()
                    if line != '':
                        # print(line)
                        self.ram[address] = int(line, 2)
                        address += 1
                    else:
                        continue
        except FileExistsError:
            print(f'Error: {filename} not found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == HLT:
            self.running = False
            self.pc += 1
        elif op == LDI:
            self.reg[reg_a] = reg_b
            self.pc += 3
        elif op == PRN:
            print(self.reg[reg_a])
            self.pc += 2
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == PUSH:
            self.reg[SP] -= 1
            stack_address = self.reg[SP]
            register_number = self.ram_read(self.pc + 1)
            register_number_value = self.reg[register_number]
            self.ram_write(stack_address, register_number_value)
            self.pc += 2
        elif op == POP:
            stack_value = self.ram_read(self.reg[SP])
            register_number = self.ram_read(self.pc + 1)
            self.reg[register_number] = stack_value
            self.reg[SP] += 1
            self.pc += 2
        elif op == CALL:
            self.reg[SP] -= 1
            stack_address = self.reg[SP]
            returned_address = self.pc + 2
            self.ram_write(stack_address, returned_address)
            register_number = self.ram_read(self.pc + 1)
            self.pc = self.reg[register_number]

        elif op == RET:
            self.pc = self.ram_read(self.reg[SP])
            self.reg[SP] += 1

        elif op == CMP:
            register_a = self.ram_read(self.pc + 1)
            register_b = self.ram_read(self.pc + 2)
            value_a = self.reg[register_a]
            value_b = self.reg[register_b]
            if value_a == value_b:
                self.flags = 0b1
            elif value_a > value_b:
                self.flags = 0b10
            elif value_b > value_a:
                self.flags = 0b100
            self.pc += 3

        elif op == JMP:
            register_a = self.ram_read(self.pc + 1)
            self.pc = self.reg[register_a]

        elif op == JEQ:
            if not self.flags & 0b1:
                self.pc += 2
            elif self.flags & 0B1:
                register_a = self.ram_read(self.pc + 1)
                self.pc = self.reg[register_a]

        elif op == JNE:
            if self.flags & 0b1:
                self.pc += 2
            elif not self.flags & 0b0:
                register_a = self.ram_read(self.pc + 1)
                self.pc = self.reg[register_a]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.load()
        while self.running:
            instruction_register = self.ram[self.pc]
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc + 2]

            # self.trace()
            self.alu(instruction_register, reg_a, reg_b)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):

        self.ram[address] = value


def driver():
    cpu = CPU()
    cpu.load()
    cpu.run()


if __name__ == "__main__":
    driver()
