<template>
  <div class="animated fadeIn">
    <el-row class="left-row left-row-info">
      <el-row class="info-title">评分</el-row>
      <el-col :span="2">&nbsp;</el-col>
      <el-col :span="22">
        <!-- <el-rate v-model="value"
          :icon-classes="iconClasses"
          void-icon-class="icon-rate-face-off"
          :colors="['#99A9BF', '#F7BA2A', '#FF9900']">
        </el-rate> -->
        <el-rate
          v-model="riskScore"
          disabled
          show-score
          text-color="#ff9900"
          score-template="{value}"
        ></el-rate>
      </el-col>
    </el-row>
    <el-row id="cfjl" class="left-row left-row-info">
      <el-row class="info-title">处罚记录</el-row>
      <el-col :span="12" class="info-text">
        公司行政处罚次数：
        <span>{{punishment.is_punish | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        经营异常次数：
        <span>{{punishment.is_bra | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        行政处罚记录次数：
        <span>{{punishment.is_brap | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        异常次数：
        <span>{{punishment.is_except | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        股权出质次数：
        <span>{{punishment.equity_pledge | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        列入失信黑名单次数：
        <span>{{punishment.is_justice_credit | showLine}}</span>
      </el-col>
      <el-col :span="12" class="info-text">
        列入工商部失信企业次数：
        <span>{{punishment.is_justice_creditaic | showLine}}</span>
      </el-col>
    </el-row>
    <el-row id="glqk" class="left-row left-row-info">
      <el-row class="info-title">各类欠款</el-row>
      <el-row class="dataList-row">
        <el-table
          :data="overdraft.data"
          v-loading="overdraft.fullscreenLoading"
          style="width: 100%"
          empty-text="暂无欠款记录"
        >
          <el-table-column
            width="90"
            prop
            label="序号"
            type="index"
            align="center"
            :index="1 + (overdraft.page - 1) * overdraft.row"
          ></el-table-column>
          <el-table-column width="120" prop="unpaidsocialins_so110" label="单位参加城镇职工基本养老保险累计欠缴金额">
            <template slot-scope="scope">
              <span>{{ scope.row.unpaidsocialins_so110 | showLine }}</span>
            </template>
          </el-table-column>
          <el-table-column width="120" prop="unpaidsocialins_so210" label="单位参加失业保险累计欠缴金额">
            <template slot-scope="scope">
              <span>{{ scope.row.unpaidsocialins_so110 | showLine }}</span>
            </template>
          </el-table-column>
          <el-table-column width="120" prop="unpaidsocialins_so310" label="单位参加职工基本医疗保险累计欠缴金额">
            <template slot-scope="scope">
              <span>{{ scope.row.unpaidsocialins_so310 | showLine }}</span>
            </template>
          </el-table-column>
          <el-table-column width="120" prop="unpaidsocialins_so410" label="单位参加工伤保险累计欠缴金额">
            <template slot-scope="scope">
              <span>{{ scope.row.unpaidsocialins_so310 | showLine }}</span>
            </template>
          </el-table-column>
          <el-table-column width="120" prop="unpaidsocialins_so510" label="单位参加生育保险累计欠缴金额">
            <template slot-scope="scope">
              <span>{{ scope.row.unpaidsocialins_so510 | showLine }}</span>
            </template>
          </el-table-column>
          <el-table-column width="115" prop="updatetime" label="更新时间">
            <template slot-scope="scope">
              <span>{{ scope.row.updatetime | showTime }}</span>
            </template>
          </el-table-column>
        </el-table>
        <el-row class="page-row" v-show="overdraft.total > overdraft.row">
          <el-pagination
            :current-page="overdraft.page"
            background
            :page-size="overdraft.row"
            layout="prev, pager, next, jumper"
            @current-change="handleCurrentChangeOverdraft"
            :total="overdraft.total"
          ></el-pagination>
        </el-row>
      </el-row>
    </el-row>
    <el-row id="sfjf" class="left-row left-row-info">
      <el-row class="info-title">司法纠纷</el-row>
      <el-row class="dataList-row">
        <el-table
          :data="judicialDispute.data"
          v-loading="judicialDispute.fullscreenLoading"
          style="width: 100%"
          empty-text="暂无司法纠纷信息"
        >
          <el-table-column
            prop
            label="序号"
            type="index"
            align="center"
            :index="1 + (judicialDispute.page - 1) * judicialDispute.row"
          ></el-table-column>
          <el-table-column prop="declaredate" label="公示日期">
            <template slot-scope="scope">
              <span>{{ scope.row.declaredate | showTime }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="appellant" label="上诉方">
            <template slot-scope="scope">
              <span>{{ scope.row.appellant | showLine }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="defendant" label="被诉方">
            <template slot-scope="scope">
              <span>{{ scope.row.defendant | showLine}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="declarestyle" label="公告类型">
            <template slot-scope="scope">
              <span>{{ scope.row.declarestyle | showLine }}</span>
            </template>
          </el-table-column>
        </el-table>
        <el-row class="page-row" v-show="judicialDispute.total > judicialDispute.row">
          <el-pagination
            :current-page="judicialDispute.page"
            background
            :page-size="judicialDispute.row"
            layout="prev, pager, next, jumper"
            @current-change="handleCurrentChangeJudicialDispute"
            :total="judicialDispute.total"
          ></el-pagination>
        </el-row>
      </el-row>
    </el-row>
  </div>
</template>

<script>
import {
  punishmentFind,
  overdraftFind,
  judicialDisputeFind
} from '@/api/detail/businessRisk'
import { showLine, showTime } from '@/filters'

export default {
  name: 'businessRisk',
  props: {
    id: '',
    tagRank: {}
  },
  data() {
    return {
      // 处罚
      punishment: {
        is_punish: undefined,
        is_bra: undefined,
        is_brap: undefined,
        is_except: undefined,
        equity_pledge: undefined,
        is_justice_credit: undefined,
        is_justice_creditaic: undefined,
        id: null
      },
      // 各类欠款
      overdraft: {
        page: 1,
        row: 5,
        data: null,
        total: undefined,
        fullscreenLoading: false, // v-loading
        id: null
      },
      // 司法纠纷
      judicialDispute: {
        page: 1,
        row: 5,
        data: null,
        total: undefined,
        fullscreenLoading: false,
        id: null
      },
      value: 3,
      loading: false,
      iconClasses: ['icon-rate-face-1', 'icon-rate-face-2', 'icon-rate-face-3'], // 等同于 { 2: 'icon-rate-face-1', 4: { value: 'icon-rate-face-2', excluded: true }, 5: 'icon-rate-face-3' }
      riskScore: 0
    }
  },
  filters: {
    showLine,
    showTime
  },
  mounted() {
    this.handlePunishment()
    this.handleOverdraft()
    this.handleJudicialDispute()
    if (this.tagRank.riskScore !== 0) { this.riskScore = 5.0 - this.tagRank.riskScore }
  },
  methods: {
    // 获取处罚数据
    handlePunishment() {
      this.punishment.id = this.id
      this.loading = true
      punishmentFind(this.punishment).then(resp => {
        this.punishment.is_punish = resp.is_punish
        this.punishment.is_bra = resp.is_bra
        this.punishment.is_brap = resp.is_brap
        this.punishment.is_except = resp.is_except
        this.punishment.equity_pledge = resp.equity_pledge
        this.punishment.is_justice_credit = resp.is_justice_credit
        this.punishment.is_justice_creditaic = resp.is_justice_creditaic
      })
    },
    // 获取欠款数据
    handleOverdraft() {
      this.overdraft.id = this.id
      this.overdraft.fullscreenLoading = true
      overdraftFind(this.overdraft).then(resp => {
        this.overdraft.data = resp.data
        this.overdraft.total = resp.total
        setTimeout(() => {
          this.overdraft.fullscreenLoading = false
        }, 0.5 * 1000)
      })
    },
    // 获取司法纠纷数据
    handleJudicialDispute() {
      this.judicialDispute.id = this.id
      this.judicialDispute.fullscreenLoading = true
      judicialDisputeFind(this.judicialDispute).then(resp => {
        this.judicialDispute.data = resp.data
        this.judicialDispute.total = resp.total
        setTimeout(() => {
          this.judicialDispute.fullscreenLoading = false
        }, 0.5 * 1000)
      })
    },
    // 分页
    handleCurrentChangeOverdraft(val) {
      this.overdraft.fullscreenLoading = true
      this.overdraft.page = val
      this.overdraft.data = null
      this.handleOverdraft()
      setTimeout(() => {
        this.overdraft.fullscreenLoading = false
      }, 1000)
    },
    handleCurrentChangeJudicialDispute(val) {
      this.judicialDispute.fullscreenLoading = true
      this.judicialDispute.page = val
      this.judicialDispute.data = null
      this.handleJudicialDispute()
      setTimeout(() => {
        this.judicialDispute.fullscreenLoading = false
      }, 1000)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
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
        text-align: center;
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
          height: 16px;
          width: 16px;
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
          width: 87%;
          height: 1px;
          background: #e2e2e2;
          display: block;
          position: absolute;
          top: 0px;
          bottom: 0px;
          margin: auto;
          left: 100px;
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
