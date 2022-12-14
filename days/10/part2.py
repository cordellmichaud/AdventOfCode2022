from collections import deque
import pathlib
import sys


def process_crt(cycle: int, x: int, crt: list[list[str]]):
    crt_sample = (cycle - 1) % 40
    crt_line = (cycle - 1) // 40
    
    if x - 1 <= crt_sample <= x + 1:
        crt[crt_line][crt_sample] = '#'

def main():
    input_path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    x = 1
    op_queue: deque[tuple[int, int]] = deque()
    cycle = 1
    crt_output = [['.' for _ in range(40)] for _ in range(6)]

    with input_path.open('r') as input_file:
        for line in input_file:
            line = line.strip()
            
            if op_queue:
                x += op_queue.pop()
            
            if 'addx' in line:
                op_queue.appendleft(0)
                op_queue.appendleft(int(line.split()[1]))
            
            if 'noop' in line:
                op_queue.appendleft(0)
            
            process_crt(cycle, x, crt_output)
            
            cycle += 1
    
    while op_queue:
        x += op_queue.pop()
        
        process_crt(cycle, x, crt_output)
        
        cycle += 1
     
    for line in crt_output:
        print(''.join(line))
    
if __name__ == '__main__':
    main()
