<template>
  <div class="animated fadeIn">
    <el-row class="left-row left-row-info">
      <el-row class="info-title">评分</el-row>
      <el-col :span="2">t</el-col>
      <el-col :span="22">
        <el-rate
          v-model="tagRank.creditScore"
          disabled
          show-score
          text-color="#ff9900"
          score-template="{value}"
        ></el-rate>
      </el-col>
    </el-row>
    <!-- 企业信用 -->
    <el-row class="left-row left-row-info" id="qyxy">
      <el-row class="info-title">企业信用</el-row>
      <el-col :span="12" class="info-text">
        守合同重信用企业次数：
        <span>{{creditinfo.is_kcont | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        企业信用评级：
        <span>{{creditinfo.credit_grade | showLine}}</span>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { searchCreditInfo } from '@/api/detail/creditInfo'
import { showLine } from '@/filters'
import { showTableCellLine } from '@/utils'

export default {
  // 通过 Prop 向子组件传递数据
  props: {
    id: '',
    tagRank: {}
  },
  data() {
    return {
      creditinfo: {
        is_kcont: undefined,
        credit_grade: undefined,
        id: null
      },
      showTableCellLine: showTableCellLine
    }
  },
  filters: {
    showLine
  },
  mounted() {
    this.initCreditinfo()
  },
  methods: {
    initCreditinfo() {
      this.creditinfo.id = this.id
      searchCreditInfo(this.creditinfo).then(resp => {
        this.creditinfo.is_kcont = resp.is_kcont
        this.creditinfo.credit_grade = resp.credit_grade
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.no-data {
  text-align: center;
  color: #999;
  line-height: 120px;
  font-size: 12px;
}
.left-col {
  padding: 0 !important;
  .left-row-info {
    padding: 20px 0;
    .info-title {
      border-left: 3px solid #3a71d8;
      margin-bottom: 10px;
      font-size: 16px;
      color: #000;
      font-weight: normal;
      text-indent: 15px;
      padding-left: 20px;
    }
    .dataList-row {
      padding: 10px 20px;
      .el-table {
        border: 1px solid rgba(242, 242, 242, 1);
        border-bottom: none;
        font-size: 12px;
      }
    }
    .el-card {
      padding: 20px;
      margin-bottom: 15px;
      .sb-logo {
        height: 82px;
        width: 82px;
        border-radius: 50%;
        vertical-align: middle;
        border: 1px solid #e2e6e9;
      }
      .sb-text {
        font-size: 14px;
        margin: 6px;
        span {
          color: #999;
        }
      }
    }
    .page-row {
      text-align: center;
      margin: 20px;
    }
    .bg-row {
      margin: 20px;
      .thead {
        font-weight: bold;
        font-family: "Arial";
        color: #3a71d8;
        line-height: 18px;
        font-size: 12px;
        .xh {
          border: 1px solid #3a71d8;
          border-radius: 50%;
          min-height: 16px;
          min-width: 16px;
          display: block;
          text-align: center;
          line-height: 16px;
          float: left;
        }
        .time {
          margin-left: 10px;
        }
        .time:after {
          content: "";
          width: 80%;
          height: 1px;
          background: #e2e2e2;
          display: block;
          position: absolute;
          top: 0px;
          bottom: 0px;
          margin: auto;
          left: 140px;
        }
      }
      .bg-item {
        font-size: 14px;
        color: #000;
        margin-top: 20px;
        span {
          color: #999;
        }
        .el-col {
          margin-bottom: 10px;
        }
      }
    }
  }
  .left-row {
    width: 100%;
    background: #ffffff;
    margin-bottom: 20px;
    border: 1px solid rgba(242, 242, 242, 1);
    .info-text {
      color: #999;
      font-size: 14px;
      padding: 8px 20px;
      span {
        color: #000;
      }
    }
  }
}
</style>
