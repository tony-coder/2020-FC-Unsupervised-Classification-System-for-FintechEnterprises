<template>
  <div>
    <uploader
      :key="uploader_key"
      :options="options"
      class="uploader-example"
      @file-success="onFileSuccess"
    >
      <uploader-unsupport />
      <uploader-drop>
        <uploader-btn :directory="false" :single="true">选择测试文件</uploader-btn>
      </uploader-drop>
      <uploader-list />
    </uploader>
  </div>
</template>

<script>
export default {
  props: {
    url: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      uploader_key: new Date().getTime(), // 这个用来刷新组件--解决不刷新页面连续上传的缓存上传数据（注：每次上传时，强制这个值进行更改---根据自己的实际情况重新赋值）
      options: {
        target: this.url, // 后台接收文件夹数据的接口
        testChunks: false// 是否分片-不分片
      }
    }
  },
  methods: {
    onFileSuccess: function(rootFile, file, response, chunk) {
      // 这里可以根据response（接口）返回的数据处理自己的实际问题（如：从response拿到后台返回的想要的数据进行组装并显示）
      // 注，这里从文件夹每上传成功一个文件会调用一次这个方法
      if (response.data.message === '上传成功') {
        this.$emit('fun', true)
        this.$notify({
          title: '成功',
          message: response.data.message,
          type: 'success'
        })
      } else {
        this.$emit('fun', false)
        this.$notify.error({
          title: '错误',
          message: response.data.message
        })
      }
    }
  }
}
</script>

<style>
  .uploader-example {
    width: 90%;
    padding: 15px;
    margin: 10px auto 0;
    font-size: 12px;
    box-shadow: 0 0 10px rgba(0, 0, 0, .4);
  }

  .uploader-example .uploader-btn {
    margin-right: 4px;
  }

  .uploader-example .uploader-list {
    max-height: 440px;
    overflow: auto;
    overflow-x: hidden;
    overflow-y: auto;
  }
</style>
