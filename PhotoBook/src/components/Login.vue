<template>
  <div>
    <el-card class="my-header">
        <i class="el-icon-loading"></i>
        <h2>MY PHOTOBOOK</h2>
        <i class="el-icon-loading"></i>
    </el-card>
    <el-card class="my-main">
          <el-form label-position="right" label-width="50%">
            <el-form-item
              label="Play Photos With MY PhotoBOOK"
              label-width="80%"
              class="my-label">
            </el-form-item>
            <el-form-item label="UserID">
              <el-input placeholder="Please Input Your ID" clearable v-model="username"></el-input>
            </el-form-item>
            <el-form-item label="Password">
              <el-input placeholder="password" v-model="password" show-password></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" round @click="login" v-loading.fullscreen.lock="loading">Login</el-button>
            </el-form-item>
            <el-form-item>
              <router-link to="/register">Click To Register</router-link>
            </el-form-item>
          </el-form>
    </el-card>
  </div>
</template>

<script>
  import ElCard from "element-ui/packages/card/src/main";
  export default {
    name: "Login",
    components: {ElCard},
    data() {
      return {
        username:'',
        password:'',
        loading:false
      }
    },
    methods:{
      login(){
        let self = this;
        self.loading = true;
        // self.$axios.post('http://localhost:8080/server/login', {"username":self.username, "password":self.password})
        self.$axios.post('/server/login', {"username":self.username, "password":self.password})
          .then(res => {
            if(res.data === 'success'){
              self.$router.push({
                path: '/home/photoWall',
                query:{
                  username: self.username
                }
              });
            }
            else{
              self.$notify({
                title:'error',
                type:'error',
                message:res.data
              })
            }
            self.loading = false;
          })
          .catch(err => {
            console.log(err);
            self.$notify({
              title:'error',
              message:'network error',
              type:'error'
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
    /*background-image: url("../assets/pure.jpg");*/
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

  .my-main{
    /*background-image: url("../assets/pure.jpg");*/
    height: 80%;
  }

  .my-header{
    height: 20%;
  }
</style>
