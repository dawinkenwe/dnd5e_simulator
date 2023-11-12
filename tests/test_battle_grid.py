from battle_grid import BattleGrid, GridSquare

import unittest


class TestBattleGrid(unittest.TestCase):
    def setUp(self):
        self.grid = BattleGrid(row_size=1, column_size=2)

    def test_grid_to_str(self):
        grid_str = str(self.grid)
        grid2 = BattleGrid(row_size=2, column_size=1)
        grid2_str = str(grid2)

        empty_square = GridSquare()
        expected_str = f"{str(empty_square)}\n{str(empty_square)}"
        expected_str2 = f"{str(empty_square)}{str(empty_square)}"
        self.assertEqual(expected_str2, grid2_str)
        self.assertEqual(expected_str, grid_str)

    def test_grid_to_str_with_special_characters(self):
        empty_square = GridSquare()
        self.grid.grid[0][0].display_str = "^"
        expected_str = f"^\n{str(empty_square)}"
        self.assertEqual(expected_str, str(self.grid))

    def test_walking_distance_from_coord1_to_coord2(self):
        self.grid = BattleGrid(row_size=6, column_size=6)
        wall = GridSquare(is_blocked=True, display_str="*")
        wall_coords = [(0, 1), (1, 1), (2, 1), (3, 1), (5, 1), (5, 2), (5, 3), (4, 3)]
        for x, y in wall_coords:
            self.grid.grid[x][y] = wall
        dist = self.grid.walking_distance_from_coord1_to_coord2((0, 0), (4, 4))
        self.assertEqual(dist, 10*5)
        dist = self.grid.walking_distance_from_coord1_to_coord2((0, 0), (0, 1))
        self.assertEqual(dist, -1)

    def test_coordinates_in_line(self):
        self.grid = BattleGrid(row_size=6, column_size=6)
        expected_line = [(0,0), (1,0), (2,1), (3,1), (4,2)]
        line = self.grid.get_line_from_coord1_to_coord2((0,0), (4,2))
        self.assertEqual(line, expected_line)
        expected_line = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (4, 3)]
        line = self.grid.get_line_from_coord1_to_coord2((0,0), (4,3))
        self.assertEqual(line, expected_line)

    def test_has_line_of_sight(self):
        self.grid = BattleGrid(row_size=6, column_size=6)
        wall = GridSquare(is_blocked=True, display_str="*")
        wall_coords = [(0, 1), (1, 1), (2, 1), (3, 1), (5, 1), (5, 2), (5, 3), (4, 3)]
        for x, y in wall_coords:
            self.grid.grid[x][y] = wall
        expected_value = True
        value = self.grid.has_line_of_sight((0,0), (4,0))
        self.assertEqual(value, expected_value)
        expected_value = True
        value = self.grid.has_line_of_sight((0,0), (4,1))
        self.assertEqual(value, expected_value)
        expected_value = False
        value = self.grid.has_line_of_sight((0,0), (4,2))
        self.assertEqual(value, expected_value)
        expected_value = False
        value = self.grid.has_line_of_sight((0,0), (0,2))
        self.assertEqual(value, expected_value)


if __name__ == '__main__':
    unittest.main()
