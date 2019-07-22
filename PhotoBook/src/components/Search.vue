<template>
    <div>
      <el-container>
        <el-main>
            <el-form>
              <el-form-item>
                <el-upload
                  action="http://localhost:8080/server/searchByPhoto"
                  :http-request="myUpload"
                  list-type="picture"
                  drag>
                  <i class="el-icon-upload"></i>
                  <div>
                    Drag Or Click To Find A Similar Picture.
                  </div>
                </el-upload>
              </el-form-item>
              <el-form-item>
                Or Input Any Words Here.Tags, Descriptions Or Whatever.
                <el-input placeholder="Input What You Want To Search For." v-model="tags"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submit" icon="el-icon-search"
                v-loading.fullscreen.lock="loading">Search</el-button>
              </el-form-item>
            </el-form>

          <el-dialog
            :visible.sync="showResult"
            :title="'results: ' + query"
            style="font-size: x-large; padding: 0"
            :fullscreen="true">
            <el-row style="height: 4rem">
                  <el-col :span="4.5" :key="id" v-for="(image,id) in images['imageIDs']">
                    <el-card style="padding: 0; height: 280px; width: 280px">
                      <el-tooltip placement="bottom" :content="images['captions'][id]">
                        <a :href="url + image + '.jpg'" target="_blank">
                          <img :src="url + 'rsz' + image +'.jpg'">
                        </a>
                      </el-tooltip>
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
    import ElTabPane from "element-ui/packages/tabs/src/tab-pane";
    export default {
      name: "Search",
      components: {ElTabPane, ElCard},
      data() {
          return {
            showResult: false,
            tags:'',
            images:{"imageIDs":[], "captions":[]},
            username:'',
            url:'http://localhost:8080/images/',
            loading:false,
            query:''
          }
      },
      methods: {
        submit() {
          let self = this;
          self.username = self.$route.query.username;
          self.loading = true;
          // self.$axios.post('http://localhost:8080/server/searchByWords',{"username": self.username,"tags":self.tags})
          self.$axios.post('/server/searchByWords',{"username": self.username,"tags":self.tags})
            .then(res => {
              console.log(res.data);
              self.images["imageIDs"].splice(0, self.images["imageIDs"].length);
              self.images["captions"].splice(0, self.images["captions"].length);
              // self.url = 'http://localhost:8080/images/' + self.username + "/";
              self.url = 'http://localhost:8080/images/' + self.username + "/";
              for(let i = 0; i < res.data["imageIDs"].length; i++){
                self.images['imageIDs'].push(res.data['imageIDs'][i]);
                self.images['captions'].push(res.data['captions'][i])
              }
              self.query = res.data['query'];
              self.showResult = true;
              self.loading = false;
            })
            .catch(err => {
              console.log(err);
              self.loading = false;
              self.$notify({
                type:'error',
                title:'error',
                message:'network error'
              })
            })
        },
        myUpload(file){
          let formData = new FormData();
          let self = this;
          self.loading = true;
          self.username = self.$route.query.username;
          let fileName = String(file.file.name);
          let start = fileName.lastIndexOf('.');
          let suffix = fileName.substring(start + 1);
          if(suffix !== 'jpg' && suffix !== 'jpeg' && suffix !=='png'){
            self.loading = false;
            self.$notify({
              title:'error',
              message:'wrong type files!',
              type:'error'
            });
            self.$refs.upload.clearFiles();
            return true;
          }
          formData.append('file',file.file);
          formData.append('username',self.username);
          // self.$axios.post('http://localhost:8080/server/searchByPhoto',formData)
          self.$axios.post('/server/searchByPhoto',formData)
            .then(res => {
              console.log(res.data);
              self.images["imageIDs"].splice(0, self.images["imageIDs"].length);
              self.images["captions"].splice(0, self.images["captions"].length);
              self.url = 'http://localhost:8080/images/' + self.username + "/";
              // self.url = '/images/' + self.username + "/";
              for(let i = 0; i < res.data["imageIDs"].length; i++){
                self.images['imageIDs'].push(res.data['imageIDs'][i]);
                self.images['captions'].push(res.data['captions'][i])
              }
              self.query = res.data['query'];
              self.showResult = true;
              self.loading = false;
            })
            .catch(err => {
              console.log(err);
              self.loading = false;
              self.$notify({
                type:'error',
                title:'error',
                message:'network error'
              })
            })
        }
      }
    }
</script>

<style scoped>
  .el-main {
    /*background-image: url("../assets/pure.jpg");*/
    text-align: center;
    line-height: 160px;
    height: 580px;
    margin: 0;
  }
  .el-form{
    margin-left: 30%;
    margin-right: 30%;
  }
</style>
