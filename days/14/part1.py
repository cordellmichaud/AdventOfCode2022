from dataclasses import dataclass, field
from itertools import pairwise
from functools import reduce
from pathlib import Path
import sys
from typing import Optional, Self


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int
    
    def is_between(self, start: Self, end: Self) -> bool:
        between_x = (
            (start.x <= self.x <= end.x) or (end.x <= self.x <= start.x))
        between_y = (
            (start.y <= self.y <= end.y) or (end.y <= self.y <= start.y))
        return between_x and between_y

@dataclass
class Rock:
    endpoints: list[Point]
    
    def collides(self, point: Point) -> bool:
        for start, end in pairwise(self.endpoints):
            if point.is_between(start, end):
                return True
        return False

@dataclass
class RockGroup:
    rocks: list[Rock] = field(default_factory=list)
    
    def add_rock(self, rock: Rock):
        self.rocks.append(rock)
    
    def collides(self, point: Point) -> bool:
        for rock in self.rocks:
            if rock.collides(point):
                return True
        return False

def draw_map(rock_group: RockGroup, sands: list[Point], 
             bbox: tuple[Point, Point]):
    print('    ' 
          + ' '.join(f'{col:0>3}' for col in range(bbox[0].x, bbox[1].x + 1)))
    for y in range(bbox[0].y, bbox[1].y + 1):
        line = f'{y:0>3} '
        for x in range(bbox[0].x, bbox[1].x + 1):
            if (x, y) == (500, 0):
                line += ' +  '
            elif rock_group.collides(Point(x, y)):
                line += ' #  '
            elif Point(x, y) in sands:
                line += ' &  '
            else:
                line += ' .  '
        print(line)

def parse_rock_file(file_path: str | Path) \
    -> tuple[RockGroup, tuple[Point, Point]]:
    rock_group = RockGroup()
    x_bounds: Optional[list[int]] = [500, 500]
    y_bounds: Optional[list[int]] = [0, 0]
    
    file_path = Path(file_path)
    
    with file_path.open('r') as file:
        for line in file:
            line = line.strip()
            if line:
                points: list[Point] = []
                point_pair_strs: list[list[str]] = [
                    line_split.split(',') for line_split in line.split()[::2]]
                for x_str, y_str in point_pair_strs:
                    x = int(x_str)
                    y = int(y_str)
                    if x < x_bounds[0]:
                        x_bounds[0] = x
                    if x > x_bounds[1]:
                        x_bounds[1] = x
                    
                    if y < y_bounds[0]:
                        y_bounds[0] = y
                    if y > y_bounds[1]:
                        y_bounds[1] = y
                points = [
                    Point(int(x_str), int(y_str)) 
                    for x_str, y_str in point_pair_strs]
                rock_group.add_rock(Rock(points))
    
    return rock_group, (Point(x_bounds[0], y_bounds[0]), 
                        Point(x_bounds[1], y_bounds[1]))

def simulate_sand(source_pos: Point, rock_group: RockGroup, 
                  sands: dict[Point, int], 
                  bbox: tuple[Point, Point]) -> Optional[Point]:
    current_pos = source_pos
    
    while current_pos.x >= bbox[0].x and current_pos.x <= bbox[1].x \
        and current_pos.y >= bbox[0].y and current_pos.y <= bbox[1].y:
        down_pos = Point(current_pos.x, current_pos.y + 1)
        dleft_pos = Point(current_pos.x - 1, current_pos.y + 1)
        dright_pos = Point(current_pos.x + 1, current_pos.y + 1)
        
        down_collides = rock_group.collides(down_pos) or down_pos in sands
        dleft_collides = rock_group.collides(dleft_pos) or dleft_pos in sands
        dright_collides = rock_group.collides(dright_pos) or dright_pos in sands
            
        if not down_collides:
            current_pos = down_pos
        elif not dleft_collides:
            current_pos = dleft_pos
        elif not dright_collides:
            current_pos = dright_pos
        else:
            if current_pos == source_pos:
                return None
            
            return current_pos

    return None

def main():
    input_path = Path(sys.argv[0]).parent / 'input.txt'
    
    rock_group, bbox = parse_rock_file(input_path)

    sands: dict[Point, int] = {}
    
    sand_source = Point(500, 0)
    
    sand_count = 0
    sand_pos = sand_source
    
    while sand_pos is not None:
        sand_pos = simulate_sand(sand_source, rock_group, sands, bbox)
        if sand_pos is not None:
            sands[sand_pos] = 1
            sand_count += 1
    
    print(f'Units of rested sand: {sand_count}.')
    
if __name__ == '__main__':
    main()
