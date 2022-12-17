from pathlib import Path
import sys
from typing import Optional

import networkx as nx


def get_height_of_char(char: str) -> int:
    match char:
        case 'S':
            return ord('a')
        case 'E':
            return ord('z')
        case _:
            return ord(char)

def construct_graph(elevation_map_file_path: str | Path) \
    -> tuple[nx.DiGraph, tuple[int, int], tuple[int, int]]:
    elevation_map_file_path = Path(elevation_map_file_path)
    
    hill_graph = nx.DiGraph()
    max_x = 0
    max_y = 0
    source_pos: Optional[tuple[int, int]] = None
    target_pos: Optional[tuple[int, int]] = None
    
    # Create graph nodes
    with elevation_map_file_path.open('r') as file:
        for y, line in enumerate(line.strip() for line in file):
            if y > max_y:
                max_y = y
            for x, char in enumerate(line):
                if x > max_x:
                    max_x = x
                if char == 'S':
                    source_pos = (x, y)
                elif char == 'E':
                    target_pos = (x, y)
                
                hill_graph.add_node((x, y), height=get_height_of_char(char))
    
    # Create directed graph edges
    for x, y in hill_graph.nodes:
        if (x - 1 >= 0 
            and hill_graph.nodes[(x - 1, y)]['height'] 
            <= hill_graph.nodes[(x, y)]['height'] + 1):
            hill_graph.add_edge((x, y), (x - 1, y), weight=1)
        
        if (x + 1 <= max_x 
            and hill_graph.nodes[(x + 1, y)]['height'] 
            <= hill_graph.nodes[(x, y)]['height'] + 1):
            hill_graph.add_edge((x, y), (x + 1, y), weight=1)
        
        if (y - 1 >= 0 
            and hill_graph.nodes[(x, y - 1)]['height'] 
            <= hill_graph.nodes[(x, y)]['height'] + 1):
            hill_graph.add_edge((x, y), (x, y - 1), weight=1)
        
        if (y + 1 <= max_y 
            and hill_graph.nodes[(x, y + 1)]['height'] 
            <= hill_graph.nodes[(x, y)]['height'] + 1):
            hill_graph.add_edge((x, y), (x, y + 1), weight=1)
    
    return hill_graph, source_pos, target_pos

def main():
    input_path = Path(sys.argv[0]).parent / 'input.txt'
    
    hill_graph, source_pos, target_pos = construct_graph(input_path)
    
    shortest_path_length = nx.dijkstra_path_length(hill_graph, source_pos, 
                                                   target_pos)
    print(f'Shortest path length: {shortest_path_length}.')
    
if __name__ == '__main__':
    main()
