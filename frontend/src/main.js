import Vue from 'vue'
import App from './App'
import router from './router'
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
import Vuex from 'vuex'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(Vuex)

// TODO: add loggedIn flag
const getDefaultState = () => {
  return {
    dishes: [],
    products: []
  }
}

const store = new Vuex.Store({
  getters: {
    allDishes(state) {
      return state.dishes
    },
    allProducts(state) {
      return state.products
    }
  },
  state: getDefaultState(),
  mutations: {
    updateDishes(state, dishes) {
      state.dishes = dishes
    },
    updateProducts(state, products) {
      state.products = products
    },
    clearState(state) {
      let s = getDefaultState()
      Object.keys(s).forEach(key => {
        state[key] = s[key]
      })
    }
  },
  actions: {
    async checkToken() {
      await fetch(
        'http://localhost:8000/token/verify/',
        {
          method: 'post',
          body: JSON.stringify({token: localStorage.getItem("token")}),
          headers: new Headers({
            'Content-Type': 'application/json'
          })
        }
      )
        .then(async function (resp) {
          if (resp.status !== 200)
            localStorage.setItem("token", "")
        })
    },

    async refreshToken() {
      await fetch(
        'http://localhost:8000/token/refresh/',
        {
          method: 'post',
          body: {},
          credentials: "include"
        }
      )
        .then(async function (resp) {
          if (resp.status === 401) {
            throw Error("Forbidden " + resp.status)
          } else {
            const token = await resp.json()
            localStorage.setItem("token", token.access)
          }
        })
        .catch(resp => {
          localStorage.setItem("token", "")
          alert("Please login")
          router.push("login")
        })
    },

    async fetchDishes({commit, dispatch}) {
      await dispatch('checkToken')
      if (localStorage.getItem("token") === "") {
        await dispatch('refreshToken')
      }

      const resp = await fetch(
        'http://localhost:8000/dishes/',
        {
          method: 'get',
          headers: new Headers({
            'Authorization': 'Bearer ' + localStorage.getItem("token")
          }),
        }
      )
      const dishes = await resp.json()
      commit('updateDishes', dishes.data)
    },

    async fetchProducts({commit, dispatch}) {
      await dispatch('checkToken')
      if (localStorage.getItem("token") === '') {
        await dispatch('refreshToken')
      }

      const resp = await fetch(
        'http://localhost:8000/products/',
        {
          method: 'get',
          headers: new Headers({
            'Authorization': 'Bearer ' + localStorage.getItem("token")
          }),
        }
      )
      const products = await resp.json()
      commit('updateProducts', products.data)
    },

    async logout({commit}) {
      await fetch(
        'http://localhost:8000/logout/',
        {
          method: 'post',
          credentials: 'include',
          headers: new Headers({
            'Authorization': 'Bearer ' + localStorage.getItem("token")
          }),
          body: {},
        }
      ).then(function()  {
        commit('clearState')
        localStorage.setItem("token", "")
      }
      )
    }
  }
})


Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
})
