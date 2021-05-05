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
import axios from 'axios';

export default {
  name: "Login",
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      show: true
    }
  },
  methods: {
    onSubmit(event) {
      event.preventDefault()
      let data = {
        email: this.form.email,
        password: this.form.password
      }
      axios.post(
        "http://localhost:8000/login/",
        data
      ).then(response => {
        console.log(response.data.access)
        axios.get("http://localhost:8000/dishes/", {headers: {Authorization: 'Bearer ' + response.data.access}})
          .then(
          response2 => {
            console.log(response)
          }
        )
      })
    }
  }
}

</script>

<style scoped>

</style>
