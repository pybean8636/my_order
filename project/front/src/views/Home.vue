<template>
<div v-if="storeInfo != null && date != null" class="ma-2 home">
  <!-- 매장정보 -->
  <v-card
    max-width="90%"
    flat
    class="mx-7 mt-10"
  >

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
<!-- summary of dash board -->
  
  <v-card
  flat
  class="mt-15 pl-10"
  max-width="90%">
    <h1 class="ml-2 mb-8">Summary</h1>
    <div id="chart" v-if="combo_chartOptions.labels!=null && donut_series != null">
      <v-row align="center">
        <v-col cols="7">
          <apexchart type="line" height="450" :options="combo_chartOptions" :series="combo_series"></apexchart>
        </v-col>
        <v-col cols="5" align-self="center">
            <apexchart type="donut" height="300" :options="donut_chartOptions" :series="donut_series"></apexchart>
        </v-col>
      </v-row>
    </div>
    <div id="chart" v-else>
      뭐야
    </div>
  </v-card>


</div>
</template>

<script>
import axios from 'axios';
import store from "../store/index.js"
import VueApexCharts from "vue-apexcharts";

export default {
  name: "home",
  components: {
    apexchart: VueApexCharts,
  },
  data(){
    return {
      order:[],
      date:null,
      storeInfo:null,
      //combo chart data
      combo_series: [{
          name: 'frequency',
          type: 'column',
          data: null
        }, {
          name: 'payment',
          type: 'line',
          data: null
        }],

        combo_chartOptions: {
          chart: {
            height: 450,
            type: 'line',
          },
          stroke: {
            width: [0, 4]
          },
          title: {
            text: '최근 발주 현황'
          },
          dataLabels: {
            enabled: true,
            enabledOnSeries: [1]
          },
          labels: null,
          xaxis: {
            type: 'datetime'
          },
          yaxis: [{
            title: {
              text: 'frequency',
            },
          
          }, {
            opposite: true,
            title: {
              text: 'payment'
            }
          }]
        },


        //donut chart data
        donut_series: null,

        donut_chartOptions: {
          chart: {
            type: 'donut',
          },
          labels:null,
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              }
            }
          }]
        }



    }
  },
  computed:{
      total(){
        var sum=0
        this.order.forEach(item => {
          sum+=(item.price*item.qty)
        })
        return sum
      }
  },
  methods:{
      async getOrder() {
          const payload ={
              user_key_id:store.state.userInfo.user_key_id
          }
          const path = 'http://localhost:5000/api/order_info'
          await axios.post(path, payload)
              .then((res) => {
                console.log("2 get order info", res.data)
                this.order = res.data.order_info
                this.date = res.data.date
              })
              .catch((error) => {
              console.error(error);
              });
      },
      async getStore() {
          const payload ={
              store_id:store.state.userInfo.store_id
          }
          const path = 'http://localhost:5000/api/store_info'
          await axios.post(path, payload)
              .then((res) => {
                console.log("1 get store info", res.data)
                this.storeInfo = res.data
              })
              .catch((error) => {
              console.error(error);
              });
      },
      async getSummary() {//summary of dash board
          const payload ={
              store_id:store.state.userInfo.store_id
          }
          const path = 'http://localhost:5000/api/dash_board_summary'
          await axios.post(path, payload)
              .then((res) => {
                console.log("3 get summary info", res.data)
                this.combo_series[0].data = res.data.frq
                this.combo_series[1].data = res.data.payment
                this.combo_chartOptions.labels=res.data.dates
                this.donut_series=res.data.tag_count
                this.donut_chartOptions.labels=res.data.tags
                // console.log(this.series)
              })
              .catch((error) => {
              console.error(error);
              });
      },
      setItems(){//store item
        store.state.items=this.order
        this.$router.push({name: 'check'})
      },

  },
  async mounted(){

    await this.getStore()
    await this.getOrder() 
    await this.getSummary() 
  }
};
</script>
