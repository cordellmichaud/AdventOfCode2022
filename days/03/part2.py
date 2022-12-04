import pathlib
import sys
from typing import Optional


def get_duplicated(rucksacks: list[str]) -> Optional[str]:
    rucksack_sets: list[set[str]] = [set(rucksack) for rucksack in rucksacks]
    
    duplicate: Optional[str] = None
    for char in rucksack_sets[0]:
        if all(char in rucksack_set for rucksack_set in rucksack_sets[1:]):
            duplicate = char
            break
    
    return duplicate

def get_priority(letter: str) -> int:
    priority: int = ord(letter) - 38 if letter.isupper() else ord(letter) - 96
    return priority

def main():
    input_path: pathlib.Path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    total_priority: int = 0
    
    with input_path.open('r') as input_file:
        rucksacks: list[str] = []
        for line in input_file:
            rucksacks.append(line.strip())
            
            if len(rucksacks) == 3:
                total_priority += get_priority(get_duplicated(rucksacks))
                rucksacks.clear()
    
    print(f'Total priority: {total_priority}.')

if __name__ == '__main__':
    main()
