from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path
import sys
from typing import Iterable, Optional, Self


def manhattan_dist(point1: tuple[int, int], point2: tuple[int, int]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

@dataclass
class SensorRegion:
    sensor_pos: tuple[int, int]
    beacon_pos: tuple[int, int]
    manhattan_radius: int = field(init=False)
    
    def __post_init__(self):
        self.manhattan_radius = manhattan_dist(self.beacon_pos, self.sensor_pos)
    
    def __contains__(self, point: tuple[int, int]):
        match point:
            case (None, None):
                return False
            case (x, None):
                lower_x = self.sensor_pos[0] - self.manhattan_radius
                upper_x = self.sensor_pos[0] + self.manhattan_radius
                return lower_x <= x <= upper_x
            case (None, y):
                lower_y = self.sensor_pos[1] - self.manhattan_radius
                upper_y = self.sensor_pos[1] + self.manhattan_radius
                return lower_y <= y <= upper_y
            case (x, y):
                return (manhattan_dist(point, self.sensor_pos) 
                        <= self.manhattan_radius)
            case _:
                return False
    
    def get_x_range(self, y: int) -> tuple[int, int]:
        if (None, y) not in self:
            return None
        
        dx = self.manhattan_radius - manhattan_dist((self.sensor_pos[0], y), 
                                                    self.sensor_pos)
        return (self.sensor_pos[0] - dx, self.sensor_pos[0] + dx)
    
    def get_y_range(self, x: int) -> tuple[int, int]:
        if (x, None) not in self:
            return None
        
        dy = self.manhattan_radius - manhattan_dist((x, self.sensor_pos[1]),
                                                    self.sensor_pos)
        return (self.sensor_pos[1] - dy, self.sensor_pos[1] + dy)

def parse_sensor_file(file_path: Path) -> list[SensorRegion]:
    sensor_regions: list[SensorRegion] = []
    
    with file_path.open('r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            line_split = line.split()
            sensor_pos = (int(line_split[2][2:-1]), int(line_split[3][2:-1]))
            beacon_pos = (int(line_split[8][2:-1]), int(line_split[9][2:]))
            sensor_region = SensorRegion(sensor_pos, beacon_pos)
            sensor_regions.append(sensor_region)
    
    return sensor_regions

def main():
    input_path = Path(sys.argv[0]).parent / 'input.txt'
    
    sensor_regions: list[SensorRegion] = parse_sensor_file(input_path)
    
    row_of_interest = 2000000
    
    relevant_sensor_x_ranges = [
        sensor_region.get_x_range(row_of_interest) 
        for sensor_region in sensor_regions
        if sensor_region.get_x_range(row_of_interest)]
    
    all_x: set[int] = set()
    for x_range in relevant_sensor_x_ranges:
        all_x.update(range(x_range[0], x_range[1]))
    
    print('Positions that cannot contain a beacon at row '
          f'y={row_of_interest}: {len(all_x)}.')
    
if __name__ == '__main__':
    main()
