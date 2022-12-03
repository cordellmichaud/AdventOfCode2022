import pathlib

def main():
    input_path: pathlib.Path = pathlib.Path('input.txt')

    all_calories: list[int] = []
    current_calories: int = 0
    with input_path.open("r") as input_file:
        for line in input_file:
            line = line.strip()
            if line:
                current_calories += int(line)
            else:  
                all_calories.append(current_calories)
                current_calories = 0
        if current_calories != 0:
            all_calories.append(current_calories)
    
    all_calories.sort(reverse=True)
    top3_sum: list[int] = sum(all_calories[:3])
    print(f'Total calories of top three elves: {top3_sum}.')

if __name__ == '__main__':
    main()
