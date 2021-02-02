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
        Latest Order <h4>{{this.date}}</h4>
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
          Price
        </th>
        <th class="text-left">
          Total Price
        </th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="item in order" :key=item.name>
        <td>{{item.name}}</td>
        <td>{{item.qty}}</td>
        <td>{{item.unit}}</td>
        <td>{{item.price}}</td>
        <td>{{item.total_price}}</td>
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
      @click="setItems"
    >
      <v-icon>mdi-cart-arrow-down</v-icon>
    </v-btn>

</v-card>



</div>
</template>

<script>
import axios from 'axios';
import store from "../store/index.js"
import {mapState , mapActions} from "vuex"  //
// @ is an alias to /src

export default {
  name: "home",
  components: {
  },
  data(){
    return {
      order:[],
      date:null
    }
  },
  computed:{
      ...mapState(['storeInfo'])
  },
  methods:{
      ...mapActions(['getStoreInfo']),
      getOrder() {
          const payload ={
              user_key_id:store.state.userInfo.user_key_id
          }
          const path = 'http://localhost:5000/api/order_info'
          axios.post(path, payload)
              .then((res) => {
                console.log("get order info")
                this.order = res.data.order_info
                this.date = res.data.date
              })
              .catch((error) => {
              console.error(error);
              });
      },
      setItems(){//store item
        store.state.items=this.order
        this.$router.push({name: 'check'})
      }
  },
  created(){
    this.getOrder()
  }
};
</script>
