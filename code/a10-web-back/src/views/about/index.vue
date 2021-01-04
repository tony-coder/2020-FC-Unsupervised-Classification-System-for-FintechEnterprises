<template>
  <div class="app-container">
    <el-card class="box-card">
      <div slot="header" style="text-align : center">
        {{ documentation }}
      </div>
      <div style="text-align : center">
        <p>服务外包创新创业大赛 测试版本v1.0</p>
        <p>前端：小鲍</p>
        <p>后端：小程</p>
        <p>算法：小陈</p>
      </div>
    </el-card>
  </div>
</template>
<script>
// import '@/assets/custom-theme/index.css' // the theme changed version element-ui css

export default {
  data() {
    return {
      documentation: 'e企查'
    }
  }
}
</script>

<style scoped>
.field-label{
  vertical-align: middle;
}
.box-card {
  width: 400px;
  max-width: 100%;
  margin: 20px auto;
}

.block {
  padding: 30px 24px;
}

.tag-item {
  margin-right: 15px;
}
</style>
