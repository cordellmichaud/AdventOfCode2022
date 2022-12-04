import pathlib
import sys


def main():
    input_path: pathlib.Path = pathlib.Path(sys.argv[0]).parent / 'input.txt'

    highest_calories: int = 0
    current_calories: int = 0
    with input_path.open("r") as input_file:
        for line in input_file:
            line = line.strip()
            if line:
                current_calories += int(line)
            else:  
                if current_calories > highest_calories:
                    highest_calories = current_calories
                current_calories = 0
    
    if current_calories > highest_calories:
        highest_calories = current_calories
    
    print(f'Highest calories: {highest_calories}.')
            
if __name__ == '__main__':
    main()
