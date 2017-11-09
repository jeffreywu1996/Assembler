#!/usr/bin/python

# This program translates our assembly code into machine code.
# Lab 2 for CSE 141L


import argparse

# TODO: branches
# TODO: does not handle random text in machine code that is not comment


opcodes = {
        'MOV': '000', 'LD': '001', 'ST': '010',
        'ADD': '011', 'LSL': '100', 'LSR': '101',
        'MOVI': '110', 'SPI': '111',
        }

registers = {
        'R0': '000', 'R1': '001', 'R2': '010',
        'R3': '011', 'R4': '100', 'R5': '101',
        'R6': '110', 'R7': '111',
        }

binary = {
        '0': '000', '1': '001', '2': '010',
        '3': '011', '4': '100', '5': '101',
        '6': '110', '7': '111',
        }

def translate_params (param, debug_line=""):
    """Translate one parameter of our assembly code into machine code
    Args:
        param one of the parameter of the assembly code
        debug_line line of the assembly code for debug purposes

    Return:
        returns the machine code portion of this parameter
    """
    # Translate if params is a register
    if param in registers:
        return registers[param]
    # Translate if params is a constant
    elif param.isdigit():
        if int(param) >= 0 and int(param) < 8:  # Only 3 bits for constants
            return binary[param]
        else:
            raise Exception("Syntax error, constant: %d in '%s' is not supported" %(int(param), debug_line))
    else:
        raise Exception("Parse error, cannot parse %" %(debug_line))

def translate_assembly (line):
    """Translate a line of assembly code into machine code
    Args:
        line a line of assembly code

    Return:
        returns the machine code of that line of assembly code
    """
    debug_line = line
    # split each line by their parameters
    line = line.split(' ')
    # Make everything uppercase
    line = [param.upper() for param in line]
    # Strip comma in line
    line[1] = line[1].strip(',')

    machine_code = ""

    # Check if valid instruction set
    if line[0] not in opcodes:
        raise Exception("Syntax error, %s not a valid instruction" %(line[0]))
    # Translate instruction to opcode
    machine_code += opcodes[line[0]]

    # Special instructions
    if 'SPI' == line[0]:
        if len(line[1]) != 6:
            raise Exception("Syntax error, %s has wrong format" %(debug_line))
        return machine_code + line[1]

    # Translate 1st param
    machine_code += translate_params(line[1], debug_line=debug_line)

    # Translate 2nd param
    machine_code += translate_params(line[2], debug_line=debug_line)

    # print line
    # print machine_code
    return machine_code


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('assembly_file')
    parser.add_argument('output_file')
    args = parser.parse_args()

    F_IN = args.assembly_file
    F_OUT = args.assembly_file

    # read in the file
    assembly_file = open(F_IN, 'r')
    contents = assembly_file.read()

    # Data clean up
    contents = contents.splitlines() # split by line
    contents = filter(None, contents)  # remove empty lines
    # remove line comments
    contents = filter(lambda line: not line.startswith(';'), contents)
    # remove inline comments and trim whitespaces
    contents = [line.split(';')[0].strip() for line in contents]
    # remove lines with semicolons (branch labels)
    contents = filter(lambda line: ':' not in line, contents)

    print contents

    outfile = open(F_OUT, 'w')
    for line in contents:
        print translate_assembly(line)
        # outfile.write(translate(line))


if __name__ == '__main__':
    main()
