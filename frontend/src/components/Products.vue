<template>
  <b-container class="mt-4">
    <b-card-group deck v-for="(row, index) in getProducts" :key="index">
      <b-card v-for="product in row"
              img-alt="Card image"
              img-top
              img-src="https://picsum.photos/400/400/?image=20"
              class="mb-3"
              :title="product.name"
              style="max-width: 10rem;"
              :key="product.name"
      >
          <b-card-text style="max-width: 270px; display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical;
overflow: hidden;">
            {{ product.name }}
          </b-card-text>
      </b-card>
    </b-card-group>
  </b-container>
</template>

<script>

export default {
  name: "Products",
  computed: {
    getProducts() {
      let products = this.$store.getters.allProducts;
      let result = [];
      let tmp = [];
      for (let product of products) {
        tmp.push(product)
        if (tmp.length === 8) {
          result.push(tmp)
          tmp = []
        }
      }
      result.push(tmp)
      return result
    }
  },
  async mounted() {
    await this.$store.dispatch('fetchProducts');
  }
}
</script>

<style scoped>

</style>
