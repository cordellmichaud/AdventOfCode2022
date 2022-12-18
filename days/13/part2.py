from collections import deque
import functools
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

def parse_packets_file(file_path: str | Path) -> list[list]:
    file_path = Path(file_path)
    
    with file_path.open('r') as file:
        return [parse_list_str(line.strip()) for line in file if line.strip()]

def main():
    input_path = Path(sys.argv[0]).parent / 'input.txt'
    
    packets = parse_packets_file(input_path)
    
    divider_start_packet = [[2]]
    divider_stop_packet = [[6]]
    packets.extend([divider_start_packet, divider_stop_packet])
    
    packets.sort(key=functools.cmp_to_key(compare))
    
    divider_start_index = None
    divider_stop_index = None
    for packet_index, packet in enumerate(packets, start=1):
        if packet == divider_start_packet:
            divider_start_index = packet_index
        elif packet == divider_stop_packet:
            divider_stop_index = packet_index
    
    decoder_key = divider_start_index * divider_stop_index
    
    print(f'Decoder key: {decoder_key}.')
    
if __name__ == '__main__':
    main()
