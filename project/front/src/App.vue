<template>
  <v-app id="header">
    
    <v-navigation-drawer
      class="teal darken-1"
      dark
      permanent
      fixed
      app
      width="200px"
    >
      <v-list >
        <v-spacer></v-spacer>
        <v-list-item-content v-if="isLogin" class="text-center ma-5">
          <v-icon large>{{ 'mdi-account' }}</v-icon>
          <h3>{{userInfo.id}}</h3>
          <h4>{{userInfo.name}}</h4>
        </v-list-item-content>
        <v-list-item-content v-else class="text-center mt-3">
          <h3>로그인을 해주세요</h3>
        </v-list-item-content>

        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title @click="$router.push({name: item.name}).catch(err => {})" >{{ item.title }}</v-list-item-title>
            <!-- 똑같은 주소로 이동하는 거에 에러뜨는 거 신경 안 쓸라면 .catch(err => {}) 추가 -->
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-2">
          <v-btn block class="grey darken-4" v-if="isLogin===false" router :to="{name: 'login'}">
            Login
          </v-btn>
          <v-btn block class="grey darken-4" v-else @click="$store.dispatch('logout')">
            Logout
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- Sizes your content based upon application components -->

    <!-- Provides the application the proper gutter -->
    <v-content>

      <!-- If using vue-router -->
      <router-view :key="$route.fullPath"></router-view>
    </v-content>

    <v-fab-transition>
    <v-btn
      bottom
      right
      fixed
      fab
      dark
      small
      @click="$vuetify.goTo('#header')"
    >
      <v-icon>mdi-arrow-up-bold</v-icon>
    </v-btn>
</v-fab-transition>


      <v-footer >
    <v-col
      class="text-center"
      cols="12"
    >
      {{ new Date().getFullYear() }} — <strong>Vue.js Order Site</strong>
    </v-col>
  </v-footer>
</v-app>
</template>

<script>
import {mapState} from "vuex"

export default {
  name: "App",

  components: {
  },

  data: () => ({
        items: [
          { title: 'Home', icon: 'mdi-home', name: 'home' },
          { title: 'My Page', icon: 'mdi-archive', name: 'my_page'},
          { title: 'Order', icon: 'mdi-cart', name: 'order' },
        ],
  }),
  computed:{
    ...mapState(['isLogin','userInfo'])
  }
};
</script>
