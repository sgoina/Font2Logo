import { defineStore } from 'pinia'

export const useSubmitStore = defineStore('submit', {
  state: () => ({
    isSubmitted: false
  }),
  actions: {
    setSubmitted(value: boolean) {
      this.isSubmitted = value
    }
  }
})
export const useFontStore = defineStore('font', {
  state: () => ({
    fontChanged: false,
    a: false,
    b: false
  }),
  actions: {
    setChanged(value: boolean) {
      this.fontChanged = value
      this.a = false
      this.b = false
    }
  }
})
