from collections import deque
from typing import List, Optional, Tuple
class GridSquare:
    def __init__(self, display_str: str="_", is_blocked=False):
        self.display_str = display_str
        self.combattant = None
        self.is_blocked = is_blocked
        pass

    def __str__(self):
        return self.display_str

class BattleGrid:
    def __init__(self, row_size: int, column_size: int):
        self.row_size = row_size
        self.column_size = column_size
        self.grid = [[GridSquare() for i in range(row_size)] for j in range(column_size)]

    def is_coord_in_grid(self, coord: Tuple[int, int]):
        x, y = coord[0], coord[1]
        return (-1 < x < self.row_size and -1 < y < self.column_size)

    def is_coord_blocked(self, coord):
        return self.grid[coord[0]][coord[1]].is_blocked

    def get_walkable_path_from_coord1_to_coord2(self, coord1: Tuple[int,int], coord2: Tuple[int, int]):
        seen = set()
        current_coord = None
        q = deque()
        q.append((coord1, []))

        while q:
            for _ in range(len(q)):
                current_coord, current_path = q.popleft()
                if current_coord == coord2:
                    return current_path
                x, y = current_coord[0], current_coord[1]
                neighboring_coords = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                current_path = current_path + [current_coord]
                for coord in neighboring_coords:
                    if coord not in seen and self.is_coord_in_grid(coord) and not self.is_coord_blocked(coord):
                        seen.add(coord)
                        q.append((coord, current_path))

        return None

    def walking_distance_from_coord1_to_coord2(self, coord1: Tuple[int,int], coord2: Tuple[int, int]):
        path = self.get_walkable_path_from_coord1_to_coord2(coord1, coord2)
        return 5 * len(path) if path else -1

    # See https://forum.gamemaker.io/index.php?threads/how-to-find-every-square-a-line-passes-through.101130/
    def get_line_from_coord1_to_coord2(self, coord1: Tuple[int,int], coord2: Tuple[int, int]) -> List[Tuple[int, int]]:
        coordinates_in_line = [coord1]
        def get_progress(start: int, finish: int, value: int):
            full_dist = finish - start
            current_dist = finish - value
            if start == finish:
                return 1
            elif not((full_dist >=0 and current_dist >= 0) or (full_dist < 0 and current_dist < 0)):
                return 1
            return (float(value-start) / full_dist)

        x1, x2, y1, y2 = coord1[0], coord2[0], coord1[1], coord2[1]
        x_dir = 1 if x2 > x1 else -1
        x_current = x1
        x_next = x_current + 1 if x2 > x1 else x_current
        x_progress = get_progress(x1, x2, x_next)

        y_dir = 1 if y2 > y1 else -1
        y_current = y1
        y_next = y_current + 1 if y2 > y1 else y_current
        y_progress = get_progress(y1, y2, y_next)

        while (x_progress < 1 or y_progress < 1):
            move_x = x_progress <= y_progress
            move_y = y_progress <= x_progress

            if move_x:
                x_current += x_dir
                x_next += x_dir
                x_progress = get_progress(x1, x2, x_next)
            if move_y:
                y_current += y_dir
                y_next += y_dir
                y_progress = get_progress(y1, y2, y_next)
            coordinates_in_line.append((x_current, y_current))

        coordinates_in_line.append(coord2)
        return coordinates_in_line

    def has_line_of_sight(self, coord1: Tuple[int, int], coord2: Tuple[int, int]):
        line = self.get_line_from_coord1_to_coord2(coord1, coord2)
        for coord in line:
            if self.get_coord(coord).is_blocked:
                return False
        return True

    def get_coord(self, coord: Tuple[int, int]) -> Optional[GridSquare]:
        return self.grid[coord[0]][coord[1]]

    def __str__(self):
        rows = []
        for row in self.grid:
            row_str = "".join([str(col) for col in row])
            rows.append(row_str)
        return "\n".join(rows)
