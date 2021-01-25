<template>
  <v-app>
    <v-navigation-drawer
      class="deep-purple accent-4"
      dark
      permanent
      fixed
      app
    >
      <v-list >
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title router :to="{name: item.name}">{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-2">
          <v-btn block>
            Logout
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- Sizes your content based upon application components -->

    <!-- Provides the application the proper gutter -->
    <v-content>

      <!-- If using vue-router -->
      <router-view></router-view>
    </v-content>

    <v-footer app>
      <!-- -->
    </v-footer>
</v-app>
</template>

<script>
export default {
  name: "App",

  components: {
  },

  data: () => ({
        items: [
          { title: 'Home', icon: 'mdi-view-dashboard', name: 'home' },
          { title: 'My Page', icon: 'mdi-account-box', name: 'my_page'},
          { title: 'Order', icon: 'mdi-gavel', name: 'order' },
        ],
  })
};
</script>
