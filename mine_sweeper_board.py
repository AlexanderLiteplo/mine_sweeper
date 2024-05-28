import random
from constants import NO_MINE, MINE

class MineSweeperBoard:
    def __init__(self, num_mines, grid_size):
        """
        Initialize the MineSweeperBoard with the given number of mines and grid size.
        
        :param num_mines: int, the number of mines to be placed on the board
        :param grid_size: tuple, the size of the grid as (rows, columns)
        """
        self._validate_input(num_mines, grid_size)
        self.num_mines = num_mines
        self.grid_size = grid_size
        self.board = self._create_empty_board()
        
    def _validate_input(self, num_mines, grid_size):
        """
        Validate the input parameters for the MineSweeperBoard.
        
        :param num_mines: int, the number of mines to be placed on the board
        :param grid_size: tuple, the size of the grid as (rows, columns)
        :raises ValueError: if the input parameters are invalid
        """
        if not isinstance(num_mines, int) or not isinstance(grid_size, tuple):
            raise ValueError("Number of mines must be an integer and grid size must be a tuple.")
        
        if len(grid_size) != 2 or not all(isinstance(dim, int) for dim in grid_size):
            raise ValueError("Grid size must be a tuple of two integers.")
        
        rows, cols = grid_size
        if num_mines < 0 or rows <= 1 or cols <= 1:
            raise ValueError("Number of mines must be non-negative and grid dimensions must be greater than 1.")
        
        total_cells = rows * cols
        if num_mines >= total_cells:
            raise ValueError("Number of mines cannot be equal to or exceed the number of cells on the board.")

    def _create_empty_board(self):
        """
        Create an empty board based on the grid size.
        
        :return: list of lists, representing the empty board
        """
        rows, cols = self.grid_size
        empty_board = []
        for _ in range(rows):
            row = [NO_MINE for _ in range(cols)]
            empty_board.append(row)
        return empty_board

    def place_mines(self, first_click_location):
        """
        Fill the board randomly with num_mines mines. Mines cannot be placed
        at the first click location.
        
        :param first_click_location: tuple, the (row, col) location of the first click
        """
        rows, cols = self.grid_size
        total_cells = rows * cols
        
        # ensure first click location is on the board
        r, c = first_click_location
        if r < 0 or r >= rows or c < 0 or c >= cols:
            raise ValueError("First click location is not on the board.")

        if self.num_mines >= total_cells:
            raise ValueError("Number of mines cannot be equal to or exceed the number of cells on the board.")
        
        available_positions = [(r, c) for r in range(rows) for c in range(cols) if (r, c) != first_click_location]

        mine_positions = random.sample(available_positions, self.num_mines)

        for r, c in mine_positions:
            self.board[r][c] = MINE
            
    def print(self):
        """
        Print the board to the console with 0's for no mines and 1's for mines.
        """
        for row in self.board:
            print(" ".join('1' if cell == MINE else '0' for cell in row))