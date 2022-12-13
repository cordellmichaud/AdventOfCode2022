import pathlib
import sys


Point = tuple[int ,int]

def perform_move(head: Point, tail: Point, 
                 direction: Point) -> tuple[Point, Point]:
    
    new_head = (head[0] + direction[0], 
                head[1] + direction[1])
    head_tail_diff = (new_head[0] - tail[0], 
                      new_head[1] - tail[1])
    match head_tail_diff:
        case (dx, dy) if abs(dx) <= 1 and abs(dy) <= 1:
            new_tail = tail
        case (dx, 0):
            new_tail = (tail[0] + direction[0], tail[1])
        case (0, dy):
            new_tail = (tail[0], tail[1] + direction[1])
        case (dx, dy) if abs(dx) == 1 and abs(dy) == 2:
            new_tail = (tail[0] + dx, tail[1] + direction[1])
        case (dx, dy) if abs(dx) == 2 and abs(dy) == 1:
            new_tail = (tail[0] + direction[0], tail[1] + dy)
        case _:
            raise ValueError('Invalid initial rope arrangement.')
    
    return new_head, new_tail

def main():
    input_path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    
    head = (0, 0)
    tail = (0, 0)
    
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
                head, tail = perform_move(head, tail, translation)
                tail_positions.add(tail)
    
    unique_positions = len(tail_positions)
    
    print('The number of unique positions visited by the tail of the rope: '
          f'{unique_positions}.')
 
if __name__ == '__main__':
    main()
