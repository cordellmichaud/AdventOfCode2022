import pathlib
import sys


Point = tuple[int ,int]

def perform_move(knots: list[Point], 
                 direction: Point) -> list[Point]:
    
    for index in range(len(knots)):
        if index == 0:
            knots[0] = (knots[0][0] + direction[0],
                        knots[0][1] + direction[1])
            continue
        next_knot_diff = (knots[index - 1][0] - knots[index][0], 
                          knots[index - 1][1] - knots[index][1])
        match next_knot_diff:
            case (dx, dy) if abs(dx) <= 1 and abs(dy) <= 1:
                break
            case (dx, 0):
                knots[index] = (knots[index][0] + (1 if dx > 0 else -1), 
                                knots[index][1])
            case (0, dy):
                knots[index] = (knots[index][0], 
                                knots[index][1] + (1 if dy > 0 else -1))
            case (dx, dy) if abs(dx) == 1 and abs(dy) == 2:
                knots[index] = (knots[index][0] + dx, 
                                knots[index][1] + (1 if dy > 0 else -1))
            case (dx, dy) if abs(dx) == 2 and abs(dy) == 1:
                knots[index] = (knots[index][0] + (1 if dx > 0 else -1), 
                                knots[index][1] + dy)
            case (dx, dy) if abs(dx) == 2 and abs(dy) == 2:
                knots[index] = (knots[index][0] + (1 if dx > 0 else -1),
                                knots[index][1] + (1 if dy > 0 else -1))
            case _:
                raise ValueError('Invalid initial rope arrangement:\n'
                                 f'{knots}')
    
    return knots

def main():
    input_path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    
    knots = [(0, 0) for _ in range(10)]
    
    tail_positions: set[Point] = set()
    
    with input_path.open('r') as input_file:
        for line in input_file:
            split_line: list[str] = line.strip().split()
            direction = split_line[0]
            units = int(split_line[1])
            match direction:
                case 'L':
                    translation = (-1, 0)
                case 'R':
                    translation = (1, 0)
                case 'U':
                    translation = (0, 1)
                case 'D':
                    translation = (0, -1)
                case _:
                    raise ValueError('Not one of L, R, U, or D.')
            
            for _ in range(units):
                knots = perform_move(knots, translation)
                tail_positions.add(knots[-1])
    
    unique_positions = len(tail_positions)
    
    print('The number of unique positions visited by the tail of the rope: '
          f'{unique_positions}.')
 
if __name__ == '__main__':
    main()
