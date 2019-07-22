<template>
    <div>
      <el-card style="background-color: cornflowerblue">
        <el-row>
          <el-col :span="20">
            <h2>
              <span style="color: #fff;">My PhotoBook</span></h2>
          </el-col>
          <el-col :span="4">
            <div style="margin-top: 20px">
              <span style="color: #ffffff">Hello,{{username}}!</span>
              <router-link to="/login">
                <span style="color: #2c3e50">Log Out</span>
              </router-link>
            </div>
          </el-col>
        </el-row>
      </el-card>
      <!--<el-card style="background-color: #f0f2f5">-->
      <el-card style="background-color: #ffffff" shadow="never">
        <el-row>
          <el-col :span="4" >
            <el-menu @select="selected" style="background-color: #8cc5ff" text-color="#fff">
              <el-menu-item index="/home/photoWall">
                <i class="el-icon-picture-outline"></i>
                PhotoWall
              </el-menu-item>
              <el-menu-item index="/home/upload">
                <i class="el-icon-upload"></i>
                Upload
              </el-menu-item>
              <!--<el-menu-item index="/home/classify">-->
                <!--<i class="el-icon-menu"></i>-->
                <!--Classify-->
              <!--</el-menu-item>-->
              <el-menu-item index="/home/search">
                <i class="el-icon-search"></i>
                Search
              </el-menu-item>
              <!--<el-menu-item index="/home/generate">-->
                <!--<i class="el-icon-document"></i>-->
                <!--Describe-->
              <!--</el-menu-item>-->
              <el-menu-item index="/home/info">
                <i class="el-icon-info"></i>
                Information
              </el-menu-item>
            </el-menu>
          </el-col>
          <el-col :span="20">
            <keep-alive>
              <router-view></router-view>
            </keep-alive>
          </el-col>
        </el-row>
      </el-card>
    </div>
</template>

<script>
  import HomePage from './Upload'
  import Classify from './Classify'
  import Generate from './Generate'
  import Search from './Search'
  import ElCard from "element-ui/packages/card/src/main";
    export default {
      components:{
        ElCard,
        HomePage,
        Classify,
        Generate,
        Search
      },
      data() {
          return {
            paths:[],
            username: '456'
          }
      },
      beforeMount() {
        this.username = this.$route.query.username;
        if(this.username === ''){
          this.$router.push('/login')
        }
        console.log(this.username)
      },
      methods:{
        selected(index, indexPath){
          let self = this;
          console.log(self.username);
          this.$router.push({
            path:index,
            query:{
              username:self.username
            }
          })
        }
      }
    }
</script>

<style scoped>
.el-tabs{
  margin: 0;
}
  .el-tab-pane{
    margin: 0;

  }

  .my-row{
    /*background-color: #409eff;*/
    height: 30px;
    margin: 0;
  }
  .el-menu-item{
    font-size: 18px;
    font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,SimSun,sans-serif;

  }
</style>
