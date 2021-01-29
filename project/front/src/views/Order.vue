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
            >
                <v-slide-item
                    v-for="tag in tags"
                    :key="tag"
                    v-slot="{ active, toggle }"
                >
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
        <p>{{ tags }}</p>
    <div class="d-flex flex-column mb-6">
        <v-card
            v-for="item in items"
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
                v-model="selected"
                :value="item.id"
                @click="item.check=!item.check"
                ></v-checkbox>
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
                <!-- <v-row>
                    <v-col class="mr-5 text-right" align-self="end" ><h3>total parice</h3>{{0}}원</v-col>
                </v-row> -->
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
import {mapState} from "vuex"

export default {
     data(){
        return {
            tag:false,
            tags:['test', 'test1'],
            selected: [],
            items:[
                {
                    id: 1,
                    name:'item1',
                    price: 30000,
                    unit: '박스',
                    info: '...',
                    tag:'test',
                    check:false,
                    qty:null
                },
                {
                    id: 2,
                    name:'item2',
                    price: 30000,
                    unit: '박스',
                    info: '...',
                    tag:'test2',
                    check:false,
                    qty:null
                },
                {
                    id: 3,
                    name:'item3',
                    price: 30000,
                    unit: '박스',
                    info: '...',
                    tag:'test2',
                    check:false,
                    qty:null
                },
                {
                    id: 4,
                    name:'item4',
                    price: 30000,
                    unit: '박스',
                    info: '...',
                    tag:'test',
                    qty:null
                },
                {
                    id: 5,
                    name:'item5',
                    price: 30000,
                    unit: '박스',
                    info: '...',
                    tag:'test',
                    check:false,
                    qty:null
                },
                {
                    id: 6,
                    name:'item6',
                    price: 30000,
                    unit: '박스',
                    info: '...',
                    tag:'test',
                    check:false,
                    qty:null
                },
            ]
            
        }
    },
    computed:{
        
        ...mapState(["userInfo"]),
        total(){
            var items=this.items
            var sum=0
            items.forEach(item => {
                console.log(item.id,item.qty)
                sum+=(item.price*item.qty)
             });
             console.log(sum)
            return sum          
        },
        addTag(n){
            console.log(n)
            var arry=this.selectedTag
            arry.push(n)
            return 0
        },
        t(){
            console.log('ttttt')
            return 0
        }
        // filterByTag(){
        //     return 0
        // }
        
    }
};
</script>
