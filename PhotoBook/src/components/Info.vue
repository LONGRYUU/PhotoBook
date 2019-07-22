<template>
  <div>
    <el-container>
      <el-main>
        <el-row>
          <h3>The Day I Uploaded Most Photos: {{day}}</h3>
        </el-row>
        <el-row>
          <h3>Top {{threshold}} Most Appeared Items in My Photos</h3>
          <el-carousel type="card" v-loading.fullscreen.lock="loading">
            <el-carousel-item v-for="(item, index) in words.default" @click="test(item)" :key="index">
              <el-row>
                <h3>{{item}}</h3>
                <el-button type="text" @click="getImage(index)">show {{freqs.default[index].length}} related pictures</el-button>
              </el-row>
              <img :src="url + 'rsz' + freqs.default[index][0] + '.jpg'">
            </el-carousel-item>
          </el-carousel>
        </el-row>
        <el-row>
          <h3>The Category Contains Most Photos: "{{kind}}"</h3>
        </el-row>
        <el-dialog
          :visible.sync="showImage"
          title="Related Photos"
          style="font-size: x-large; padding: 0"
          :fullscreen="true">
          <el-row style="height: 4rem">
            <el-col :span="4.5" v-for="(image, index) in images[selected]" :key="index">
              <el-card>
                <a :href="url + image + '.jpg'" target="_blank">
                  <img :src="url + 'rsz' + image +'.jpg'">
                </a>
              </el-card>
            </el-col>
          </el-row>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script>
    import ElCard from "element-ui/packages/card/src/main";
    import ElCarousel from "element-ui/packages/carousel/src/main";
    import ElContainer from "element-ui/packages/container/src/main";
    import ElMain from "element-ui/packages/main/src/main";
    export default {
        name: "Info",
      components: {ElMain, ElContainer, ElCarousel, ElCard},
      data() {
          return {
            username: '',
            kind:'',
            words:{'default':[1,2,3,4,5]},
            freqs:{'default':[]},
            threshold:5,
            images:[],
            url:'',
            showImage:false,
            selected:0,
            day:'',
            loading:false
          }
      },
      mounted(){
          let self = this;
          self.username = self.$route.query.username;
          self.url='http://localhost:8080/images/' + self.username + '/';
          self.loading = true;
          // self.url='/images/' + self.username + '/';
          // self.$axios.get('http://localhost:8080/server/info',{params:{'username':self.username}})
          self.$axios.get('/server/info',{params:{'username':self.username}})
            .then(res => {
              let freq = JSON.parse(res.data["freq"]);
              // let freq = res.data["freq"]
              self.words.default.splice(0, self.words.default.length);
              self.images.splice(0, self.images.length);
              let count = 0;
              for(let i = 0;i < freq.default.length; i++){
                count++;
                if(count <= self.threshold) {
                  self.words.default.push(freq.default[i].word);
                }
                self.images.push(freq.default[i].images);
              }
              self.freqs.default.splice(0, self.words.default.length);
              for(let i = 0; i < freq.default.length; i++){
                self.freqs.default.push(freq.default[i].images)
              }
              self.kind = res.data["cate"];
              self.day = res.data["date"];
              self.loading = false;
            })
            .catch(err => {
              console.log(err);
              self.$notify({
                title:'error',
                type:'error',
                message:'network error'
              })
            })
      },
      methods:{
          getImage(index){
            let self = this;
            self.selected = index;
            self.showImage = true;
          }
      }
    }
</script>

<style scoped>
  .el-form{
    margin-right: 30%;
    margin-left: 40%;
  }

</style>
