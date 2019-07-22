<template>
    <div>
      <el-container>
        <el-main>
          <el-form>
            <el-form-item>
              <el-upload
                action="http://localhost:8080/server/generateByPhoto"
                drag
                ref="generate"
                :auto-upload="false"
                :http-request="myUpload"
                :on-change="checkEmpty"
                :on-remove="handleRemove"
                list-type="picture"
              >
                <i class="el-icon-upload"></i>
                <div>
                  Drag or Click to pick a local file.
                </div>
              </el-upload>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submit" v-loading.fullscreen.lock="loading" :disabled="!clickable">Generate</el-button>
            </el-form-item>
            <el-form-item>
              <el-timeline>
                <el-timeline-item v-for="(caption,index) in captions" :key="index">
                {{caption.value}}
                </el-timeline-item>
              </el-timeline>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="clearFiles" v-loading.fullscreen.lock="loading">Clear</el-button>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </div>
</template>

<script>
    import ElTimeline from "element-ui/packages/timeline/src/main";
    export default {
      name: "Generate",
      components: {ElTimeline},
      data() {
          return {
            captions:[],
            loading:false,
            username:'',
            clickable:false,
            fileList:[]
          }
      },
      methods:{
          myUpload(file){
            let formData = new FormData();
            let self = this;
            self.username = self.$route.query.username;
            formData.append('username', self.username);
            formData.append('file', file.file);
            self.loading = true;
            // self.$axios.post('http://localhost:8080/server/generateByPhoto', formData)
            self.$axios.post('/server/generateByPhoto', formData)
              .then(res => {
                console.log(res.data);
                self.captions.splice(0, self.captions.length);
                for(let i = 0; i < res.data.captions.length; i++){
                  self.captions.push({'value':res.data.captions[i]})
                }
                self.loading = false;
                self.$notify({
                  title:'success',
                  message:'finished',
                  type:'success'
                });
                self.clickable = true;
                console.log(self.captions)
              })
              .catch(err => {
                console.log(err);
                self.loading = false;
                self.$notify({
                  type:"error",
                  message:'network error',
                  title:'failed'
                })
              })
          },
        submit(){
            this.loading = true;
            this.$refs.generate.submit()
        },
        clearFiles(){
            this.captions.splice(0, this.captions.length);
            this.$refs.generate.clearFiles();
            this.clickable = false;
        },
        checkEmpty(file, fileList){
            if(fileList.length > 0){
              this.clickable = true;
            }
        },
        handleRemove(file, fileList){
            this.clearFiles();
        }
      }
    }
</script>

<style scoped>
  .el-main {
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
