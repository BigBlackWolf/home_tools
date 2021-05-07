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

const store = new Vuex.Store({
  getters: {
    allDishes(state) {
      return state.dishes
    },
    getToken(state) {
      return localStorage.getItem("token")
    }
  },
  state: {
    dishes: [],
  },
  mutations: {
    setToken(state, token) {
      localStorage.setItem("token", token)
    },
    updateDishes(state, dishes) {
      state.dishes = dishes
    },
  },
  actions: {
    async checkToken({getters, commit}) {
      await fetch(
        'http://localhost:8000/token/verify/',
        {
          method: 'post',
          body: JSON.stringify({token: getters.getToken}),
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

    async refreshToken({commit}) {
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
            commit('setToken', token.access)
          }
        })
        .catch(resp => {
          commit('setToken', '')
          alert("Please login")
          router.push("login")
        })
    },

    async fetchDishes({commit, getters, dispatch}) {
      await dispatch('checkToken')
      if (getters.getToken === '') {
        await dispatch('refreshToken')
      }

      const resp = await fetch(
        'http://localhost:8000/dishes/',
        {
          method: 'get',
          headers: new Headers({
            'Authorization': 'Bearer ' + getters.getToken
          }),
        }
      )
      const dishes = await resp.json()
      commit('updateDishes', dishes.data)
    },

    async logout({commit, getters}) {
      await fetch(
        'http://localhost:8000/logout/',
        {
          method: 'post',
          credentials: 'include',
          headers: new Headers({
            'Authorization': 'Bearer ' + getters.getToken
          }),
          body: {},
        }
      ).then(
        commit('setToken', '')
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
