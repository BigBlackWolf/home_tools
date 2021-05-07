import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import Login from "../components/Login";
import Dishes from "../components/Dishes";
import Register from "../components/Register";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/dishes',
      name: 'Dishes',
      component: Dishes
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/logout',
      name: 'Logout',
      redirect: Login
    },
  ],
  mode: "history"
})
