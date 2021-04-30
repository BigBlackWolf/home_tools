<template>
  <div id="app">
    <div>
      <b-nav tabs align="center">
        <b-nav-item active>
          <router-link to="/">Home</router-link>
        </b-nav-item>
        <b-nav-item>
          <router-link to="/login">Login</router-link>
        </b-nav-item>
        <b-nav-item>Link with a long name</b-nav-item>
        <b-nav-item disabled>Disabled</b-nav-item>
      </b-nav>
    </div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

