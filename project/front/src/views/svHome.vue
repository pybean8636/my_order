<template>
    <div class="ma-10">
       <div id="headquarters-info" v-if="headquarters_info!=null">
            <v-card
            max-width="93%"
            class="ml-12 mb-5"
            flat>
                <v-row>
                    <v-icon large color="indigo darken-4" class="pb-1 mr-2">{{ 'mdi-store' }}</v-icon>
                    <h3 class="mt-2">{{headquarters_info.headquarters_name}}</h3>
                </v-row>
                <v-row>
                    <v-icon color="indigo darken-4" class="pb-1 mr-2 ml-1">{{ 'mdi-map-marker' }}</v-icon>
                    <p class="mt-4">{{headquarters_info.headquarters_location}}</p>
                </v-row>
                <v-row>
                    <v-icon color="indigo darken-4" class="pb-1 mr-2 ml-1">{{ 'mdi-phone-classic' }}</v-icon>
                    <p class="mt-4">{{headquarters_info.headquarters_contact}}</p>
                </v-row>
            </v-card>
       </div>
        <v-divider class="my-4"></v-divider>
       <div id="store-list" v-if="stores!=null">
           <v-toolbar
            color="indigo lighten-5"
            class="rounded-t-xl pa-3 mx-3 my-8"
            height="80px"
            max-width="93%"
            flat
            >
            <!-- <p class="title">가맹점 리스트</p> -->
            <h3 class="pb-5 ml-3">가맹점 리스트</h3>
            </v-toolbar>
           <v-card 
           v-for="store in paginatedData"
           :key="store.store_id"
           max-width="93%"
           class="mx-2 my-8"
           flat>
               <v-row align="center" justify="center">
                   <v-col cols="2" class="text-left">
                       <v-icon color="indigo darken-4" class="pb-1">{{ 'mdi-storefront-outline' }}</v-icon>
                       {{store.store_name}}점
                   </v-col>
                   <v-col cols="3" class="text-left">
                       <v-icon color="indigo darken-4" class="pb-1">{{ 'mdi-map-marker' }}</v-icon>
                       {{store.store_location}}
                   </v-col>
                   <v-col cols="2" class="text-left">
                       <v-icon color="indigo darken-4" class="pb-1">{{ 'mdi-phone-classic' }}</v-icon>
                       {{store.store_contact}}
                   </v-col>
                   <v-col cols="4" class="text-left">
                       <v-icon color="indigo darken-4" class="pb-1">{{ 'mdi-calendar-month' }}</v-icon>
                       최근 발주: {{store.latest_date}}
                   </v-col>
               </v-row>
               <v-divider class="mt-6"></v-divider>
           </v-card>
           <div id="pagination">
                <div class="text-center my-5">
                    <v-col cols="11">
                        <v-pagination
                        v-model="pageNum"
                        :length="pageCount"
                        ></v-pagination>
                    </v-col>
                    
                </div>
            </div>
       </div>
    </div>
</template>


<script>
import axios from 'axios'
import store from "../store/index.js"

export default {
    name:"sv_home",
    data(){
        return{
            headquarters_info: null,
            stores: null,

            pageNum :1,//현재 페이지
            pageSize:5,//한 페이지에 나올 가맹점 수

        }
    },
    computed:{

        pageCount(){//페이지 개수
            let store_length=this.stores.length,
            listSize= this.pageSize,
            page=Math.floor((store_length-1)/listSize)+1;
            console.log(page)
            return page;
        },
        paginatedData(){//페이지 별로 슬라이스
            const start = (this.pageNum -1) * this.pageSize,
            end= start + this.pageSize;

            return this.stores.slice(start, end);
        }

    },
    methods:{
        async getHead() {
            const payload ={
                user_key_id:store.state.userInfo.user_key_id
            }
            const path = 'http://localhost:5000/api/headquarters_info'
            await axios.post(path, payload)
                .then((res) => {
                    this.headquarters_info = res.data.headquarters_info
                })
                .catch((error) => {
                console.error(error);
                });
        },
        async getSvStore() {
            const payload ={
                user_key_id:store.state.userInfo.user_key_id
            }
            const path = 'http://localhost:5000/api/sv_store_info'
            await axios.post(path, payload)
                .then((res) => {
                    this.stores = res.data.sv_store_info
                })
                .catch((error) => {
                console.error(error);
                });
        },
    },
    async mounted(){
        await this.getHead()
        await this.getSvStore()
    }
}
</script>