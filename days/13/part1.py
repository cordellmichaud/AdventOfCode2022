from collections import deque
import json
from pathlib import Path
import sys
from typing import Optional


def compare(left: list, right: list) -> int:
    l_queue, r_queue = deque(left), deque(right)
    while l_queue and r_queue:
        l, r = l_queue.popleft(), r_queue.popleft()
        
        match (l, r):
            case (int(), list()):
                comparison = compare([l], r)
                if comparison < 0:
                    return -1
                if comparison > 0:
                    return 1
            case (list(), int()):
                comparison = compare(l, [r])
                if comparison < 0:
                    return -1
                if comparison > 0:
                    return 1
            case (int(), int()):
                if l < r:
                    return -1
                if l > r:
                    return 1
            case (list(), list()):
                comparison = compare(l, r)
                if comparison < 0:
                    return -1
                if comparison > 0:
                    return 1
    if l_queue:
        return 1
    if r_queue:
        return -1
    
    return 0

def parse_list_str(list_str: str) -> list:
    return json.loads(list_str)

def iter_lines_pairwise(file_path: str | Path) -> tuple[str, str, int]:
    file_path = Path(file_path)
    
    line1 = None
    line2 = None
    pair_index = 1
    
    with file_path.open('r') as file:
        for current_line in file:
            current_line = current_line.strip()
            line1 = line2
            line2 = current_line
            
            if line1 and line2:
                yield line1, line2, pair_index
                pair_index += 1
    return

def main():
    input_path = Path(sys.argv[0]).parent / 'input.txt'
    
    correctly_ordered_indices: list[int] = [
        pair_index 
        for line1, line2, pair_index in iter_lines_pairwise(input_path)
        if compare(parse_list_str(line1), parse_list_str(line2)) < 0]
    
    sum_of_ordered_pair_indices = sum(correctly_ordered_indices)
    
    print('Sum of the indices of ordered pairs: '
          f'{sum_of_ordered_pair_indices}.')
    
if __name__ == '__main__':
    main()
