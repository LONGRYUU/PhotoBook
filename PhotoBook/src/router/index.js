import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login'
import Register from '../components/Register'
import Home from '../components/Home'
import Classify from "../components/Classify";
import Search from "../components/Search";
import Generate from "../components/Generate";
import Upload from "../components/Upload"
import PhotoWall from "../components/PhotoWall"
import Info from "../components/Info"

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      redirect:'/login'
    },
    {
      path: '/login',
      name:'Login',
      component: Login
    },
    {
      path:'/register',
      name:'Register',
      component:Register
    },
    {
      path:'/home',
      name:'Home',
      component:Home,
      children:[
        {
          path:'classify',
          name:'classify',
          component:Classify
        },
        {
          path:'search',
          name:'search',
          component:Search,
        },
        {
          path:'generate',
          name:'generate',
          component:Generate
        },
        {
          path:'upload',
          name:'upload',
          component:Upload
        },
        {
          path:'photoWall',
          name:'photoWall',
          component:PhotoWall,
        },
        {
          path:'info',
          name:'name',
          component:Info
        }
      ]
    }
  ]
})
