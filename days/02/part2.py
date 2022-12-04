import enum
import pathlib
import sys


class Hand(enum.IntEnum):
    ROCK: int = 1
    PAPER: int = 2
    SCISSORS: int = 3

play_values: dict[str, int] = {
    'A': Hand.ROCK,
    'B': Hand.PAPER,
    'C': Hand.SCISSORS
}

def calculate_score(strategy: str) -> int:
    strategy_split: list[str] = strategy.split()
    opp: Hand = play_values[strategy_split[0]]
    end_condition: str = strategy_split[1]
    score: int = 0
    
    match [opp, end_condition]:
        case [_, 'Y']:
            score += 3 + opp
        case [Hand.ROCK, _]:
            score += 6 + Hand.PAPER if end_condition == 'Z' else Hand.SCISSORS
        case [Hand.PAPER, _]:
            score += 6 + Hand.SCISSORS if end_condition == 'Z' else Hand.ROCK
        case [Hand.SCISSORS, _]:
            score += 6 + Hand.ROCK if end_condition == 'Z' else Hand.PAPER
    
    return score

def main():
    input_path: pathlib.Path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    total_score: int = 0
    with input_path.open("r") as input_file:
        total_score = sum(
            calculate_score(line.strip()) for line in input_file)
    print(f'Total score: {total_score}.')

if __name__ == '__main__':
    main()
