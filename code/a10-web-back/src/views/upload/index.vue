<template>
  <div class="dashboard-editor-container">
    <div style="margin-bottom:20px;">
      <h2>
        <strong>上传数据</strong>
      </h2>
      <small>上传数据到服务器</small>
    </div>
    <!-- <el-row>
      <uploader />
    </el-row> -->
    <el-row style="margin-bottom:300px">
      <el-col :span="12">
        <el-upload
          ref="upload"
          class="upload-demo"
          action="/api/api/bfx/upload/train"
          :on-success="handlesuccess"
          :before-upload="beforeUpload"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :file-list="fileList"
          :auto-upload="false"
        >
          <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
          <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
          <div slot="tip" class="el-upload__tip">只能上传.zip文件，且不超过100Mb</div>
        </el-upload>
      </el-col>
    </el-row>
    <!-- <el-row>
      <el-button type="primary">开始训练模型</el-button>
    </el-row> -->
  </div>
</template>

<script>
// import uploader from '@/components/Upload/globalUploader'
export default {
  components: {
    // uploader
  },
  data() {
    return {

    }
  },
  methods: {
    submitUpload() {
      this.$refs.upload.submit()
    },
    handleRemove(file, fileList) {
      console.log(file, fileList)
    },
    handlePreview(file) {
      console.log(file)
    },
    handlesuccess(response, file, fileList) {
      if (response.data.message === '上传成功') {
        this.istrain = true
        this.$notify({
          title: '成功',
          message: response.data.message,
          type: 'success'
        })
      } else {
        this.istrain = false
        this.$notify.error({
          title: '错误',
          message: response.data.message
        })
      }
    },
    beforeUpload(file) {
      console.log(file.type)
      const is_ZIP = file.type === 'application/x-zip-compressed'
      if (!is_ZIP) {
        this.$message.error('上传文件只能是 zip 格式!')
        return false
      }
      const isLt1M = file.size / 1024 / 1024 < 100
      if (isLt1M) {
        return true
      }
      this.$message({
        message: '文件大小不能超过 100Mb!',
        type: 'warning'
      })
      return false
    }
  }
}
</script>
<style lang="scss" scoped>
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
