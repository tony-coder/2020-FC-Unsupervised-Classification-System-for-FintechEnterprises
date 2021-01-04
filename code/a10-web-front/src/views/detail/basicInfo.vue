<template>
  <div class="animated fadeIn">
    <!-- 工商信息 -->
    <el-row class="left-row left-row-info" id="gsxx">
      <el-row class="info-title">工商信息</el-row>
      <el-col :span="12" class="info-text">
        工商注册号：
        <span>{{basicInfo.registrationCode | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        法定代表人：
        <span>{{basicInfo.legalRepresentative | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        经营状态：
        <span>{{basicInfo.registrationStatus | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        核准日期：
        <span>{{basicInfo.issueDate | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        公司类型：
        <span>{{basicInfo.type | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        注册资本：
        <span>{{basicInfo.registeredCapital | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        成立日期：
        <span>{{basicInfo.dateOfEstablishment | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        注销时间：
        <span>{{basicInfo.dateOfLetout | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        营业期限自：
        <span>{{basicInfo.businessTermStart | showLine}}</span>
      </el-col>
      <!-- <el-col :span="12" class="info-text">
        工商注册号：
        <span>{{basicInfo.registrationCode | showLine}}</span>
      </el-col>-->
      <el-col :span="12" class="info-text">
        营业期限至：
        <span>{{basicInfo.businessTermEnd | showLine}}</span>
      </el-col>
      <el-col :span="24" class="info-text">
        企业地址：
        <span>{{basicInfo.residence | showLine}}</span>
      </el-col>
      <el-col :span="24" class="info-text">
        经营范围：
        <span>{{basicInfo.scopeOfBusiness | showLine}}</span>
        <!--<div style="margin-top: 8px" class="text-justify"></div>-->
      </el-col>
    </el-row>
    <!-- 推荐企业 -->
    <el-row class="left-row left-row-info" id="tjqy">
      <el-row class="info-title">相似企业推荐</el-row>
      <el-card
        class="list-card animated fadeInLeft"
        shadow="never"
        v-loading="recommandEnt.loading"
      >
        <el-card shadow="never">
        <div slot="header" class="result-title">
          <span>公司名称</span>
          <el-col :span="3" style="float:right;text-align: center">状态</el-col>
        </div>
          <el-row class="result-list" v-for="item in recommandEnt.data" :key="item.id">
            <!-- 点击进入企业详情 -->
            <div @click="showDetailPage(item.id)">
              <!-- 企业照片 默认 -->
              <el-col :span="5" class="company-img">
                <img src="../../assets/index/list-img.png" />
              </el-col>
              <el-col :span="11" class="company-content">
                <el-row>
                  <h2>{{item.enterpriseName | showLine}}</h2>
                </el-row>
                <!-- 标签 -->
                <el-row >
                  <!-- 风险 -->
                  <el-col :span="5" class="bj-img2" v-if="item.riskRank==10">
                    <el-tag type="danger">极高风险</el-tag>
                  </el-col>
                  <el-col :span="5" class="bj-img2" v-if="item.riskRank>=7 && item.riskRank<=9">
                    <el-tag type="warning">高风险</el-tag>
                  </el-col>
                  <el-col :span="5" class="bj-img2" v-if="item.riskRank>=4 && item.riskRank<=6">
                    <el-tag type="info">中等风险</el-tag>
                  </el-col>
                  <el-col :span="5" class="bj-img2" v-if="item.riskRank!=null && item.riskRank<=2 && item.riskRank>0">
                    <el-tag type="success">低风险</el-tag>
                  </el-col>
                  <!-- 投资水平 -->
                  <el-col :span="6" class="bj-img2" v-if="item.investmentRank!=null && item.investmentRank<=3 && item.investmentRank>0">
                    <el-tag type="danger">低投资水平</el-tag>
                  </el-col>
                  <el-col :span="7" class="bj-img2" v-if="item.investmentRank>=4 && item.investmentRank<=6">
                    <el-tag type="warning">中等投资水平</el-tag>
                  </el-col>
                  <el-col :span="6" class="bj-img2" v-if="item.investmentRank>=7 && item.investmentRank<=9">
                    <el-tag type="info">高投资水平</el-tag>
                  </el-col>
                  <el-col :span="7" class="bj-img2" v-if="item.investmentRank==10">
                    <el-tag type="success">极高投资水平</el-tag>
                  </el-col>
                  <!-- 创新水平 -->
                  <el-col :span="6" class="bj-img2" v-if="item.creativityRank!=null && item.creativityRank<=3 && item.creativityRank>0">
                    <el-tag type="danger">低创新水平</el-tag>
                  </el-col>
                  <el-col :span="7" class="bj-img2" v-if="item.creativityRank>=4 && item.creativityRank<=6">
                    <el-tag type="warning">中等创新水平</el-tag>
                  </el-col>
                  <el-col :span="6" class="bj-img2" v-if="item.creativityRank>=6 && item.creativityRank<=9">
                    <el-tag type="info">高创新水平</el-tag>
                  </el-col>
                  <el-col :span="7" class="bj-img2" v-if="item.creativityRank==10">
                    <el-tag type="success">极高创新水平</el-tag>
                  </el-col>
                  <!-- 品牌水平 -->
                  <el-col :span="6" class="bj-img2" v-if="item.brandRank!=null && item.brandRank<=3 && item.brandRank>0">
                    <el-tag type="danger">低品牌水平</el-tag>
                  </el-col>
                  <el-col :span="7" class="bj-img2" v-if="item.brandRank>=4 && item.brandRank<=6">
                    <el-tag type="warning">中等品牌水平</el-tag>
                  </el-col>
                  <el-col :span="6" class="bj-img2" v-if="item.brandRank>=7 && item.brandRank<=9">
                    <el-tag type="info">高品牌水平</el-tag>
                  </el-col>
                  <el-col :span="7" class="bj-img2" v-if="item.brandRank==10">
                    <el-tag type="success">极高品牌水平</el-tag>
                  </el-col>
                  <!-- 用人需求 -->
                  <el-col :span="6" class="bj-img2" v-if="item.recruitRank!=null && item.recruitRank<=3 && item.recruitRank>0">
                    <el-tag type="danger">低用人需求</el-tag>
                  </el-col>
                  <el-col :span="7" class="bj-img2" v-if="item.recruitRank>=4 && item.recruitRank<=6">
                    <el-tag type="warning">中等用人需求</el-tag>
                  </el-col>
                  <el-col :span="6" class="bj-img2" v-if="item.recruitRank>=7 && item.recruitRank<=9">
                    <el-tag type="info">高用人需求</el-tag>
                  </el-col>
                  <el-col :span="7" class="bj-img2" v-if="item.recruitRank==10">
                    <el-tag type="success">极高用人需求</el-tag>
                  </el-col>
                  <!-- 信用 -->
                  <el-col :span="5" class="bj-img2" v-if="item.creditRank!=null && item.creditRank<=3 && item.creditRank>0">
                    <el-tag type="danger">低信用</el-tag>
                  </el-col>
                  <el-col :span="5" class="bj-img2" v-if="item.creditRank>=4 && item.creditRank<=6">
                    <el-tag type="warning">中等信用</el-tag>
                  </el-col>
                  <el-col :span="5" class="bj-img2" v-if="item.creditRank>=7 && item.creditRank<=9">
                    <el-tag type="info">高信用</el-tag>
                  </el-col>
                  <el-col :span="5" class="bj-img2" v-if="item.creditRank==10">
                    <el-tag type="success">极高信用</el-tag>
                  </el-col>
                </el-row>
                <el-row>
                  <span>
                    法人代表：
                    <span>{{item.legalRepresentative | showLine}}</span>
                  </span>
                </el-row>
                <el-row>
                  <el-col :span="12">
                    <span>
                      注册资本：{{item.registeredCapital | showLine}}
                      <span
                        v-if="item.registeredCapital"
                      >万人民币</span>
                    </span>
                  </el-col>
                  <el-col :span="12">
                    <span>
                      电话：
                      <span>{{item.phoneNumber | showLine}}</span>
                    </span>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="12">
                    <span>成立时间：{{item.dateOfEstablishment | showLine}}</span>
                  </el-col>
                  <el-col :span="12">
                    <span>
                      邮箱：
                      <span>{{item.email | showLine}}</span>
                    </span>
                  </el-col>
                </el-row>
                <el-row>
                  <span>地址：{{item.address | showLine}}</span>
                </el-row>
              </el-col>
              <el-col :span="7">
                <RaddarChart
                v-bind:tagRankList=item.tagRankList
                v-bind:enterpriseName=item.enterpriseName
                >
                </RaddarChart>
              </el-col>
            </div>
          </el-row>
        <el-row v-if="recommandEnt.totalNumber===0" class="result-list">
          <div class="no-data">没有推荐企业</div>
        </el-row>
      </el-card>
      </el-card>
       <el-row class="page-row" v-show="recommandEnt.totalNumber>recommandEnt.rows">
        <!-- Pagination 分页 当数据量过多时，使用分页分解数据 https://element.eleme.cn/#/zh-CN/component/pagination-->
        <el-pagination
          :current-page="recommandEnt.page"
          background
          small="small"
          :page-size="recommandEnt.rows"
          layout="prev, pager, next"
          @current-change="handleRecommandCurrentChange"
          :total="recommandEnt.totalNumber"
        ></el-pagination>
      </el-row>

      <!-- <el-row class="dataList-row">
        <el-table
          :data="recommandEnt.data"
          style="width: 100%"
          v-loading="recommandEnt.loading"
          empty-text="暂无推荐企业"
          @selection-change="handleSelectionChange">
        >
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column
            type="index"
            label="序号"
            width="249px;"
            :index="1 + (recommandEnt.page - 1) * recommandEnt.rows"
          ></el-table-column>
          <el-table-column prop="entname" label="企业名" width="270px;" :formatter="showTableCellLine"></el-table-column>
          <el-table-column prop="type" label="公司类型" width="270px;" :formatter="showTableCellLine"></el-table-column>
        </el-table>
        <el-row class="page-row" v-if="recommandEnt.totalNumber>recommandEnt.rows">
          <el-pagination
            :current-page="recommandEnt.page"
            background
            :page-size="recommandEnt.rows"
            layout="prev, pager, next, jumper"
            @current-change="handleRecommandCurrentChange"
            :total="recommandEnt.totalNumber"
          ></el-pagination>
        </el-row>
      </el-row> -->
    </el-row>
  </div>
</template>

<script>
import basicInfo from '@/api/detail/basicInfo'
import { showLine } from '@/filters'
import { showTableCellLine } from '@/utils'
import RaddarChart from '@/views/list/RaddarChart'

export default {
  // 通过 Prop 向子组件传递数据
  props: {
    id: '',
    basicInfo: {}
  },
  components: {
    RaddarChart
  },
  data() {
    return {
      recommandEnt: {
        page: 1,
        rows: 5,
        totalNumber: undefined,
        data: [],
        loading: false
      },
      showTableCellLine: showTableCellLine,
      multipleSelection: [],
      checkList: []
    }
  },
  filters: {
    showLine
  },
  mounted() {
    this.initRecommandEntList()
  },
  methods: {
    initRecommandEntList() {
      const data = {}
      data.page = this.recommandEnt.page
      data.rows = this.recommandEnt.rows
      data.id = this.id
      this.recommandEnt.loading = true
      basicInfo.searchRecommandEnt(data).then(resp => {
        console.log(resp)
        this.recommandEnt.data = resp.data
        this.recommandEnt.totalNumber = resp.totalNumber
        console.log(this.recommandEnt.data)
        setTimeout(() => {
          this.recommandEnt.loading = false
        }, 0.5 * 1000)
      })
    },
    handleRecommandCurrentChange(val) {
      this.recommandEnt.page = val
      this.initRecommandEntList()
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    // 企业选中处理
    handleCheckedEntChange(val) {
      // console.log(val)
      console.log(this.checkList)
    },
    // 跳转到企业详情页面
    showDetailPage(id, activeTap = 'basicInfo') {
      var location =
        window.location.origin + `/detail/${id}?activeTap=${activeTap}`
      window.open(location)
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
  .result-list {
    padding-bottom: 5px;
    border-bottom: 1px solid #e9eeef;
    .company-img {
      text-align: center;
      padding-top: 25px;
      img {
        width: 70%;
      }
    }
  }
  .list-card {
      margin-top: 20px;
      padding: 20px;
      .totla-text {
        font-size: 14px;
        color: #666;
        margin-bottom: 10px;
        margin-left: 30px;
        span {
          color: #3a71d8;
        }
      }
      .result-title {
        margin: -5px -20px -5px 10px;
      }
      .result-list {
        padding-bottom: 5px;
        border-bottom: 1px solid #e9eeef;
        .company-img {
          text-align: center;
          padding-top: 25px;
          img {
            width: 70%;
          }
        }
        .company-content {
          padding-top: 10px;
          color: #666;
          font-size: 14px;
          h2 {
            font-size: 20px;
            color: #000;
            font-weight: normal;
            margin-bottom: 4px;
            letter-spacing: 1px;
            line-height: 22px;
          }
          .el-row {
            padding: 6px 0;
          }
          .jg-col {
            /*border-left: 1px solid #666;*/
            padding-left: 15px;
          }
        }
      }
  }
}
</style>
