// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'
import ElementUI from 'element-ui'
import axios from 'axios'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(VueResource);
Vue.use(ElementUI);
Vue.config.productionTip = false;
Vue.prototype.$axios = axios;
Vue.prototype.$bus = new Vue();
axios.defaults.baseURL = 'http://localhost:8080/server';
axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';
/* eslint-disable no-new */

new Vue({
  el: '#app',
  router,
  VueResource,
  ElementUI,
  components: { App },
  template: '<App/>'
});
