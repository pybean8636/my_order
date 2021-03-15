<template>
    <div>
        {{regions}}
        {{arrayData}}
        {{makeData}}
    </div>
</template>

<script>
import axios from 'axios'
import store from "../store/index.js"

export default {
    name:"item",
    data(){
        return{
            arrayData:[],
            regions:null,
            dataRegionSeries:[],
            colors :[
                "#008FFB",
                "#00E396",
                "#FEB019",
                "#FF4560",
                "#775DD0",
                "#00D9E9",
                "#FF66C3"
                ]
        }
    },
    computed: {
        makeData(){//지역 데이터 생성 
            var dataSet=this.arrayData,
            regions=this.regions,
            dataRegionSeries=[]
            if (regions!=null){
                for(var i=0; i<regions.length; i++){
                    dataRegionSeries.push({
                        x:regions[i],
                        y:dataSet[i].region_count,
                        color: this.colors[i],
                        stores: dataSet[i].stores
                    })
                }
            }
            
            return dataRegionSeries

        }
    },
    methods: {
        async getRegionData(){
            const payload={
                user_key_id:store.state.userInfo.user_key_id
            }
            const path = 'http://localhost:5000/api/sv_board_region'
            await axios.post(path, payload)
                .then((res)=>{
                    this.regions= res.data.regions
                    /////////////////////////////////////////////////
                    this.regions.forEach(region => {
                        this.arrayData.push(res.data.region_data[region])
                    });
                    this.region_data_arr
                })
        }
    },
    mounted(){
        this.getRegionData()
    }
}
</script>