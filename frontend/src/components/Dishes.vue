<template>
  <b-container>
    <ul id="dishes">
      <li v-for="dish in allDishes">
        {{ dish.name }}
      </li>
    </ul>
  </b-container>
</template>

<script>
import { mapGetters } from "vuex"

export default {
  name: "Dishes",
  computed: mapGetters(["allDishes"]),
  async mounted() {
    await this.$store.dispatch('fetchDishes');
  }
}
</script>

<style scoped>

</style>
