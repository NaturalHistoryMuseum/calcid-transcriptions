import Vue from 'vue'
import App from './App.vue'
import VueResource from 'vue-resource'

Vue.config.productionTip = false

Vue.use(VueResource)

// Set up config
const vueConfig = require('vue-config');
Vue.use(vueConfig, require('./config.js'));

// Set up fontawesome
import 'vue-awesome/icons';

import Icon from 'vue-awesome/components/Icon'

// globally (in your main .js file)
Vue.component('icon', Icon)


new Vue({
  render: h => h(App)
}).$mount('#app')
