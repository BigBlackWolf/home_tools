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
        label="Username:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          v-model="form.username"
          type="text"
          placeholder="Enter username"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-3"
        label="Password:"
        label-for="input-3"
      >
        <b-form-input
          id="input-3"
          v-model="form.password"
          type="password"
          placeholder="Enter password"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-4"
        label="Repeat password:"
        label-for="input-4"
      >
        <b-form-input
          id="input-4"
          v-model="form.password2"
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
  name: "Register",
  data() {
    return {
      form: {
        email: '',
        username: '',
        password: '',
        password2: '',
      },
      show: true
    }
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault()
      let data = {
        email: this.form.email,
        username: this.form.username,
        password: this.form.password,
        password2: this.form.password2,
      }

      const resp = await fetch(
        'http://localhost:8000/register/',
        {
          method: 'post',
          headers: new Headers({
            'Content-Type': 'application/json',
          }),
          body: JSON.stringify(data),
        }
      )

      if (resp.status === 200){
          await router.push("login")
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
