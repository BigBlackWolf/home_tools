<template>
  <div id="app">
    <div>
      <b-nav tabs align="center">
        <b-nav-item>
          <router-link to="/">Home</router-link>
        </b-nav-item>
        <b-nav-item to="/dishes">
          <router-link to="/dishes">Dishes</router-link>
        </b-nav-item>
        <b-nav-item v-show="$store.getters.getToken === ''">
          <router-link to="/login">Login</router-link>
        </b-nav-item>
        <b-nav-item v-show="$store.getters.getToken === ''">
          <router-link to="/register">Register</router-link>
        </b-nav-item>
        <b-nav-item to="/login" v-show="$store.getters.getToken !== ''" @click="logout">
          <router-link to="/logout">Logout</router-link>
        </b-nav-item>
      </b-nav>
    </div>
    <router-view/>
  </div>
</template>

<script>

export default {
  name: 'App',
  methods: {
    async logout() {
      await this.$store.dispatch('logout')
    }
  }
}
</script>

