from collections import deque
import pathlib
import sys


def parse_stacks(lines: list[str]) -> list[deque[str]]:
    deques: list[deque[str]] = []
    
    for col, char in enumerate(lines[-1]):
        if char not in ' []':
            deques.append(deque([
                line[col] for line in lines[:-1:]
                if col < len(line) and line[col] != ' ']))
    
    return deques

def parse_command(command: str) -> tuple[int, int, int]:
    split_command: list[str] = command.split()
    quantity: int = int(split_command[1])
    src_stack: int = int(split_command[3]) - 1
    dest_stack: int = int(split_command[5]) - 1
    
    return quantity, src_stack, dest_stack

def perform_move(quantity: int, src_stack: deque[str], dest_stack: deque[str]):
    crates: deque[str] = deque()
    for _ in range(quantity):
        crates.appendleft(src_stack.popleft())
    for _ in range(quantity):
        dest_stack.appendleft(crates.popleft())

def main():
    input_path: pathlib.Path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    
    with input_path.open('r') as input_file:
        stacks_lines: list[str] = []
        stacks: list[deque[str]] = []
        
        for line in input_file:
            line = line.strip('\n')
            
            if line and not stacks:
                stacks_lines.append(line)
                continue
            
            if line and stacks:
                quantity, src_stack_index, dest_stack_index = \
                    parse_command(line)
                perform_move(quantity, stacks[src_stack_index], 
                             stacks[dest_stack_index])
                continue
            
            if not line:
                stacks = parse_stacks(stacks_lines)
    
    stack_top_string: str = ''.join(
        [stack[0] if stack else ' ' for stack in stacks])
    print(f'String of top item of each stack: {stack_top_string}.')            
 
if __name__ == '__main__':
    main()
