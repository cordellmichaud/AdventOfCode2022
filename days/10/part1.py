from collections import deque
import pathlib
import sys


def main():
    input_path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    
    x = 1
    op_queue: deque[tuple[int, int]] = deque()
    cycle = 1
    cycles_of_interest = (20, 60, 100, 140, 180, 220)
    x_by_cycles_of_interest = {}
    
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
            
            if cycle in cycles_of_interest:
                x_by_cycles_of_interest[cycle] = x
            
            cycle += 1
    
    while op_queue:
        x += op_queue.pop()
        
        if cycle in cycles_of_interest:
            x_by_cycles_of_interest[cycle] = x
        
        cycle += 1
    
    for cycle in cycles_of_interest:
        if cycle not in x_by_cycles_of_interest:
            x_by_cycles_of_interest[cycle] = x_by_cycles_of_interest[cycle - 40]
    
    print(x_by_cycles_of_interest)
    
    summed_signal_strengths = sum(
        cycle * x for cycle, x in x_by_cycles_of_interest.items())
    
    print(f'Sum of the six signal strengths: {summed_signal_strengths}.')
    
if __name__ == '__main__':
    main()
