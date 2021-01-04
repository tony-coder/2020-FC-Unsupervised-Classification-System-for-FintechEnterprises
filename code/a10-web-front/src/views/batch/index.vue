<template>
  <el-container>
    <el-header height="54px"></el-header>
    <el-main>
      <el-row>
        <div class="search-box">
          <el-upload
            class="upload-demo"
            drag
            action="https://jsonplaceholder.typicode.com/posts/"
            multiple
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              将文件拖到此处，或
              <em>点击上传</em>
            </div>
            <div class="el-upload__tip" slot="tip">下载Excel示例文件并填充企业名录信息上传文件不超过2M，仅支持Excel（xls、xlsx）文件VIP单次免费查询数量为200家，超过需使用增值服务</div>
          </el-upload>
        </div>
      </el-row>
    </el-main>
    <my-footer></my-footer>
  </el-container>
</template>

<script>
export default {}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.search-box {
  min-width: 1200px;
  height: 520px;
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
}
</style>