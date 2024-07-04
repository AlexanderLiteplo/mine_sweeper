import unittest
from constants import NO_MINE, MINE
from mine_sweeper_board import MineSweeperBoard 

class TestMineSweeperBoardInitialization(unittest.TestCase):
    def test_valid_initialization(self):
        board = MineSweeperBoard(10, (5, 5))
        self.assertEqual(board.num_mines, 10)
        self.assertEqual(board.grid_size, (5, 5))
        self.assertEqual(len(board.board), 5)
        self.assertEqual(len(board.board[0]), 5)

    def test_negative_num_mines(self):
        with self.assertRaises(ValueError):
            MineSweeperBoard(-1, (5, 5))

    def test_zero_or_one_grid_size(self):
        with self.assertRaises(ValueError):
            MineSweeperBoard(10, (0, 5))
        
        with self.assertRaises(ValueError):
            MineSweeperBoard(10, (5, 1))
        
        with self.assertRaises(ValueError):
            MineSweeperBoard(10, (1, 5))

    def test_num_mines_exceeds_cells(self):
        with self.assertRaises(ValueError):
            MineSweeperBoard(26, (5, 5))

    def test_non_integer_num_mines(self):
        with self.assertRaises(ValueError):
            MineSweeperBoard("10", (5, 5))

    def test_non_tuple_grid_size(self):
        with self.assertRaises(ValueError):
            MineSweeperBoard(10, [5, 5])

    def test_grid_size_with_non_integer(self):
        with self.assertRaises(ValueError):
            MineSweeperBoard(10, (5.0, 5))
        
        with self.assertRaises(ValueError):
            MineSweeperBoard(10, (5, "5"))

    def test_grid_size_with_more_than_two_elements(self):
        with self.assertRaises(ValueError):
            MineSweeperBoard(10, (5, 5, 5))
            
    def test_mines_not_at_first_click(self):
        board = MineSweeperBoard(10, (5, 5))
        first_click = (2, 2)
        board.place_mines(first_click)
        
        # Ensure no mine is at the first click location
        self.assertEqual(board.board[first_click[0]][first_click[1]], NO_MINE)
        
        # Ensure the correct number of mines are placed
        mine_count = sum(row.count(MINE) for row in board.board)
        self.assertEqual(mine_count, 10)

    def test_mines_placement_on_board(self):
        board = MineSweeperBoard(5, (3, 3))
        first_click = (0, 0)
        board.place_mines(first_click)
        
        # Ensure all mines are within board boundaries
        for row in range(3):
            for col in range(3):
                if board.board[row][col] == MINE:
                    self.assertTrue(0 <= row < 3)
                    self.assertTrue(0 <= col < 3)

    def test_first_click_out_of_bounds(self):
        board = MineSweeperBoard(5, (3, 3))
        with self.assertRaises(ValueError):
            board.place_mines((3, 3))

if __name__ == "__main__":
    unittest.main()
