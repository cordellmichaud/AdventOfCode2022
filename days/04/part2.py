import dataclasses
import pathlib
import sys
from typing import Self, Sequence, Optional


@dataclasses.dataclass(order=True)
class SectionRange:
    start: int
    end: int
    
    def __contains__(self, other: Self | Sequence[int] | int) -> bool:
        if isinstance(other, SectionRange):
            return other.start >= self.start and other.end <= self.end
        
        if isinstance(other, Sequence):
            return other[0] >= self.start and other[-1] <= self.end
        
        if isinstance(other, int):
            return self.start <= other <= self.end
    
    def overlaps(self, other: Self | Sequence[int] | int) -> Optional[Self]:
        if isinstance(other, SectionRange):
            other_ends: tuple[int, int] = (other.start, other.end)
        elif isinstance(other, Sequence):
            other_ends: tuple[int, int] = (other[0], other[-1])
        else:
            other_ends: tuple[int, int] = (other, other)
        
        if self.start <= other_ends[0] <= self.end:
            return SectionRange(
                other_ends[0], 
                other_ends[1] if other_ends[1] <= self.end else self.end)
        elif other_ends[0] <= self.start <= other_ends[1]:
            return SectionRange(
                self.start,
                self.end if self.end <= other_ends[1] else other_ends[1])
        else:
            return None

def parse_line(line: str) -> tuple[SectionRange, SectionRange]:
    return tuple(SectionRange(*[int(num) for num in section_str.split('-')]) 
                 for section_str in line.strip().split(','))

def main():
    input_path: pathlib.Path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    overlap_count: int = 0
    
    with input_path.open('r') as input_file:
        for line in input_file:
            section1, section2 = parse_line(line)
            if section1.overlaps(section2):
                overlap_count += 1
    
    print(f'Overlap count: {overlap_count}.')
 
if __name__ == '__main__':
    main()
