import pathlib
import sys
from typing import Optional


def get_duplicated(rucksack: str) -> Optional[str]:
    half_sets: tuple[set[str], set[str]] = (
        set(rucksack[:len(rucksack) // 2]), 
        set(rucksack[len(rucksack) // 2:]))
    
    duplicate: Optional[str] = None
    for char in half_sets[0]:
        if char in half_sets[1]:
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
        total_priority = sum(
            get_priority(get_duplicated(line.strip())) 
            for line in input_file)
    print(f'Total priority: {total_priority}.')

if __name__ == '__main__':
    main()
