<template>
  <el-footer class="footer" height="180px">
    <el-row class="footer-row">
      <h2>e企查</h2>
      <el-row class="source-list">
        <el-col :span="3"  style="text-align: right">数据来源：</el-col>
        <el-col :span="10">
          中国大学生服务外包创新创业大赛组委会
        </el-col>
        <el-col :span="10" class="middle">
          A10-浪潮-无监督分类系统训练集-Inspur
        </el-col>
      </el-row>
    </el-row>
  </el-footer>
</template>
<script>
export default {
  name: 'myFooter',
  data() {
    return {
      centerDialogVisible: false
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.el-footer {
  background: #262626;
  min-width: 1200px;
  padding: 0 !important;
  .footer-row {
    width: 1200px;
    margin: 0 auto;
    color: #fff;
    h2 {
      font-size: 20px;
      text-align: center;
      padding: 10px 0;
      font-weight: normal;
      margin: 30px 0 20px;
    }
    .source-list {
      width: 55%;
      margin: 0 auto;
      color: #b4b4b4;
      font-size: 14px;
      text-align: center;
    }
    .middle {
      border-left: 1px solid;
      border-right: 1px solid;
    }
    .w-link {
      color: #fff;
      font-size: 14px;
    }
  }
}
</style>
