<template>
  <div id="app">
    <h1>Minesweeper Client</h1>
    <div>
      <label for="boardWidth">Board Width:</label>
      <input type="number" v-model="boardWidth" id="boardWidth" />
    </div>
    <div>
      <label for="boardHeight">Board Height:</label>
      <input type="number" v-model="boardHeight" id="boardHeight" />
    </div>
    <div>
      <label for="numMines">Number of Mines:</label>
      <input type="number" v-model="numMines" id="numMines" />
    </div>
    <button @click="initializeBoard">Initialize Board</button>
    <button @click="resetGame">Reset Game</button>
    <div class="board" v-if="board">
      <div v-for="(row, rowIndex) in board" :key="rowIndex" class="row">
        <CellComponent
          v-for="(cell, cellIndex) in row"
          :key="cellIndex"
          :value="boardDisplay[rowIndex][cellIndex]"
          :x="rowIndex"
          :y="cellIndex"
          @cell-click="handleCellClick"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { initializeBoard, placeMines } from './api';
import CellComponent from './components/CellComponent.vue';

export default defineComponent({
  name: 'App',
  components: {
    CellComponent,
  },
  data() {
    return {
      boardWidth: 10,
      boardHeight: 10,
      numMines: 10,
      firstClickRow: 0,
      firstClickCol: 0,
      board: null as boolean[][] | null, // represents mine locations, true = mine
      boardClicks: null as boolean[][] | null, // represents clicked cells
      boardDisplay: null as string[][] | null, // represents cell display values
      boardClicked: false,
    };
  },
  methods: {
    async initializeBoard() {
      try {
        const response = await initializeBoard(this.boardWidth, this.boardHeight, this.numMines);
        console.log(response.data);
        this.createEmptyBoard();
      } catch (error) {
        console.error(error);
      }
    },
    async placeMines() {
      try {
        const response = await placeMines([this.firstClickRow, this.firstClickCol]);
        console.log(response.data);
        this.updateBoardWithMines(response.data.board);
      } catch (error) {
        console.error(error);
      }
    },
    createEmptyBoard() {
      this.board = Array.from({ length: this.boardHeight }, () =>
        Array(this.boardWidth).fill(false)
      );
      this.boardClicks = Array.from({ length: this.boardHeight }, () =>
        Array(this.boardWidth).fill(false)
      );
      this.boardDisplay = Array.from({ length: this.boardHeight }, () =>
        Array(this.boardWidth).fill('')
      );
      this.boardClicked = false;
    },
    updateBoardWithMines(boardWithMines: boolean[][]) {
      this.board = boardWithMines;
    },
    handleCellClick(x: number, y: number) {
      console.log(`Cell clicked at (${x}, ${y})`);
      console.log(this.board);
      
      // Don't do anything if the cell is already clicked
      // if (!this.board || !this.boardClicks || this.boardClicks[x][y]) return; 
      
      // if no cells have been clicked yet, place mines
      if (!this.boardClicked) {
        console.log('Placing mines!')
        this.firstClickRow = x;
        this.firstClickCol = y;
        this.placeMines();
      }

      this.boardClicked = true;
      
      // Game over logic
      if (this.board && this.board[x][y] === true) {
        alert('Game Over! You hit a mine.');
        this.revealAllMines();
        return;
      }

      this.boardClicks![x][y] = true;
      this.updateBoardDisplay();
      this.checkWinCondition();
      this.$forceUpdate();
    },
    revealAllMines() {
      if (this.board && this.boardDisplay) {
        for (let i = 0; i < this.boardHeight; i++) {
          for (let j = 0; j < this.boardWidth; j++) {
            if (this.board[i][j] === true) {
              this.boardDisplay[i][j] = '💣';
            }
          }
        }
      }
      this.$forceUpdate();
    },
    checkWinCondition() {
      if (!this.board || !this.boardClicks) return false;

      if (this.board && this.boardClicks) {
        for (let i = 0; i < this.boardHeight; i++) {
          for (let j = 0; j < this.boardWidth; j++) {
            // If there is a cell that is not a mine and not clicked, return false
            if (this.board[i][j] === false && !this.boardClicks[i][j]) {
              return false;
            }
          }
        }
        alert('Congratulations! You won!');
        return true;
      }
      return false;
    },
    updateBoardDisplay() {
      if (this.board && this.boardClicks && this.boardDisplay) {
        for (let i = 0; i < this.boardHeight; i++) {
          for (let j = 0; j < this.boardWidth; j++) {
            if (this.boardClicks[i][j]) {
              if (this.board[i][j] === true) {
                // log this
                console.log(`updating board display with bomb emoji at (${i}, ${j})`);
                this.boardDisplay[i][j] = '💣'; // Display bomb emoji for mines
              } else {
                const mineCount = this.countAdjacentMines(i, j);
                this.boardDisplay[i][j] = mineCount > 0 ? mineCount.toString() : '';
              }
            } else {
              this.boardDisplay[i][j] = ''; // Keep it empty for unclicked cells
            }
          }
        }
      }
    },
    countAdjacentMines(x: number, y: number): number {
      const directions = [
        [-1, -1], [-1, 0], [-1, 1],
        [0, -1],          [0, 1],
        [1, -1], [1, 0], [1, 1]
      ];
      let mineCount = 0;
      for (const [dx, dy] of directions) {
        const newX = x + dx;
        const newY = y + dy;
        if (newX >= 0 && newX < this.boardHeight && newY >= 0 && newY < this.boardWidth) {
          if (this.board![newX][newY] === true) {
            mineCount++;
          }
        }
      }
      return mineCount;
    },
    resetGame() {
      this.createEmptyBoard();
      this.updateBoardDisplay();
      this.$forceUpdate();
    },
  },
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.board {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.row {
  display: flex;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
