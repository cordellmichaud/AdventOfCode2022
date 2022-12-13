import pathlib
import sys
from typing import TextIO

import numpy as np
import numpy.typing as npt


def input_file_as_np_txt(file: TextIO):
    for line in file:
        yield ' '.join(char for char in line)

def calculate_visibility_map(arr: npt.NDArray) -> npt.NDArray[np.bool_]:
    running_max_vertical: npt.NDArray[np.int8] = np.min(
        np.stack(
            (np.maximum.accumulate(arr, axis=0),
             np.maximum.accumulate(arr[::-1], axis=0)[::-1]), 
            axis=2), 
        axis=2)
    running_max_horizontal: npt.NDArray[np.int8] = np.min(
        np.stack(
            (np.maximum.accumulate(arr, axis=1),
             np.maximum.accumulate(arr[:, ::-1], axis=1)[:, ::-1]), 
            axis=2), 
        axis=2)
    
    visibility_map: npt.NDArray[np.bool8] = np.full(arr.shape, True)
    
    for row in np.arange(arr.shape[0]):
        for col in np.arange(arr.shape[1]):
            match (row, col):
                case (y, x) if (
                    y == 0 or x == 0 
                    or y == arr.shape[0] - 1 or x == arr.shape[1] - 1):
                    visibility_map[row, col] = 1
                case _:
                    visibility_map[row, col] = (
                        arr[row, col] > min(
                            [running_max_vertical[row - 1, col],
                             running_max_vertical[row + 1, col],
                             running_max_horizontal[row, col - 1],
                             running_max_horizontal[row, col + 1]]))
    
    return visibility_map

def main():
    input_path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    
    with input_path.open('r') as input_file:
        height_map: npt.NDArray[np.int8] = np.loadtxt(
            input_file_as_np_txt(input_file), dtype=np.int8)
    
    visibility_map: npt.NDArray[np.bool_] = calculate_visibility_map(height_map)
    
    num_trees: int = np.count_nonzero(visibility_map)
    
    print(f"Number of visible trees: {num_trees}.")
 
if __name__ == '__main__':
    main()
