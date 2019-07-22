<template>
    <div>
      <el-row>
        <el-col :span="12"></el-col>
        <el-col :span="12"></el-col>
      </el-row>
      <el-container>
        <el-main>
            <el-form label-position="right">
              <el-form-item>
                <el-upload
                  drag
                  ref="upload"
                  action="http://localhost:8080/server"
                  :auto-upload="false"
                  :http-request="myUpload"
                  :on-remove="handleRemove"
                  :on-change="checkEmpty"
                list-type="picture"
                multiple>
                  <i class="el-icon-upload"></i>
                  <div>Drag Files Here Or Just Click.</div>
                </el-upload>
              </el-form-item>
              <!--<el-form-item>-->
                <!--<el-input maxlength="140" placeholder="Give Some Notes About Your Photo." v-model="userCaption"></el-input>-->
              <!--</el-form-item>-->
            </el-form>
            <el-form inline>
              <el-form-item label="pick or create a category for your picture(s)">
                <el-select v-model="userClass"
                           filterable
                           allow-create
                >
                  <!--v-on:focus="getCategories"-->
                  <el-option
                    maxlength="10"
                    v-for="item in categories"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary"
                           @click="uploadClicked"
                           :disabled="!clickable"
                           v-loading.fullscreen.lock="loading">Upload</el-button>
              </el-form-item>
            </el-form>
        </el-main>
      </el-container>
    </div>
</template>

<script>
    import ElCard from "element-ui/packages/card/src/main";
    import Classify from "./Classify.vue"
    export default {
      name: "HomePage",
      components: {ElCard, Classify},
      data(){
        return {
          // userCaption:'',
          userClass:'default',
          categories:[],
          clickable:false,
          loading:false
        }
      },
      beforeMount(){
        this.username = this.$route.query.username;
        this.getCategories()
      },
      methods:{
        myUpload(file){
          let self = this;
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
          let formData = new FormData();
          formData.append('username', self.username);
          formData.append('file', file.file);
          formData.append('userClass', self.userClass);
          let temp = [];
          for(let item in self.categories){
            temp.push(item.value)
          }
          console.log('sending');
          // this.$axios.post('http://localhost:8080/server/server/upload', formData)
          this.$axios.post('/server/upload', formData)
            .then(res => {
              if(res.data.result === 'success'){
                if(self.userClass !== '' && temp.indexOf(self.userClass) < 0){
                  self.categories.push({'value':self.userClass, 'label':self.userClass})
                }
                self.$notify({
                  type:'success',
                  message:'uploaded successfully!',
                  title:'success'
                });
                self.$bus.$emit('upload', res.data)
              }
              else{
                self.$notify({
                  title:'failed',
                  type:'error',
                  message:res.data
                })
              }
              self.$refs.upload.clearFiles();
              this.loading = false;
            })
            .catch(err => {
              console.log('failed');
              console.log(err);
              this.loading = false;
              this.$refs.upload.clearFiles();
              this.$notify({
                type:'error',
                title:'network error!',
                message:'failed to finish uploading'
              })
            });
          return true;
        },
        uploadClicked(){
            this.loading = true;
            this.$refs.upload.submit()
        },
        checkEmpty(file, fileList){
          if(fileList.length > 0) {
            this.clickable = true;
          }
        },
        handleRemove(file,fileList){
          if(fileList.length <= 0){
            this.clickable = false;
          }
        },
        getCategories(){
          let self = this;
          console.log('userClass is ' + self.userClass);
          // this.$axios.get('http://localhost:8080/server/getCategories',{params:{'username': self.username}})
          this.$axios.get('/server/getCategories',{params:{'username': self.username}})
            .then(res => {
              console.log(res.data);
              self.categories.splice(0, self.categories.length);
              for(let i = 0; i < res.data.length; i++){
                self.categories.push({'value':res.data[i], 'label':res.data[i]});
              }

            })
            .catch(err => {
              console.log(err);
              self.$notify({
                title:'Error!',
                Message:'Failed to get categories',
                type:'error'
              })
            })
        }
      }
    }
</script>

<style scoped>
  .el-main {
    /*background-color: #E9EEF3;*/
    /*background-image: url("../assets/timg.jpg");*/

    /*color: #333;*/
    text-align: center;
    /*line-height: 160px;*/
    height: 580px;
    margin: 0;
  }

  .el-form{
    margin-left: 30%;
    margin-right: 30%;
  }
</style>
