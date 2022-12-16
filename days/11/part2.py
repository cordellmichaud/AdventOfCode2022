from collections import deque
from dataclasses import dataclass, field, InitVar
import math
from pathlib import Path
import sys
from typing import Callable, Optional, Self


def mod_add(a: int, b: int, mod_divisor: int) -> int:
    return (a + b) % mod_divisor

def mod_mul(a: int, b: int, mod_divisor: int) -> int:
    return (a * b) % mod_divisor

@dataclass(order=True)
class Monkey:
    monkey_id: int = field(compare=False)
    items: deque[int] = field(compare=False)
    op_a: str | int = field(compare=False)
    operation_str: InitVar[str] = field(compare=False)
    op_b: str | int = field(compare=False)
    test_divisor: int = field(compare=False)
    test_target_true: InitVar[int] = field(compare=False)
    test_target_false: InitVar[int] = field(compare=False)
    
    total_items_inspected: int = field(default=0, init=False, compare=True)
    op_func: Callable[[int, int], int] = field(init=False, compare=False)
    test_targets: dict[bool, int] = field(init=False, compare=False)
    
    def __post_init__(self, operation_str, test_target_true, test_target_false):
        if operation_str == '+':
            self.op_func = mod_add
        else:
            self.op_func = mod_mul
        
        self.test_targets = {
            True: test_target_true,
            False: test_target_false
        }
        
    def take_turn(self, monkeys: list[Self], divisor_common_multiple: int):
        while self.items:
            self.total_items_inspected += 1
            current_item: int = self.items.popleft()
            
            match (self.op_a, self.op_b):
                case ('old', 'old'):
                    current_item = self.op_func(current_item, current_item, 
                                                divisor_common_multiple)
                case ('old', num) | (num, 'old'):
                    current_item = self.op_func(current_item, num, 
                                                divisor_common_multiple)
                case _:
                    current_item = self.op_func(self.op_a, self.op_b,
                                                divisor_common_multiple)
            
            test_result = current_item % self.test_divisor == 0
            target_monkey_index: int = self.test_targets[test_result]
            monkeys[target_monkey_index].items.append(current_item)

def parse_items(items_line: str) -> deque[str]:
    split_items_line = items_line.split()
    if len(split_items_line) < 3:
        return deque()
    
    return deque([int(item[:-1]) if ',' in item else int(item) 
                  for item in items_line.split()[2:]])

def parse_operation(operation_line: str) -> tuple[str | int, str, str | int]:
    split_operation_line = operation_line.split()
    op_a: str | int = (split_operation_line[3] 
                       if split_operation_line[3] == "old" 
                       else int(split_operation_line[3]))
    op_str = split_operation_line[4]
    op_b: str | int = (split_operation_line[5] 
                       if split_operation_line[5] == "old" 
                       else int(split_operation_line[5]))
    
    return op_a, op_str, op_b

def parse_test_divisor(test_line: str) -> int:
    return int(test_line.split()[3])

def parse_conditional_monkey_index(conditional_monkey_str: str) -> int:
    return int(conditional_monkey_str.split()[5])

def parse_monkey_file(file_path: str | Path) -> list[Monkey]:
    monkeys: list[Monkey] = []
    
    with file_path.open('r') as input_file:
        items: Optional[deque[int]] = None
        op_a: Optional[str | int] = None
        op_str: Optional[str] = None
        op_b: Optional[str] = None
        test_divisor: Optional[int] = None
        true_monkey_index: Optional[int] = None
        false_monkey_index: Optional[int] = None
        
        for line in input_file:
            line = line.strip()
            
            if line.startswith("Monkey"):
                items = None
                op_a = None
                op_str = None
                op_b = None
                test_divisor = None
                true_monkey_index = None
                false_monkey_index = None
                continue
            
            if line.startswith('Starting items:'):
                items = parse_items(line)
                continue
            
            if line.startswith('Operation:'):
                op_a, op_str, op_b = parse_operation(line)
                continue
            
            if line.startswith('Test:'):
                test_divisor = parse_test_divisor(line)
                continue
            
            if line.startswith('If true:'):
                true_monkey_index = parse_conditional_monkey_index(line)
                continue
            
            if line.startswith('If false:'):
                false_monkey_index = parse_conditional_monkey_index(line)
                monkeys.append(
                    Monkey(len(monkeys), items, op_a, op_str, op_b, 
                           test_divisor, true_monkey_index, false_monkey_index))
                continue
    
    return monkeys

def main():
    input_path = Path(sys.argv[0]).parent / 'input.txt'
    
    monkeys: list[Monkey] = parse_monkey_file(input_path)
    
    least_common_multiple: int = math.lcm(
        *(monkey.test_divisor for monkey in monkeys))
    
    total_rounds = 10000
    for _ in range(total_rounds):
        for monkey in monkeys:
            monkeys[monkey.monkey_id].take_turn(monkeys, least_common_multiple)

    for monkey in monkeys:
        print(f'Monkey {monkey.monkey_id} inspected items '
              f'{monkey.total_items_inspected} times.')
    
    # Sort by items inspected
    monkeys.sort(reverse=True)
    
    monkey_business: int = (
        monkeys[0].total_items_inspected * monkeys[1].total_items_inspected)
    
    print(f'\nLevel of monkey business after {total_rounds} rounds: '
          f'{monkey_business}.')
    
if __name__ == '__main__':
    main()
