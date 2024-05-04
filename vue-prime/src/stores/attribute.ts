import { defineStore } from 'pinia'
export const useNumbersStore = defineStore('numbers', {
  state: () => ({
    numbers: [] as number[]
  }),
  actions: {
    updateNumbers(numbers: number[]) {
      this.numbers = numbers
    }
  },
  getters: {
    getNumbers(): number[] {
      return this.numbers
    }
  }
})
