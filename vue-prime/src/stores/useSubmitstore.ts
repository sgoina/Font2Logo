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
