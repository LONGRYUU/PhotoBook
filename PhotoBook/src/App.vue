<template>
  <div id="app" style="overflow-y: hidden;">
    <router-view></router-view>
  </div>
</template>

<script>

import Login from "./components/Login"
import Register from "./components/Register"
import Home from "./components/Home"
export default {
  name: 'App',
  components:{
    Login,
    Register,
    Home
  },
  data () {
    return {
    }
  },
  methods:{

  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0;
}
</style>
