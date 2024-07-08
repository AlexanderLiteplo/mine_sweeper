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

<script lang="ts">
import { defineComponent } from "vue";
import { initializeBoard, placeMines } from "./api";
import CellComponent from "./components/CellComponent.vue";
import { useMinesweeper } from './composables/useMineSweeper';
import './assets/styles/main.css';

export default defineComponent({
  name: "App",
  components: {
    CellComponent,
  },
  setup() {
    const minesweeper = useMinesweeper();
    return { ...minesweeper };
  }
});
</script>

