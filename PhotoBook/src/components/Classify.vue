<template>
  <div>
    <!--<el-container>-->
      <!--<el-main>-->

        <el-row style="margin-bottom: 20px">
          <span>Classify All Photos With Tags Below：</span>
        </el-row>
          <el-tag :key="index" v-for="(tag,index) in dynamicTags"
                  closable :disable-transitions="false"
                  @close="deleteTag(tag)" type="">
            {{tag}}
          </el-tag>
          <el-input
            maxlength="20"
            v-if="inputVisible" v-model="inputValue"
            ref="tagInput" size="small" class="input-new-tag"
            @blur="handleInputConfirm">
          </el-input>
          <el-button v-else size="small" @click="showInput"
                     class="button-new-tag">New Tag</el-button>
          <el-button type="primary" @click="classifyAll" size="small" v-loading.fullscreen.lock="loading">get classified</el-button>
        <el-dialog
          :visible.sync="showResult"
          title="Results"
          :fullscreen="true">
          <el-timeline>
            <el-timeline-item :timestamp="tag" :key="index" v-for="(tag,index) in dynamicTags" placement="top">
              <el-row>
                <el-col :span="4.5" :key="i" v-for="(image,i) in images[tag]">
                  <el-card>
                    <el-tooltip placement="bottom" :content="captions[tag][i]">
                      <a :href="url + image + '.jpg'" target="_blank">
                        <img :src="url + 'rsz' + image +'.jpg'">
                      </a>
                    </el-tooltip>
                  </el-card>
                </el-col>
              </el-row>
            </el-timeline-item>
          </el-timeline>
          <el-button @click="apply" type="primary">Apply</el-button>
        </el-dialog>
      <!--</el-main>-->
    <!--</el-container>-->
  </div>
</template>

<script>
    import ElCard from "element-ui/packages/card/src/main";
    import ElUpload from "element-ui/packages/upload/src/index";
    import ElTimeline from "element-ui/packages/timeline/src/main";
    export default {
      name: "Classify",
      components: {ElTimeline, ElUpload, ElCard},
      data() {
          return {
            dynamicTags:['cat'],
            images: {},
            captions:{},
            showResult:false,
            url:'http://localhost:8080/server/images/',
            inputVisible:false,
            inputValue:'',
            username:'',
            loading:false,
          }
      },
      beforeMount(){
        this.username = this.$route.query.username;
      },
      methods:{
        classifyAll(){
          let self = this;
          self.username = self.$route.query.username;
          let params = {'username': self.username, 'tags': JSON.stringify(self.dynamicTags)};
          self.loading = true;
          // self.$axios.post('http://localhost:8080/server/classifyAll', params)
          self.$axios.post('/server/classifyAll', params)
            .then(res => {
              console.log(res.data);
              self.showResult = true;
              self.url = 'http://localhost:8080/images/' + self.username + '/';
              // self.url = '/images/' + self.username + '/';
              self.images = res.data.ids;
              self.captions = res.data.caps;
              self.$notify({
                type:'success',
                message:'Here are the results.',
                title:'result'
              });
              self.loading = false;
            })
            .catch(err => {
              console.log(err);
              self.$notify({
                type:'error',
                message:'failed to classify',
                title:'network error'
              });
              self.loading = false;
            })
        },
        apply(){
          let self = this;
          self.username = self.$route.query.username;
          self.loading = true;
          let images = {'tags':self.dynamicTags, 'ids': self.images};
          let params = {'username':self.username, 'tags': JSON.stringify(images)};
          self.$axios.post('/server/batchUpdate', params)
            .then(res => {
              if(res.data === 'success')
              {
                self.$notify({
                  type:'success',
                  message:'Finished Applying.',
                  title:'result'
                });
                window.location.reload();
              }
              else{
                self.$notify({
                  type:'error',
                  message:'failed to classify',
                  title:'network error'
                });
                self.loading = false;
              }
            })
            .catch(err => {
              console.log(err);
              self.$notify({
                type:'error',
                message:'failed to classify',
                title:'network error'
              });
              self.loading = false;
            })
          // })
        },
        deleteTag(tag){
          this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
        },
        showInput(){
          this.inputVisible = true;
        },
        handleInputConfirm() {
          let inputValue = this.inputValue;
          inputValue = inputValue.replace(/\s+/g, " ");
          if (inputValue) {
            this.dynamicTags.push(inputValue);
          }
          this.inputVisible = false;
          this.inputValue = '';
        },
        myUpload(file){
          let formData = new FormData();
          let self = this;
          let fileName = String(file.file.name);
          let start = fileName.lastIndexOf('.');
          let suffix = fileName.substring(start + 1);
          if(suffix !== 'jpg' && suffix !== 'jpeg' && suffix !== 'png'){
            self.$notify({
              title:'wrong format!',
              message:'Please upload photos in jpg,png or jpeg format.',
              type:'error'
            });
            self.$refs.classify.clearFiles();
            return true;
          }
          self.loading = true;
          self.username = self.$route.query.username;
          formData.append('username', self.username);
          formData.append('file', file.file);
          formData.append('tags',JSON.stringify(self.dynamicTags));
          // self.$axios.post('http://localhost:8080/server/classifyPhoto', formData)
          self.$axios.post('/server/classifyPhoto', formData)
            .then(res => {
                console.log(res.data);
                self.loading = false;
                self.similarities.splice(0, self.similarities.length);
                for(let item in res.data){
                  self.similarities.push({
                    tag:item,
                    data:res.data[item]
                  })
                }
                self.photoResult = true;
                self.$notify({
                  title:'result',
                  type:'success',
                  message:'here are the results'
                });
                self.$refs.classify.clearFiles()
            })
            .catch(err => {
              console.log(err);
              self.$notify({
                title:'network error',
                type:'error',
                message:'failed to classify'
              });
              self.loading = false;
              self.$refs.classify.clearFiles()
            });
          return true
        }
      }
    }
</script>

<style scoped>
 .el-form{
   margin-right: 20%;
 }
 .el-main {
   /*background-image: url("../assets/pure.jpg");*/
   text-align: center;
   height: 100px;
   margin: 0;
 }
  .el-form-item{
    margin-bottom: 10px;
  }

  .input-new-tag{
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }

 .button-new-tag {
   margin-left: 10px;
   height: 32px;
   line-height: 30px;
   padding-top: 0;
   padding-bottom: 0;
 }

  .el-tag{
    margin-left: 10px;
  }

  .el-card__body{
    padding: 0;
  }
</style>
