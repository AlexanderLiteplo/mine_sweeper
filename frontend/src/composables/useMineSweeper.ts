import { ref, computed } from 'vue';
import { initializeBoard as apiInitializeBoard, placeMines as apiPlaceMines } from "../api";

export function useMinesweeper() {
  const boardWidth = ref(5);
  const boardHeight = ref(5);
  const numMines = ref(4);
  const firstClickRow = ref(0);
  const firstClickCol = ref(0);
  const board = ref<boolean[][] | null>(null);
  const boardClicks = ref<boolean[][] | null>(null);
  const boardDisplay = ref<string[][] | null>(null);
  const boardClicked = ref(false);
  const gameOver = ref(false);
  const gameTimer = ref<number | null>(null);
  const elapsedTime = ref(0);

  function startTimer() {
    elapsedTime.value = 0;
    gameTimer.value = setInterval(() => {
      elapsedTime.value++;
    }, 1000);
  }

  function stopTimer() {
    if (gameTimer.value) {
      clearInterval(gameTimer.value);
      gameTimer.value = null;
    }
  }

  function formatTimer(seconds: number): string {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  }

  async function initializeBoard() {
    try {
      const response = await apiInitializeBoard(
        boardWidth.value,
        boardHeight.value,
        numMines.value
      );
      console.log(response.data);
      createEmptyBoard();
      stopTimer();
      elapsedTime.value = 0;
    } catch (error) {
      console.error(error);
    }
  }

  async function placeMines() {
    try {
      const response = await apiPlaceMines([
        firstClickRow.value,
        firstClickCol.value,
      ]);
      console.log("Received board from server:");
      printBoard(response.data.board);
      updateBoardWithMines(response.data.board);
      revealSquare(firstClickRow.value, firstClickCol.value);
      updateBoardDisplay();
    } catch (error) {
      console.error(error);
    }
  }

  function printBoard(boardToPrint: boolean[][]) {
    console.log("Current display state:");
    let output = "";
    for (let i = 0; i < boardToPrint.length; i++) {
      for (let j = 0; j < boardToPrint[i].length; j++) {
        output += boardToPrint[i][j] ? "X " : "O ";
      }
      output += "\n";
    }
    console.log(output);
  }

  function createEmptyBoard() {
    board.value = Array.from({ length: boardHeight.value }, () =>
      Array(boardWidth.value).fill(false)
    );
    boardClicks.value = Array.from({ length: boardHeight.value }, () =>
      Array(boardWidth.value).fill(false)
    );
    boardDisplay.value = Array.from({ length: boardHeight.value }, () =>
      Array(boardWidth.value).fill("")
    );
    boardClicked.value = false;
    gameOver.value = false;

    console.log("Empty board created:");
    printBoard(board.value!);
  }

  function updateBoardWithMines(boardWithMines: boolean[][]) {
    board.value = boardWithMines;
  }

  function handleCellClick(x: number, y: number) {
    console.log(`Cell clicked at (${x}, ${y})`);

    if (!board.value || !boardClicks.value || boardClicks.value[x][y] || gameOver.value) return;

    if (!boardClicked.value) {
      console.log("Placing mines!");
      firstClickRow.value = x;
      firstClickCol.value = y;
      boardClicked.value = true;
      placeMines();
      startTimer();
      return;
    }

    revealSquare(x, y);
    updateBoardDisplay();
    
    if (!gameOver.value) {
      checkWinCondition();
    }
  }

  function handleCellFlag(x: number, y: number) {
    console.log(`Cell flagged at (${x}, ${y})`);

    if (!board.value || !boardClicks.value || boardClicks.value[x][y] || gameOver.value) return;

    if (boardDisplay.value![x][y] === "🚩") {
      boardDisplay.value![x][y] = "";
    } else {
      boardDisplay.value![x][y] = "🚩";
    }
  }

  function revealAllMines() {
    if (board.value && boardDisplay.value) {
      for (let i = 0; i < boardHeight.value; i++) {
        for (let j = 0; j < boardWidth.value; j++) {
          if (board.value[i][j] === true) {
            boardDisplay.value[i][j] = "💣";
          }
        }
      }
    }
  }

  function checkWinCondition() {
    if (!board.value || !boardClicks.value) return false;

    for (let i = 0; i < boardHeight.value; i++) {
      for (let j = 0; j < boardWidth.value; j++) {
        if (board.value[i][j] === false && !boardClicks.value[i][j]) {
          return false;
        }
      }
    }
    
    gameOver.value = true;
    stopTimer();
    alert("Congratulations! You won!");
    revealAllMines();
    return true;
  }

  function updateBoardDisplay() {
    if (board.value && boardClicks.value && boardDisplay.value) {
      console.log("Current board state:");
      printBoard(board.value);

      for (let i = 0; i < boardHeight.value; i++) {
        for (let j = 0; j < boardWidth.value; j++) {
          if (boardClicks.value[i][j]) {
            if (board.value[i][j] === true) {
              console.log(`Bomb found at (${i}, ${j})`);
              boardDisplay.value[i][j] = "💣";
            } else {
              const mineCount = countAdjacentMines(i, j);
              boardDisplay.value[i][j] =
                mineCount > 0 ? mineCount.toString() : "0";
            }
          } 
        }
      }

      printBoard(board.value);
    }
  }

  function countAdjacentMines(x: number, y: number): number {
    if (!board.value) return 0;

    const directions = [
      [-1, -1], [-1, 0], [-1, 1],
      [0, -1],          [0, 1],
      [1, -1], [1, 0], [1, 1]
    ];

    let mineCount = 0;

    for (const [dx, dy] of directions) {
      const newX = x + dx;
      const newY = y + dy;
      if (
        newX >= 0 &&
        newX < boardHeight.value &&
        newY >= 0 &&
        newY < boardWidth.value
      ) {
        if (board.value[newX][newY] === true) {
          mineCount++;
        }
      }
    }

    return mineCount;
  }

  function revealAdjacentSquares(x: number, y: number) {
    const directions = [
      [-1, -1], [-1, 0], [-1, 1],
      [0, -1],          [0, 1],
      [1, -1], [1, 0], [1, 1]
    ];

    for (const [dx, dy] of directions) {
      const newX = x + dx;
      const newY = y + dy;
      if (
        newX >= 0 &&
        newX < boardHeight.value &&
        newY >= 0 &&
        newY < boardWidth.value &&
        !boardClicks.value![newX][newY]
      ) {
        revealSquare(newX, newY);
      }
    }
  }

  function revealSquare(x: number, y: number) {
    if (!board.value || !boardClicks.value || !boardDisplay.value || boardClicks.value[x][y]) return;

    boardClicks.value[x][y] = true;

    if (board.value[x][y] === true) {
      console.log(`Bomb found at (${x}, ${y})`);
      boardDisplay.value[x][y] = "💣";
      gameOver.value = true;
      stopTimer();
      alert("Game Over! You hit a mine.");
      revealAllMines();
    } else {
      const mineCount = countAdjacentMines(x, y);
      boardDisplay.value[x][y] = mineCount > 0 ? mineCount.toString() : "0";

      if (mineCount === 0) {
        revealAdjacentSquares(x, y);
      }
    }
  }

  function resetGame() {
    initializeBoard();
    updateBoardDisplay();
    stopTimer();
    elapsedTime.value = 0;
  }

  return {
    boardWidth,
    boardHeight,
    numMines,
    board,
    boardDisplay,
    elapsedTime,
    gameOver,
    initializeBoard,
    handleCellClick,
    handleCellFlag,
    resetGame,
    formatTimer,
  };
}