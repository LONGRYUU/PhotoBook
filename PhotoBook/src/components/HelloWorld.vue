<template>
  <div>
    <el-timeline :reverse="reverse">
      <el-timeline-item :timestamp="time" placement="top" v-for="(time,index) in timestamps">
        <el-row>
          <el-col :span="8" v-for="image in images[index]">
            <el-card>
              <el-row>
                <img :src="url + image.fileName" :alt="image.fileName">
              </el-row>
              <el-row>
                <el-input v-model="image.userCaption"></el-input>
              </el-row>
              <el-row style="margin-top: 3px">
                <el-col :span="16">
                  <el-select v-model="image.category"
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
                <el-col :span="4" style="margin-left: 39px">
                  <el-button type="primary" @click="modify(image)">Modify</el-button>
                </el-col>
              </el-row>
            </el-card>
          </el-col>
        </el-row>
      </el-timeline-item>
    </el-timeline>
    <el-upload
      ref="upload"
      class="upload-demo"
      :on-preview="handlePreview"
      :on-remove="handleRemove"
      :before-remove="beforeRemove"
      multiple
      :limit="3"
      :http-request="myUpload"
      :on-exceed="handleExceed"
      :file-list="fileList"
      :auto-upload="false"
      action="http://192.168.1.106:8080/server/upload"
      name="file">
      <el-button size="small" type="primary">点击上传</el-button>
    </el-upload>
    <el-input v-model="tags"></el-input>
    <button @click="testClick">click here to test</button>
    <el-button @click="uploadClicked">upload</el-button>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      fileList:[],
      tags:''
    }
  },
  methods:{
    testClick(){
      this.$http.get('http://192.168.1.106:8080/server/test')
        .then(res => {
          console.log('here');
          console.log(res)
        })
        .catch(err => {
          console.log('failed');
          console.log(err)
        })
    },
    uploadClicked(){
      this.$refs.upload.submit();
    },
    myUpload(file){
      let formData = new FormData();
      // formData.append('tags', this.tags);
      formData.append('file', file.file);
      // formData.append('id','123');
      // console.log(file);
      this.$axios.post('/upload', formData)
        .then(res => {
          // console.log(formData.get('file'));
          console.log('succeed');
          console.log(res)
        })
        .catch(err => {
          console.log('failed');
          console.log(err)
        });
      return true;
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${ file.name }？`);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
