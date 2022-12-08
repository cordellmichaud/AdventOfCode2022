from collections import deque
import dataclasses
import functools
import pathlib
import sys
from typing import Self, Sequence, Optional


@dataclasses.dataclass(unsafe_hash=True, frozen=False)
class Node:
    name: str
    is_file: bool
    parent: Optional[Self] = None
    children: list[Self] = dataclasses.field(default_factory=list, hash=False)
    size: int = 0
    
@functools.cache
def calculate_total_size(node: Node) -> int:
    if node.is_file or not node.children:
        return node.size
    
    return sum(calculate_total_size(child) for child in node.children)

def main():
    input_path = pathlib.Path(sys.argv[0]).parent / 'input.txt'
    
    total_size_selected_dirs: int = 0
    upper_size_limit: int = 100000
    dir_stack: deque[Node] = deque()
    root = Node('/', False)
    dir_stack.appendleft(root)
    with input_path.open('r') as input_file:
        current_node: Node = root
        for line in input_file:
            line = line.strip()
            
            if line.startswith('$ cd'):
                to_dir: str = line.split()[2]
                
                if to_dir == '/':
                    current_node = root
                    continue
                
                if to_dir == '..':
                    if current_node is not None:
                        current_node = current_node.parent
                    continue
                
                matching_children: Sequence[Node] = [
                    child for child in current_node.children
                    if child.name == to_dir]
                if matching_children:
                    current_node = matching_children[0]
                    continue
                
                new_child = Node(to_dir, False, parent=current_node)
                current_node.children.append(new_child)
                dir_stack.appendleft(new_child)
                continue
            
            if line.startswith('$ ls'):
                continue
            
            split_line: list[str] = line.split()
            name: str = split_line[1]
            if split_line[0] == 'dir':
                new_child = Node(name, False, parent=current_node)
                current_node.children.append(new_child)
                dir_stack.appendleft(new_child)
                continue
            
            current_node.children.append(
                Node(name, True, parent=current_node, size=int(split_line[0])))
        
        while dir_stack:
            current_size: int = calculate_total_size(dir_stack.popleft())
            if current_size <= upper_size_limit:
                total_size_selected_dirs += current_size
    
    print('The sum of the total sizes of directories with total size at most '
          f'100000: {total_size_selected_dirs}.')
 
if __name__ == '__main__':
    main()
