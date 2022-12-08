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
    
    total_disk_space: int = 70000000
    desired_unused_space: int = 30000000
    dir_stack: deque[Node] = deque()
    root = Node('/', False)
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
        
        total_used_space: int = calculate_total_size(root)
        unused_space: int = total_disk_space - total_used_space
        dir_to_remove_and_size: tuple[Node, int] = (root, total_used_space)
        while dir_stack:
            current_dir: Node = dir_stack.popleft()
            current_dir_size: int = calculate_total_size(current_dir)
            
            if current_dir_size < dir_to_remove_and_size[1] and (
                unused_space + current_dir_size >= desired_unused_space):
                dir_to_remove_and_size = (current_dir, current_dir_size)
        
        print('Directory to remove and its size: '
              f'{dir_to_remove_and_size[0].name} {dir_to_remove_and_size[1]}.')
 
if __name__ == '__main__':
    main()
