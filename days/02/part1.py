import enum
import pathlib

class Hand(enum.IntEnum):
    ROCK: int = 1
    PAPER: int = 2
    SCISSORS: int = 3

play_values: dict[str, int] = {
    'A': Hand.ROCK,
    'B': Hand.PAPER,
    'C': Hand.SCISSORS,
    'X': Hand.ROCK,
    'Y': Hand.PAPER,
    'Z': Hand.SCISSORS
}

def calculate_score(strategy: str) -> int:
    hands: list[Hand] = [play_values[play] for play in strategy.split()]
    score: int = hands[1]
    
    match hands:
        case [Hand.ROCK, Hand.PAPER] | [Hand.PAPER, Hand.SCISSORS] \
            | [Hand.SCISSORS, Hand.ROCK]:
            score += 6
        case [opp, player] if opp == player:
            score += 3
    
    return score
            

def main():
    input_path: pathlib.Path = pathlib.Path('input.txt')
    total_score: int = 0
    with input_path.open("r") as input_file:
        total_score = sum(
            calculate_score(line.strip()) for line in input_file)
    print(f'Total score: {total_score}.')

if __name__ == '__main__':
    main()
