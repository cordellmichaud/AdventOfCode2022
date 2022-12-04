import dataclasses
import pathlib
import sys
from typing import Self, Sequence


@dataclasses.dataclass(order=True)
class SectionRange:
    start: int
    end: int
    
    def __contains__(self, other: Self | Sequence | int) -> bool:
        if isinstance(other, SectionRange):
            return other.start >= self.start and other.end <= self.end
        
        if isinstance(other, Sequence):
            return other[0] >= self.start and other[-1] <= self.end
        
        if isinstance(other, int):
            return self.start <= other <= self.end

def parse_line(line: str) -> tuple[SectionRange, SectionRange]:
    return tuple(SectionRange(*[int(num) for num in section_str.split('-')]) 
                 for section_str in line.strip().split(','))

def main():
    input_path: pathlib.Path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    contain_count: int = 0
    
    with input_path.open('r') as input_file:
        for line in input_file:
            section1, section2 = parse_line(line)
            if section1 in section2 or section2 in section1:
                contain_count += 1
    
    print(f'Contain count: {contain_count}.')
 
if __name__ == '__main__':
    main()
