<template>
  <div>
    <el-card class="my-header">
      <i class="el-icon-loading"></i>
      <h2>MY PHOTOBOOK</h2>
      <i class="el-icon-loading"></i>
    </el-card>
    <el-card>
      <el-form label-position="right" label-width="50%">
        <el-form-item
          label="Play Photos With MY PhotoBOOK"
          label-width="80%"
          class="my-label">
        </el-form-item>
        <el-form-item label="Username">
          <el-input placeholder="Please Input Your Username" clearable v-model="username"></el-input>
        </el-form-item>
        <el-form-item label="Password">
          <el-input placeholder="password" v-model="password" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" round @click="register" v-loading.fullscreen.lock="loading">Register</el-button>
        </el-form-item>
        <el-form-item>
          <router-link to="/login">Click To Login</router-link>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
  export default {
    name: "Register",
    data() {
      return {
        username:'',
        password:'',
        loading:false
      }
    },
    methods:{
      register(){
        let self = this;
        if(self.username.match('[^a-zA-Z0-9]') || self.password.match('[^a-zA-Z0-9]')){
          self.$notify({
            title:'warning',
            message:'Only alphas and numbers are allowed.',
            type:'warning'
          });
          return true;
        }
        if(self.username ==='' || self.password ===''){
          self.$notify({
            type:'warning',
            message:'invalid username/password!',
            title:'wrong input'
          });
          self.loading = false;
          return;
        }
        self.loading = true;
        // this.$axios.post('http://localhost:8080/server/register',{'username': self.username, 'password': self.password})
        this.$axios.post('/server/register',{'username': self.username, 'password': self.password})
          .then(res => {
            if(res.data === 'success'){
              self.$notify({
                type:'success',
                message:'succeed signing in!',
                title:'result'
              })
            }else{
              self.$notify({
                title:'problem',
                message:res.data,
                type:'error'
              })
            }
            self.loading = false;
          })
          .catch(err => {
            console.log(err);
            self.$notify({
              title:'error',
              type:'error',
              message:'network error'
            });
            self.loading = false;
          })
      }
    }
  }
</script>

<style scoped>
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
    font-size: 30px;
    margin: 0;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .el-main {
    /*background-color: #E9EEF3;*/
    background-image: url("../assets/pure.jpg");
    /*color: #333;*/
    text-align: center;
    line-height: 160px;
    height: 675px;
  }

  .el-form{
    margin-right: 30%;
  }

  .my-label{
    line-height: 200px;
  }

</style>
