<template>
<div class="ma-2 home">
  <!-- 매장정보 -->
  <v-card
    max-width="90%"
    flat
    class="mx-7 mt-10"
  >
    <!-- <v-card-text>
     <h2 large class="mb-3"> <v-icon large class="mr-3">{{ 'mdi-storefront-outline' }}</v-icon>{{storeInfo.headquarters_name}}</h2>
      <h1 class="text--primary mb-2 ">
        <v-icon large class="mr-2 text--primary">{{ 'mdi-map-marker' }}</v-icon>{{storeInfo.store_location}}점
      </h1>
      <h3 class="button mb-3">
      <v-icon class="ml-1">{{ 'mdi-phone-classic' }}</v-icon>
        {{storeInfo.store_contact}}
      </h3>
    </v-card-text> -->

    <v-list>
      <v-list-item>
        <v-list-item-icon>
          <v-icon large color="indigo darken-4">{{ 'mdi-storefront-outline' }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>
            <h3>{{storeInfo.headquarters_name}}</h3>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
        <v-list-item-icon>
          <v-icon large color="indigo darken-4">{{ 'mdi-map-marker' }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>
            <h2>{{storeInfo.store_location}}점</h2>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
        <v-list-item-icon>
          <v-icon large color="indigo darken-4">{{ 'mdi-phone-classic' }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>
            {{storeInfo.store_contact}}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>


    </v-list>

  <v-divider class="mb-8"></v-divider>
  
  </v-card>
    <!-- 해당 사용자의 최근 발주 내역 -->
  <v-card
    elevation="0"
    max-width="90%"
    class="mx-8"
    max-height="500px"
    
  >
    <v-toolbar
    :color="'grey darken-4'"
    dark
    class="rounded-t-xl"
    >
      <v-toolbar-title>
        <h4> My Latest Order</h4>
      </v-toolbar-title>

      <v-spacer></v-spacer>

    </v-toolbar>


  <v-card class="overflow-y-auto" max-height="400px" 
    elevation="0" outlined>
    <p class="ma-4 body-2">Date: {{this.date.slice(0, 22)}}</p>
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
      <tr v-for="item in order" :key=item.name class="body-2">
        <td>{{item.name}}</td>
        <td>{{item.qty}}</td>
        <td>{{item.unit}}</td>
        <td>{{item.price}}원</td>
        <td>{{item.total_price}}원</td>
      </tr>
      <tr>
        <td></td>
        <td></td>
        <td></td>
        <td class="text-left subtitle-2">합계</td>
        <td>
        <h4 class="text-left subtitle-2">{{total}}원</h4>
        </td>
      </tr>
      
    </tbody>

  </v-simple-table>

  </v-card>
  <v-btn
      large
      dark
      absolute
      bottom
      right
      class="rounded-xl indigo darken-4 mb-1 mr-2"
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
// import {mapState , mapActions} from "vuex"  //
// @ is an alias to /src

export default {
  name: "home",
  components: {
  },
  data(){
    return {
      order:[],
      date:null,
      storeInfo:null
    }
  },
  computed:{
      // ...mapState(['storeInfo']),
      total(){
        var sum=0
        this.order.forEach(item => {
          sum+=(item.price*item.qty)
        })
        return sum
      }
  },
  methods:{
      // ...mapActions(['getStoreInfo']),
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
      getStore() {
          const payload ={
              store_id:store.state.userInfo.store_id
          }
          const path = 'http://localhost:5000/api/store_info'
          axios.post(path, payload)
              .then((res) => {
                console.log("get store info", res.data)
                this.storeInfo = res.data
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
    console.log('created')
    this.getStore()
    this.getOrder()   
  }
};
</script>
