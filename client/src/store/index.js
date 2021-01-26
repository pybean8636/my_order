import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    allUsers:[
      {id:'pybean', pw:112233, name:'박유빈'}
    ],
    isLogin: false,
    isLoginError:false,
    userInfo:null
  },
  mutations: {
    //login success
    loginSucceess(state, payload){
      state.isLogin = true
      state.isLoginError= false
      state.userInfo =payload
    },
    //login fail
    loginError(state){
      state.isLogin = false
      state.isLoginError= true
    }
  },//change state
  actions: {
    //tryng login  success->loginSuccess commit, fail->loginError commit
    login({state, commit}, loginOb){
        let selectedUser=null
        state.allUsers.forEach(user => {
            if(user.id === loginOb. id) selectedUser=user    
        });
        selectedUser===null ? commit('loginError') :
            selectedUser.pw != loginOb.pw ? commit('loginError') : commit('loginSucceess',selectedUser)
    
    }

  },//
  modules: {}
});
