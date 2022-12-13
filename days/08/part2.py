import pathlib
import sys
from typing import TextIO

import numpy as np
import numpy.typing as npt


def input_file_as_np_txt(file: TextIO):
    for line in file:
        yield ' '.join(char for char in line)

def calculate_visibility_map(arr: npt.NDArray[np.int8]) \
    -> npt.NDArray[np.bool_]:
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

def get_scenic_scores(arr: npt.NDArray[np.int8], 
                      visibility_map: npt.NDArray[np.bool_]) \
    -> npt.NDArray[np.int32]:
    scenic_scores = np.zeros(arr.shape, dtype=np.int32)
    for row in np.arange(arr.shape[0]):
        for col in np.arange(arr.shape[1]):
            if not visibility_map[row, col]:
                continue
            
            up_score: int = 0
            for scan_row in np.arange(row - 1, -1, -1):
                up_score += 1
                if arr[scan_row, col] >= arr[row, col]:
                    break
            
            down_score: int = 0
            for scan_row in np.arange(row + 1, arr.shape[0]):
                down_score += 1
                if arr[scan_row, col] >= arr[row, col]:
                    break
            
            left_score: int = 0
            for scan_col in np.arange(col - 1, -1, -1):
                left_score += 1
                if arr[row, scan_col] >= arr[row, col]:
                    break
            
            right_score: int = 0
            for scan_col in np.arange(col + 1, arr.shape[1]):
                right_score += 1
                if arr[row, scan_col] >= arr[row, col]:
                    break
            
            scenic_score: int = up_score * down_score * left_score * right_score
            
            scenic_scores[row, col] = scenic_score
    
    return scenic_scores

def main():
    input_path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    
    with input_path.open('r') as input_file:
        height_map: npt.NDArray[np.int8] = np.loadtxt(
            input_file_as_np_txt(input_file), dtype=np.int8)
    
    visibility_map: npt.NDArray[np.bool_] = calculate_visibility_map(height_map)

    scenic_scores: npt.NDArray[np.int32] = get_scenic_scores(
        height_map, visibility_map)
    
    highest_scenic_score: int = np.max(scenic_scores)
    
    print('The highest scenic score possible for any tree: '
          f'{highest_scenic_score}')
 
if __name__ == '__main__':
    main()
