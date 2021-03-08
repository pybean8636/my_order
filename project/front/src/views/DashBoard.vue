<template>
    <div class="ma-13">
        <v-card
        class="my-15"
        flat>
            <h1 class="ml-2 my-10">Dash Board</h1>
            <div id="chart" v-if="donut_series != null && bar_series!=null">
                <v-row>
                    <v-col cols="4" align-self="center" >
                        <apexchart type="donut" height="330" :options="donut_chartOptions" :series="donut_series"></apexchart>
                    </v-col>    
                    <v-col cols="8" align-self="center">
                        <apexchart type="bar" height="300" :options="bar_chartOptions" :series="bar_series"></apexchart>
                    </v-col>  
                </v-row>
            </div>
            <div v-else>
                뭐야
            </div>
        </v-card>
        <v-card 
        class="my-15"
        flat>
            <div id="chart" v-if="stacked_chartOptions.xaxis.categories!=null">
                <v-row>
                    <v-col cols="12" align-self="center">
                        <apexchart type="bar" height="350" :options="stacked_chartOptions" :series="stacked_series"></apexchart>
                    </v-col>
                </v-row>
            </div>
            <div v-else>
                뭐야
            </div>
        </v-card>
        <v-card 
        class="my-15"
        flat>
            <div id="chart" v-if="line_series!=null">
                <v-row>
                    <v-col>
                        <apexchart type="line" height="350" :options="line_chartOptions" :series="line_series"></apexchart>
                    </v-col> 
                </v-row>
            </div>
            <div v-else>
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
    name:"board",
    components: {
        apexchart: VueApexCharts,
    },
    data(){
        return{


            //donut chart
            donut_series: null,

            donut_chartOptions: {
            chart: {
                type: 'donut',
            },
            title: {
                text: '태그 비율'
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
            },


            //사용자별 발주 빈도 stacked chart data
            stacked_series: [],//사용자별 발주 수
            stacked_chartOptions: {
            chart: {
                type: 'bar',
                height: 350,
                stacked: true,
                toolbar: {
                show: true
                },
                zoom: {
                enabled: true
                }
            },
            title: {
                text: '발주 빈도 그래프'
            },
            responsive: [{
                breakpoint: 480,
                options: {
                legend: {
                    position: 'bottom',
                    offsetX: -10,
                    offsetY: 0
                }
                }
            }],
            plotOptions: {
                bar: {
                borderRadius: 8,
                horizontal: false,
                },
            },
            xaxis: {
                type: 'datetime',
                categories: null,//발주 날짜
            },
            legend: {
                position: 'right',
                offsetY: 40
            },
            fill: {
                opacity: 1
            }
            },

            //payment line chart
          
            line_series: null,//payment data
            line_chartOptions: {
                chart: {
                    height: 350,
                    type: 'line',
                    dropShadow: {
                        enabled: true,
                        color: '#000',
                        top: 18,
                        left: 7,
                        blur: 10,
                        opacity: 0.2
                    },
                    toolbar: {
                        show: true
                    },          
                    zoom: {
                        type: "x",
                        enabled: true,
                        autoScaleYaxis: true
                    },
                },
                colors: ['#2E9AFE'],
                dataLabels: {
                    enabled: true,
                },
                stroke: {
                    curve: 'smooth'
                },
                title: {
                    text: '지출 내역',
                    align: 'left'
                },
                grid: {
                    borderColor: '#e7e7e7',
                    row: {
                    colors: ['transparent'], // takes an array which will be repeated on columns
                    opacity: 0.5
                    },
                },
                markers: {
                    size: 1
                },
                xaxis: {
                    categories: null,//dates
                    title: {
                    text: 'Month Date'
                    }
                },
                yaxis: {
                    title: {
                    text: 'Payment'
                    }
                },
                legend: {
                    position: 'top',
                    horizontalAlign: 'right',
                    floating: true,
                    offsetY: -25,
                    offsetX: -5
                }
            },
            
          
          //item rating bar chart


          
            bar_series: null,
            bar_chartOptions: {
            chart: {
                type: 'bar',
                height: 350
            },
            title: {
                text: '물품 순위'
            },
            plotOptions: {
                bar: {
                distributed: true,
                horizontal: true,
                }
            },
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: null,//item name
            }
            },
          
          
        
          

        }
    },
    methods:{
        async getSummary() {//tag ratio donut chart
            const payload ={
                store_id:store.state.userInfo.store_id
            }
            console.log('line_series',this.line_series)
            const path = 'http://localhost:5000/api/dash_board_summary'
            await axios.post(path, payload)
                .then((res) => {
                    this.donut_series=res.data.tag_count
                    this.donut_chartOptions.labels=res.data.tags
                    console.log(this.line_series)
                })
                .catch((error) => {
                console.error(error);
                });
        },
        async get_stacked() {//stacked chart
            const payload ={
                store_id:store.state.userInfo.store_id
            }
            const path = 'http://localhost:5000/api/dash_board_stacked'
            await axios.post(path, payload)
                .then(async (res) => {
                    var users_id= res.data.users
                    var i
                    console.log('users_id', users_id)
                    for (i=0; i<users_id.length; i++){
                        this.stacked_series.push({
                            name: users_id[i],
                            data: res.data[users_id[i]]
                        })
                    }
                    this.stacked_chartOptions.xaxis.categories=res.data.dates
                    console.log('data', this.stacked_chartOptions.xaxis.categories)
                    // console.log(this.series)
                })
                .catch((error) => {
                console.error(error);
                });
        },
        async get_item_bar() {//stacked chart
            const payload ={
                store_id:store.state.userInfo.store_id
            }
            const path = 'http://localhost:5000/api/dash_board_item'
            await axios.post(path, payload)
                .then(async (res) => {
                    this.bar_series=[{
                        data:res.data.item_qty
                    }]
                    this.bar_chartOptions.xaxis.categories=res.data.item_names
                })
                .catch((error) => {
                console.error(error);
                });
        },
        async get_payment_year() {//payment_year
            const payload ={
                store_id:store.state.userInfo.store_id
            }
            const path = 'http://localhost:5000/api/dash_board_payment'
            await axios.post(path, payload)
                .then(async (res) => {
                    this.line_series=[{
                        name:"payment_year",
                        data:res.data.payment_year 
                    }]
                    this.line_chartOptions.xaxis.categories=res.data.dates_year
                })
                .catch((error) => {
                console.error(error);
                });
        },

    },
    async mounted(){
        await this.get_stacked()
        await this.getSummary()
        await this.get_item_bar()
        await this.get_payment_year()
    }
}
</script>