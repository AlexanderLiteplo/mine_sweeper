<template>
  <div id="app">
    <h1>Minesweeper</h1>
    <div class="timer">Time: {{ formatTimer(elapsedTime) }}</div>
    <div class="controls">
      <div class="control-item">
        <label for="boardWidth">Board Width:</label>
        <input type="number" v-model="boardWidth" id="boardWidth" />
      </div>
      <div class="control-item">
        <label for="boardHeight">Board Height:</label>
        <input type="number" v-model="boardHeight" id="boardHeight" />
      </div>
      <div class="control-item">
        <label for="numMines">Number of Mines:</label>
        <input type="number" v-model="numMines" id="numMines" />
      </div>
    </div>
  <div>
    <button @click="initializeBoard">Initialize Board</button>
    <button @click="resetGame">Reset Game</button>
  </div>
    <div class="board" v-if="board">
      <div v-for="(row, rowIndex) in board" :key="rowIndex" class="row">
        <CellComponent
          v-for="(cell, cellIndex) in row"
          :key="cellIndex"
          :value="boardDisplay[rowIndex][cellIndex]"
          :x="rowIndex"
          :y="cellIndex"
          @cell-click="handleCellClick"
          @cell-flag="handleCellFlag"
        />
      </div>
    </div>
  </div>
</template>


<style>
:root {
  --primary-color: #3498db;
  --secondary-color: #2c3e50;
  --accent-color: #e74c3c;
  --background-color: #f0f3f5;
  --text-color: #34495e;
}

body {
  background-color: #1E1E1E;
  color: #FFFFFF;
  font-family: 'Rajdhani', sans-serif;
}

#app {
  font-family: 'Roboto', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: var(--text-color);
  max-width: 800px;
  margin: 0 auto;
  padding: 3rem;
}

h1 {
  color: #00FFFF;
  font-size: 3rem;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  letter-spacing: 3px;
}

.timer {
  font-family: 'Digital-7', monospace;
  font-size: 2rem;
  color: #00FF00;
  margin-bottom: 3rem;
}

input[type="number"] {
  background-color: rgba(0, 191, 255, 0.1);
  border: 1px solid #00BFFF;
  color: #FFFFFF;
  padding: 0.5rem;
  border-radius: 5px;
}

.controls {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 2rem; /* Space before the buttons */
}

.control-item {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem; /* Space between each control item */
  width: 100%;
}

.control-item label {
  font-size: 1.5rem; /* Larger label text */
  width: 200px; /* Fixed width for labels to align inputs */
  text-align: right;
  margin-right: 1rem;
}

input[type="number"] {
  font-size: 1.5rem; /* Larger input text */
  padding: 0.75rem;
  width: 100px; /* Fixed width for inputs */
}

button {
  background-color: #00BFFF;
  color: #FFFFFF;
  border: none;
  padding: 1rem 2rem;
  margin-right: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #2980b9;
}

.board {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 3rem;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 191, 255, 0.3);
}

.row {
  display: flex;
}

/* Add this if you want to style the CellComponent */
.cell {
  width: 40px;
  height: 40px;
  background: linear-gradient(145deg, #2a2a2a, #232323);
  border: 1px solid #333;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cell:hover {
  transform: scale(1.05);
  box-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
}
</style>

<script lang="ts">
import { defineComponent } from "vue";
import { initializeBoard, placeMines } from "./api";
import CellComponent from "./components/CellComponent.vue";

export default defineComponent({
  name: "App",
  components: {
    CellComponent,
  },
  data() {
    return {
      boardWidth: 5,
      boardHeight: 5,
      numMines: 4,
      firstClickRow: 0,
      firstClickCol: 0,
      board: null as boolean[][] | null, // represents mine locations, true = mine
      boardClicks: null as boolean[][] | null, // represents clicked cells
      boardDisplay: null as string[][] | null, // represents cell display values
      boardClicked: false,
      gameOver: false,
      gameTimer: 0 as number | null,
      elapsedTime: 0 as number,
    };
  },
  methods: {
    startTimer() {
      this.elapsedTime = 0;
      this.gameTimer = setInterval(() => {
        this.elapsedTime++;
      }, 1000);
    },
    stopTimer() {
      if (this.gameTimer) {
        clearInterval(this.gameTimer);
        this.gameTimer = null;
      }
    },
    formatTimer(seconds: number): string {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    },
    async initializeBoard() {
      try {
        const response = await initializeBoard(
          this.boardWidth,
          this.boardHeight,
          this.numMines
        );
        console.log(response.data);
        this.createEmptyBoard();
        this.stopTimer();
        this.elapsedTime = 0;
      } catch (error) {
        console.error(error);
      }
    },
    async placeMines() {
      try {
        const response = await placeMines([
          this.firstClickRow,
          this.firstClickCol,
        ]);
        console.log("Received board from server:");
        this.printBoard(response.data.board);
        this.updateBoardWithMines(response.data.board);
        this.revealSquare(this.firstClickRow, this.firstClickCol);
        this.updateBoardDisplay();
        this.$forceUpdate();
      } catch (error) {
        console.error(error);
      }
    },
    printBoard(board: boolean[][]) {
      console.log("Current display state:");

      let output = "";
      for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[i].length; j++) {
          output += board[i][j] ? "X " : "O ";
        }
        output += "\n";
      }
      console.log(output);
    },
    createEmptyBoard() {
      this.board = Array.from({ length: this.boardHeight }, () =>
        Array(this.boardWidth).fill(false)
      );
      this.boardClicks = Array.from({ length: this.boardHeight }, () =>
        Array(this.boardWidth).fill(false)
      );
      this.boardDisplay = Array.from({ length: this.boardHeight }, () =>
        Array(this.boardWidth).fill("")
      );
      this.boardClicked = false;
      this.gameOver = false;

      console.log("Empty board created:");
      this.printBoard(this.board);
    },
    updateBoardWithMines(boardWithMines: boolean[][]) {
      this.board = boardWithMines;
    },
    handleCellClick(x: number, y: number) {
      console.log(`Cell clicked at (${x}, ${y})`);

      if (!this.board || !this.boardClicks || this.boardClicks[x][y] || this.gameOver) return;

      if (!this.boardClicked) {
        console.log("Placing mines!");
        this.firstClickRow = x;
        this.firstClickCol = y;
        this.boardClicked = true;
        this.placeMines();
        this.startTimer();
        return;
      }

      this.revealSquare(x, y);
      this.updateBoardDisplay();
      
      if (!this.gameOver) {
        this.checkWinCondition();
      }
      
      this.$forceUpdate();
    },
    handleCellFlag(x: number, y: number) {
      console.log(`Cell flagged at (${x}, ${y})`);

      if (!this.board || !this.boardClicks || this.boardClicks[x][y] || this.gameOver) return;

      if (this.boardDisplay![x][y] === "🚩") {
        this.boardDisplay![x][y] = "";
      } else {
        this.boardDisplay![x][y] = "🚩";
      }

      this.$forceUpdate();
    },
    revealAllMines() {
      if (this.board && this.boardDisplay) {
        for (let i = 0; i < this.boardHeight; i++) {
          for (let j = 0; j < this.boardWidth; j++) {
            if (this.board[i][j] === true) {
              this.boardDisplay[i][j] = "💣";
            }
          }
        }
      }
      this.$forceUpdate();
    },
    checkWinCondition() {
      if (!this.board || !this.boardClicks) return false;

      for (let i = 0; i < this.boardHeight; i++) {
        for (let j = 0; j < this.boardWidth; j++) {
          if (this.board[i][j] === false && !this.boardClicks[i][j]) {
            return false;
          }
        }
      }
      
      this.gameOver = true;
      this.stopTimer();
      alert("Congratulations! You won!");
      this.revealAllMines();
      return true;
    },
    updateBoardDisplay() {
      if (this.board && this.boardClicks && this.boardDisplay) {
        console.log("Current board state:");
        this.printBoard(this.board);

        for (let i = 0; i < this.boardHeight; i++) {
          for (let j = 0; j < this.boardWidth; j++) {
            if (this.boardClicks[i][j]) {
              if (this.board[i][j] === true) {
                console.log(`Bomb found at (${i}, ${j})`);
                this.boardDisplay[i][j] = "💣";
              } else {
                const mineCount = this.countAdjacentMines(i, j);
                this.boardDisplay[i][j] =
                  mineCount > 0 ? mineCount.toString() : "0";
              }
            } 
          }
        }

        this.printBoard(this.board);
      }
    },
    countAdjacentMines(x: number, y: number): number {
      if (!this.board) return 0;

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
          newX < this.boardHeight &&
          newY >= 0 &&
          newY < this.boardWidth
        ) {
          if (this.board[newX][newY] === true) {
            mineCount++;
          }
        }
      }

      return mineCount;
    },
    revealAdjacentSquares(x: number, y: number) {
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
          newX < this.boardHeight &&
          newY >= 0 &&
          newY < this.boardWidth &&
          !this.boardClicks![newX][newY]
        ) {
          this.revealSquare(newX, newY);
        }
      }
    },
    revealSquare(x: number, y: number) {
      if (!this.board || !this.boardClicks || !this.boardDisplay || this.boardClicks[x][y]) return;

      this.boardClicks[x][y] = true;

      if (this.board[x][y] === true) {
        console.log(`Bomb found at (${x}, ${y})`);
        this.boardDisplay[x][y] = "💣";
        this.gameOver = true;
        this.stopTimer();
        alert("Game Over! You hit a mine.");
        this.revealAllMines();
      } else {
        const mineCount = this.countAdjacentMines(x, y);
        this.boardDisplay[x][y] = mineCount > 0 ? mineCount.toString() : "0";

        if (mineCount === 0) {
          this.revealAdjacentSquares(x, y);
        }
      }
    },
    resetGame() {
      this.initializeBoard();
      this.updateBoardDisplay();
      this.stopTimer();
      this.elapsedTime = 0;
      this.$forceUpdate();
    },
  },
});
</script>

