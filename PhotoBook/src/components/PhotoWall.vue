<template>
  <div>
    <el-main style="height: 580px">

      <classify></classify>
    <el-tabs style="margin-left: 5px">
      <el-tab-pane label="timeline">
        <!--sort：-->
        <!--<el-radio-group v-model="reverse">-->
          <!--<el-radio :label="true">latest</el-radio>-->
          <!--<el-radio :label="false">reverse</el-radio>-->
        <!--</el-radio-group>-->
        <el-timeline>
          <el-timeline-item :timestamp="time" :key="index" placement="top" v-for="(time,index) in timestamps" size="large">
            <el-row>
              <el-col :span="8" :key="idx" v-for="(id,idx) in timeIndices[index]">
                <el-card>
                  <el-row>
                    <el-tooltip placement="left" :content="images[id].caption">
                    <a :href="url + images[id].fileName +'.jpg'" target="_blank">
                      <img :src="url + 'rsz' + images[id].fileName +'.jpg'" :alt="images[id].caption">
                    </a>
                    </el-tooltip>
                  </el-row>
                  <el-row style="margin-top: 3px">
                    <el-col :span="16">
                      <el-select v-model="images[id].category"
                                 filterable
                                 allow-create>
                        <el-option
                          v-for="item in categories"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value">
                        </el-option>
                      </el-select>
                    </el-col>
                    <!--<el-col :span="2" style="margin-left: 39px">-->
                      <el-button type="text" @click="modify(images[id])" v-loading.fullscreen.lock="loading">Modify</el-button>
                    <!--</el-col>-->
                    <!--<el-col :span="2">-->
                      <el-button type="text" @click="deletePhoto(images[id])" v-loading.fullscreen.lock="loading">
                        Delete
                      </el-button>
                    <!--</el-col>-->
                  </el-row>
                </el-card>
              </el-col>
            </el-row>
          </el-timeline-item>
        </el-timeline>
      </el-tab-pane>
      <el-tab-pane label="categories">
        <el-timeline>
          <el-timeline-item :timestamp="category.value" :key="index" v-for="(category,index) in categories" placement="top" size="large">
            <el-row>
              <el-col :span="8" :key="idx" v-for="(id,idx) in cateIndices[index]">
                <el-card>
                  <el-tooltip placement="left" :content="images[id].caption">
                  <el-row>
                    <a :href="url + images[id].fileName +'.jpg'" target="_blank">
                      <img :src="url + 'rsz' + images[id].fileName +'.jpg'" :alt="images[id].caption">
                    </a>
                  </el-row>
                  </el-tooltip>
                  <!--<el-row>-->
                    <!--<el-input v-model="images[id].userCaption"></el-input>-->
                  <!--</el-row>-->
                  <el-row style="margin-top: 3px">
                    <el-col :span="16">
                      <el-select v-model="images[id].category"
                                 filterable
                                 allow-create>
                        <el-option
                          v-for="item in categories"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value">
                        </el-option>
                      </el-select>
                    </el-col>
                    <!--<el-col :span="4" style="margin-left: 39px">-->
                      <el-button type="text" @click="modify(images[id])" v-loading.fullscreen.lock="loading">Modify</el-button>
                    <!--</el-col>-->
                    <el-button type="text" @click="deletePhoto(images[id])" v-loading.fullscreen.lock="loading">Delete</el-button>
                  </el-row>
                </el-card>
              </el-col>
            </el-row>
          </el-timeline-item>
        </el-timeline>
      </el-tab-pane>
    </el-tabs>
    </el-main>
  </div>
</template>

<script>
    import ElCard from "element-ui/packages/card/src/main";
    import ElTimeline from "element-ui/packages/timeline/src/main";
    import ElTabPane from "element-ui/packages/tabs/src/tab-pane";
    import ElMain from "element-ui/packages/main/src/main";
    import Classify from  "./Classify.vue"
    export default {
      name: "PhotoWall",
      components: {ElMain, ElTabPane, ElTimeline, ElCard, Classify},
      data() {
        return {
          images:[],
          url:'',
          username:'',
          userClass:'',
          categories:[],
          cates:[],
          timestamps:[],
          timeIndices:[],
          cateIndices:[],
          reverse:false,
          loading:false
        }
      },
      created(){
        let self = this;
        self.loading = true;
        self.username = self.$route.query.username;
        self.images.splice(0, self.images.length);
        self.timestamps.splice(0, self.timestamps.length);
        self.categories.splice(0, self.categories.length);
        self.timeIndices.splice(0, self.timeIndices.length);
        self.cateIndices.splice(0, self.cateIndices.length);
        self.cates.splice(0,self.cates.length);
        self.$axios.get('http://localhost:8080/server/server/allImages',{params:{'username': self.username}})
        // self.$axios.get('/server/allImages', {params: {'username': this.username}})
          .then(res => {
            self.url = 'http://localhost:8080/images/' + this.username + "/";
            // self.url='/images/'+this.username+"/";
            for (let i = 0; i < res.data["imageMap"]["imageIDs"].length; i++) {
              self.images.push({
                'fileName': res.data["imageMap"]["imageIDs"][i],
                'category': res.data["imageMap"]["categories"][i],
                'caption': res.data["imageMap"]["captions"][i]
              });
            }
            for (let item in res.data["cateMap"]) {
              self.categories.push({'value': item, 'label': item});
              self.cateIndices.push(res.data["cateMap"][item]);
              self.cates.push(item)
            }
            for (let item in res.data["timeMap"]) {
              self.timestamps.push(item);
              self.timeIndices.push(res.data["timeMap"][item])
            }
            self.loading = false;
            self.$notify({
              type: 'success',
              message: 'All photos are here!',
              title: 'success'
            })
          })
          .catch(err => {
            console.log(err);
            self.loading = false;
            self.$notify({
              type: 'error',
              message: 'failed to get photos',
              title: 'network error'
            })
          });
      },
      mounted(){
        let self = this;
        this.$bus.$on('upload', function (val) {
          let idx = self.images.push({
            'fileName': val['imageID'],
            'category': val['category'],
            'caption':val['caption']
          }) - 1;
          if(self.cates.indexOf(val['category']) < 0){
            self.categories.push({'value':val['category'], 'label': val['category']});
            self.cates.push(val['category']);
            self.cateIndices.push([idx])
          }else {
            self.cateIndices[self.cates.indexOf(val['category'])].push(idx)
          }
          if(self.timestamps.indexOf(val['uploadDate']) < 0){
            let arr = [];
            self.timestamps.push(val['uploadDate']);
            self.timeIndices.push([idx])
          }else {
            self.timeIndices[self.timestamps.indexOf(val['uploadDate'])].push(idx)
          }
        });
      },
      methods:{
        modify(item){
          let self = this;
          // self.loading = true;
          self.username = self.$route.query.username;
          let params = {
            'imageID':item.fileName,
            'userClass':item.category,
            'username': self.username
          };
         self.$axios.post('/server/modifyPhoto', params)
         // self.$axios.post('http://localhost:8080/server/modifyPhoto', params)
           .then(res => {
             if(res.data === 'success'){
               self.modifyItems(item);
               self.$notify({
                 type:'success',
                 message:'updated successfully!',
                 title:'success'
               })
             }else {
               self.$notify({
                 type:'error',
                 message:'failed to modify information!',
                 title:'network error'
               })
             }
           })
           .catch(err => {
             console.log(err);
             self.loading = false;
             self.$notify({
               type:'error',
               message:'failed to modify information!',
               title:'network error'
             })
           })
        },
        modifyItems(item){
          let self = this;
          for(let i = 0; i < self.images.length; i++){
            if(self.images[i].fileName === item.fileName){
              for(let j = 0; j < self.cateIndices.length; j++){
                for(let k = 0; k < self.cateIndices[j].length; k++){
                  if(self.cateIndices[j][k] === i && item.category !== self.cates[j]){
                    self.cateIndices[j].splice(k, 1);
                    if(self.cateIndices[j].length === 0){
                      self.cateIndices.splice(j, 1);
                      self.categories.splice(j, 1);
                      self.cates.splice(j, 1);
                    }
                    if(self.cates.indexOf(item.category) < 0){
                      self.categories.push({label:item.category, value:item.category});
                      let arr = [];
                      arr.push(i);
                      self.cateIndices.push(arr);
                      self.cates.push(item.category);
                    }else{
                      self.cateIndices[self.cates.indexOf(item.category)].push(i);
                    }
                    self.loading = false;
                    return;
                  }
                }
              }
            }
          }
        }
        ,
        deletePhoto(item){
          let self = this;
          self.username = self.$route.query.username;
          // self.loading = true;
          let params = {
            'username': self.username,
            'imageID':item.fileName
          };
          console.log('here1');
          // self.$axios.post('http://localhost:8080/server/delete', params)
          self.$axios.post('/server/delete', params)
            .then(res => {
              // console.log(res.data);
              console.log('here2');
              if(res.data === 'success'){
                for(let i = 0; i < self.images.length; i++){
                  if(self.images[i].fileName === item.fileName){
                    self.deleteCate(i);
                    self.deleteTime(i);

                    break;
                  }
                }
                // self.loading = false;
                // self.$notify({
                //   type:"info",
                //   message:'finished',
                //   title:'success'
                // });
              }
              else{
                self.$notify({
                  type:'error',
                  message:'failed to delete photo!',
                  title:'network error'
                });
                self.loading =false;
              }
            })
            .catch(err => {
              console.log(err);
              self.$notify({
                type:'error',
                message:'failed to delete photo!',
                title:'network error'
              });
              self.loading = false;
            })
        },
        deleteCate(i){
          let self = this;
          for(let j = 0; j < self.cateIndices.length; j++){
            for(let k = 0; k < self.cateIndices[j].length; k++){
              if(self.cateIndices[j][k] === i){
                self.cateIndices[j].splice(k, 1);
                if(self.cateIndices[j].length === 0){
                  self.cateIndices.splice(j, 1);
                  self.categories.splice(j, 1);
                  self.cates.splice(j, 1)
                }
                return;
                // break;
              }
            }
            // break;
          }
        },
        deleteTime(i){
          let self = this;
          for(let j = 0; j < self.timeIndices.length; j++){
            for(let k = 0; k < self.timeIndices[j].length; k++){
              if(self.timeIndices[j][k] === i){
                self.timeIndices[j].splice(k, 1);
                if(self.timeIndices[j].length === 0){
                  self.timeIndices.splice(j, 1);
                  self.timestamps.splice(j, 1);
                  self.loading = false;
                  self.$notify({
                    type:'info',
                    message:'deleted a photo',
                    title:'finished'
                  })
                }
                return;
                // break;
              }
            }
            // break;
          }
        }
      }
    }
</script>

<style scoped>

</style>
