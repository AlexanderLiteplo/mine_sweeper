<template>
    <div class="cell" @click="handleClick">
      {{ displayValue }}
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, PropType } from 'vue';
  
  export default defineComponent({
    name: 'CellComponent',
    props: {
        value: {
            type: [Boolean, String] as PropType<boolean | string>,
            default: null,
        },
      x: {
        type: Number as PropType<number>,
        required: true,
      },
      y: {
        type: Number as PropType<number>,
        required: true,
      },
    },
    computed: {
        displayValue() {
            console.log('displayValue');
            console.log(this.value);
            // if (this.value === true) return '💣';
            // if (this.value === false) return '';
            if (this.value === true) return '';
            return this.value;
        },
    },
    methods: {
      handleClick() {
        this.$emit('cell-click', this.x, this.y);
      },
    },
  });
  </script>
  
  <style scoped>
  .cell {
    width: 30px;
    height: 30px;
    border: 1px solid #000;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  </style>
  