<template>
    <v-container class="ma-10">
        <h2>{{ userInfo.store_location }}점 발주</h2>
    <!-- 스위치 -->
      <v-switch
            label="태그별 모아보기 "
            color="success"
            value="success"
            hide-details
            shaped
            @click="tag = !tag"
            class="mb-8 "
        ></v-switch>

        <!-- 태그선택 슬라이드 시트 -->
        <v-sheet
        max-width="900"
        v-if="tag"
        class="mb-5"
         >
            <v-slide-group
            multiple
            show-arrows
            v-model="model" 
            >
                <v-slide-item
                    v-for="tag in tags"
                    :key="tag"
                    :value="tag"
                    v-slot="{ active, toggle }"
                >
                <!-- 모델에 선택된 태그들로 필터링하기 위해서 태그 이름을 값으로 배열에 저장 -->
                    <v-btn
                    class="mx-2"
                    :input-value="active"
                    active-class="teal white--text"
                    depressed
                    rounded
                    @click="toggle"
                    >
                    <!-- 태그 받아와야 함~! -->
                    {{ tag }}
                    </v-btn>
                </v-slide-item>
            </v-slide-group>
        </v-sheet>

        <v-divider class="mb-8"></v-divider>
        <!-- 아이템 나열 -->
        <!-- <p>{{ model }}</p> -->
    <div class="d-flex flex-column mb-6">
        <v-card
            v-for="item in filterByTag"
            :key="item.id"
            class="pa-3 ma-1"
            outlined
            tile
            max-width="93%"
            :color="item.check? 'teal lighten-5' : 'white'"
        >
        <v-row >
            <v-col cols="1" align-self="center">
                <v-checkbox
                :value="item.id"
                @click="item.check=!item.check"
                ></v-checkbox>
                <!-- v-model="selected" -->
            </v-col>

             <v-col cols="4" >
                 <v-row justify="start">
                <h3 class="mt-2" >{{ item.name }}</h3>
                 </v-row>
                <v-row >
                    <p align-self="center">{{ item.info }}</p>
                </v-row>
                <v-row class="mb-1">
                    <v-chip
                        color="teal"
                        text-color="white"
                        >
                        {{item.tag}}
                    </v-chip>
                </v-row>
            </v-col>

            <v-col align-self="center">
                <v-row >
                    <v-col cols="7 text-right" align-self="center">{{item.price}}원</v-col>
                    <v-col cols="2" align-self="center">
                        <v-text-field
                            min="0"
                            type="number"
                            :value="item.qty"
                            v-model.number="item.qty"
                        ></v-text-field>
                    </v-col>
                    <v-col align-self="center">
                        {{item.unit}}
                    </v-col>
                        
                </v-row>
            </v-col>

        </v-row>
        <v-divider class="mt-3"></v-divider>
        </v-card>
        <v-col align-self="start" cols="11 text-right" class="my-3">
            <h2>total price</h2>
            <h3 class="mb-6">{{total}}원</h3>
            
            <v-btn
            color="teal"
            class="white--text "
            large
            rounded
            @click="$router.push({name: 'check'})"
            >
                선택 완료
                <v-icon
                    right
                    dark
                >
                    mdi-arrow-right-bold
                </v-icon>
            </v-btn>
        </v-col>        
    </div>

  </v-container>
</template>

<script>
import {mapState, mapActions} from "vuex"
import store from "../store/index.js"

export default {
     data(){
        return {
            model:null, //선택된 태그 저장
            tag:false, //태그별 보기 필터링
            
        }
    },
    computed:{
        
        ...mapState(["userInfo", 'items', 'tags']),
        total(){ //총가격저장
            var items=this.items
            var sum=0
            items.forEach(item => {
                if(item.check){
                    sum+=(item.price*item.qty)
                }
             });
            return sum          
        },
        filterByTag(){
            if (this.tag===true && this.model!=null && this.model.length>0){
                return this.items.filter((item)=>{
                    return this.model.includes(item.tag)
                })
            }else{
                return this.items
            }
        },
        
    },
    methods:{
        ...mapActions(['getItems'])
        
    },
    created() {
        store.dispatch('getItems')
  },
};
</script>
