<template>
<div class="ma-2">
  <!-- 매장정보 -->
  <v-card
    max-width="900"
    flat
    class="ma-8"
  >
    <v-card-text>
      <h3>{{storeInfo.headquarters}}</h3>
      <p class="display-1 text--primary">
        {{storeInfo.location}}점
      </p>
      <div class="text--primary">
      <v-icon class="mr-3">{{ 'mdi-phone' }}</v-icon>
        {{storeInfo.contact}}
      </div>
    </v-card-text>

  <v-divider></v-divider>
  
  </v-card>

    <!-- 해당 사용자의 최근 발주 내역 -->
  <v-card
    elevation="2"
    height="300px" 
    width="900px"
    class="ma-8"
  >
    <v-toolbar
    :color="'grey darken-4'"
    dark
    >

      <v-toolbar-title>
        Latest Order
      </v-toolbar-title>

      <v-spacer></v-spacer>

    </v-toolbar>



  <v-simple-table width="200px" class="ma-5">

    <thead>
      <tr>
        <th class="text-left">
          Name
        </th>
        <th class="text-left">
          Qty
        </th>
        <th class="text-left">
          Unit
        </th>
        <th class="text-left">
          Total Price
        </th>
      </tr>
    </thead>

    <tbody>
      <tr>
        <td>item</td>
        <td>qty</td>
        <td>box</td>
        <td>price</td>
      </tr>
    </tbody>

  </v-simple-table>

    <v-btn
      large
      dark
      absolute
      bottom
      right
      class="v-btn--example grey darken-3"
      @click="$router.push({name: 'check'})"
    >
      <v-icon>mdi-cart-arrow-down</v-icon>
    </v-btn>

</v-card>



</div>
</template>

<script>
import {mapState , mapActions} from "vuex"  //
// @ is an alias to /src

export default {
  name: "home",
  components: {
  },
  computed:{
      ...mapState(['storeInfo'])
  },
  methods:{
      ...mapActions(['getStoreInfo']),
  }
};
</script>
