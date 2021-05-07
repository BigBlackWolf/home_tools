<template>
  <b-container>
    <b-form @submit="onSubmit" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Email address:"
        label-for="input-1"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          placeholder="Enter email"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        label="Password:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          v-model="form.password"
          type="password"
          placeholder="Enter password"
          required
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
    <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card>
  </b-container>
</template>

<script>
import router from "../router";

export default {
  name: "Login",
  data() {
    return {
      form: {
        email: 'user@user.com',
        password: 'user',
      },
      show: true
    }
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault()
      let data = {
        email: this.form.email,
        password: this.form.password
      }

      const resp = await fetch(
        'http://localhost:8000/login/',
        {
          method: 'post',
          headers: new Headers({
            'Content-Type': 'application/json',
          }),
          credentials: "include",
          body: JSON.stringify(data),
        }
      )

      if (resp.status === 200){
          const response = await resp.json()
          await this.$store.commit('setToken', response.access)
          await router.push("dishes")
        }
        else {
          let data = await resp.json()
          console.log(data.errors)
      }
    }
  }
}

</script>

<style scoped>

</style>
