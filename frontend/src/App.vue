<template>
  <div id="app">
    <div class="bg-warning">
      <b-container>
        <b-navbar class="pl-0" type="light">
          <b-navbar-nav class="h6">
            <b-nav-item to="/">
              Home
            </b-nav-item>
            <b-nav-item to="/dishes">
              Dishes
            </b-nav-item>
            <b-nav-item to="/products">
              Products
            </b-nav-item>
          </b-navbar-nav>
          <b-nav-form>
              <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
            </b-nav-form>
          <b-navbar-nav class="ml-auto" :key="loggedIn">
            <b-nav-item v-show="loggedIn === false" to="/login">
              Login
            </b-nav-item>
            <b-nav-item v-show="loggedIn === false" to="/register">
              Register
            </b-nav-item>
            <b-nav-item to="/logout" v-show="loggedIn === true" @click="logout">
              Logout
            </b-nav-item>
          </b-navbar-nav>
        </b-navbar>
      </b-container>
    </div>
    <div>
      <router-view/>
    </div>
  </div>
</template>

<script>

export default {
  name: 'App',
  methods: {
    async logout() {
      await this.$store.dispatch('logout');
      this.loggedIn = false;
    }
  },
  data() {
    return {
      loggedIn: this.$store.getters.getToken !== ""
    }
  },
  mounted() {
    this.$root.$on('login', () => {
      this.loggedIn = this.$store.getters.getToken !== "";
    });
  }

}
</script>

