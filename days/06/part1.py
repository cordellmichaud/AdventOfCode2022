from collections import Counter, deque
import pathlib
import sys


def main():
    input_path: pathlib.Path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    
    chars_processed: int = 0
    with input_path.open('r') as input_file:
        char_window: deque[str] = deque()
        for char_index, char in enumerate(input_file.read().strip()):
            char_window.appendleft(char)
            if char_index > 3:
                char_window.pop()
                if len(Counter(char_window)) == 4:
                    chars_processed = char_index + 1
                    break
    
    print('Characters processed before the first start-of-packet marker is '
          f'detected: {chars_processed}.')        
 
if __name__ == '__main__':
    main()
