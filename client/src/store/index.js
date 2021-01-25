import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    allUsers:[
      {id:'pybean', pw:112233, name:'박유빈'}
    ],
    isLogin: false,
    isLoginError:false
  },
  mutations: {
    //login success
    loginSucceess(state){
      state.isLogin = true
      state.isLoginError= false
    },
    //login fail
    loginError(state){
      state.isLogin = false
      state.isLoginError= true
    }
  },//change state
  actions: {
    //tryng login  success->loginSuccess commit, fail->loginError commit
    login({state, commit}, signinOb){
      commit('')
    }

  },//
  modules: {}
});
