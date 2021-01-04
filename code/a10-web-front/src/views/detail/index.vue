<template>
  <el-container>
    <el-header height="54px">
      <my-header></my-header>
    </el-header>
    <el-main>
      <el-row class="top-row self-row">
        <div class="top-row-inner">
          <el-row>
            <el-col :span="18">
              <h2>{{basicInfo.enterpriseName}}</h2>
            </el-col>
            <el-col :span="6" style="text-align: right;">
              <el-col :span="24" style="margin-top: 10px">
                <span
                  v-if="basicInfo.registrationStatus"
                  class="cunx"
                >{{basicInfo.registrationStatus}}</span>
              </el-col>
            </el-col>
          </el-row>
          <el-row :gutter="40">
            <el-col :span="3">
              <img src="../../assets/index/list-img.png" alt class="logo" />
            </el-col>
            <el-col :span="21">
              <el-row class="inner-row1">
                <el-col :span="16">
                  企业名称：
                  <span>{{id | showLine}}</span>
                </el-col>
                <el-col :span="8" class="inner-row-text" style="text-align: right">
                  数据更新时间：
                  <span>{{basicInfo.updateDate | showLine}}</span>
                </el-col>
              </el-row>
              <el-row class="inner-row-text row-margin">
                <span>法定代表：{{basicInfo.legalRepresentative | showLine}}</span>
              </el-row>
              <el-row class="inner-row-text row-margin">
                <el-col :span="12">成立日期：{{basicInfo.dateOfEstablishment | showLine}}</el-col>
                <el-col :span="12">电话：{{basicInfo.phoneNumber | showLine}}</el-col>
              </el-row>
              <el-row class="inner-row-text row-margin">
                <el-col :span="12">登记机关：{{basicInfo.registrationAuthority | showLine}}</el-col>
                <el-col :span="12">邮箱：{{basicInfo.email | showLine}}</el-col>
              </el-row>
            </el-col>
          </el-row>
        </div>
      </el-row>
      <el-row class="bjrisk-row self-row">
        <el-col :span="3" class="bj-img">
          <img src="../../assets/index/details-bjfx.png" alt />
        </el-col>
        <el-col :span="18" style="margin-top: 15px">
          <el-rate v-model="tagRank.totScore" disabled show-score text-color="#ff9900" score-template="{value}"></el-rate>
        </el-col>
        <el-col :span="3">
          <!-- <PDF ref="pdf"></PDF> -->
          <el-button type="primary" icon="el-icon-download" style="margin-top: 7px" plain @click="hadlePreview(id)">导出pdf</el-button>
        </el-col>
        <!-- <el-col :span="2" class="risk-wenzi" style="margin:17px 5px 17px 20px;" v-if="riskTotalNum==0">
          <span class="first-title">自身风险<span class="o-red">{{riskTotalNum}}</span></span>
        </el-col>-->
      </el-row>
      <el-row class="self-row info-row" :gutter="40" v-if="activeTap">
        <el-col :span="17" class="left-col">
          <sticky :sticky-top="0">
            <el-row>
              <el-tabs type="border-card" v-model="activeTap">
                <el-tab-pane name="basicInfo" label="基本信息">
                  <el-button
                    type="text"
                    @click="handleScrollTo('gsxx')"
                    class="module-btn"
                    :class="{'active':activeBtn==='gsxx'}"
                  >工商信息</el-button>
                  <el-button
                    type="text"
                    @click="handleScrollTo('tjqy')"
                    class="module-btn"
                    :class="{'active':activeBtn==='tjqy'}"
                  >相似企业推荐</el-button>
                </el-tab-pane>
                <el-tab-pane name="businessRisk" label="经营风险">
                  <el-button
                    type="text"
                    @click="handleScrollTo('cfjl')"
                    class="module-btn"
                    :class="{'active':activeBtn==='cfjl'}"
                  >处罚记录</el-button>
                  <el-button
                    type="text"
                    @click="handleScrollTo('glqk')"
                    class="module-btn"
                    :class="{'active':activeBtn==='glqk'}"
                  >各类欠款</el-button>
                  <el-button
                    type="text"
                    @click="handleScrollTo('sfjf')"
                    class="module-btn"
                    :class="{'active':activeBtn==='sfjf'}"
                  >司法纠纷</el-button>
                </el-tab-pane>
                <el-tab-pane name="investmentInfo" label="投资信息">
                  <el-button
                    type="text"
                    @click="handleScrollTo('jbtz')"
                    class="module-btn"
                    :class="{'active':activeBtn==='jbtz'}"
                  >基本投资信息</el-button>
                  <el-button
                    type="text"
                    @click="handleScrollTo('qycz')"
                    class="module-btn"
                    :class="{'active':activeBtn==='qycz'}"
                  >企业出资信息</el-button>
                </el-tab-pane>
                <el-tab-pane name="intellectualPropertyInfo" label="知识产权">
                  <el-button
                    type="text"
                    @click="handleScrollTo('zscq')"
                    class="module-btn"
                    :class="{'active':activeBtn==='zscq'}"
                  >知识产权信息</el-button>
                </el-tab-pane>
                <el-tab-pane name="brandInfo" label="品牌信息">
                  <el-button
                    type="text"
                    @click="handleScrollTo('ppxx')"
                    class="module-btn"
                    :class="{'active':activeBtn==='ppxx'}"
                  >知识产权信息</el-button>
                </el-tab-pane>
                <el-tab-pane name="recruitInfo" label="招聘信息">
                  <el-button
                    type="text"
                    @click="handleScrollTo('zpxx')"
                    class="module-btn"
                    :class="{'active':activeBtn==='zpxx'}"
                  >招聘信息</el-button>
                </el-tab-pane>
                <el-tab-pane name="creditInfo" label="信用">
                  <el-button
                    type="text"
                    @click="handleScrollTo('qyxy')"
                    class="module-btn"
                    :class="{'active':activeBtn==='qyxy'}"
                  >企业信用</el-button>
                </el-tab-pane>
              </el-tabs>
            </el-row>
          </sticky>

          <el-row style="margin-top: 50px">
            <!-- <keep-alive>是Vue的内置组件，能在组件切换过程中将状态保留在内存中，防止重复渲染DOM
            <keep-alive> 包裹动态组件时，会缓存不活动的组件实例，而不是销毁它们-->
            <keep-alive>
              <!-- component的is,即多个组件可以使用同一个挂载点，根据条件来切换不同的组件 -->
              <component
                :is="activeTap"
                :id="id"
                :basicInfo="basicInfo"
                :tagRank='tagRank'
                v-loading="loading"
                :ref="activeTap"
                @load-success="loadSuccess"
              ></component>
            </keep-alive>
          </el-row>
        </el-col>
        <!-- 右侧展示图 -->
        <el-col :span="7" class="right-col">
          <el-row>
            <img src="../../assets/index/details-img01.png" alt />
          </el-row>
        </el-col>
      </el-row>
      <!-- pdf弹窗 -->
      <el-dialog title="预览" :visible.sync="viewVisible" width="80%" height="100%" :before-close='closeDialog'>
        <!-- <el-link target="_blank" :href="url" :underline="false" style="margin-left:15px">
          <el-button type="primary" icon="el-icon-download" style="margin-top: 7px" plain>下载</el-button>
        </el-link> -->
        <el-button type="primary" icon="el-icon-download" style="margin-top: 7px" plain @click="HandleDownload">下载</el-button>
        <div class="pdf" v-show="fileType === 'pdf'">
          <div v-for="i in numPages" :key="i">
            <pdf :src="pdfsrc" :page='i' style="width:70%;margin-left:300px;"></pdf>
          </div>
       	</div>
      </el-dialog>
    </el-main>
     <my-footer></my-footer>
  </el-container>
</template>

<script>
import detail from '@/api/detail/index'
import basicInfo from './basicInfo' // 企业基本信息模块
import businessRisk from './businessRisk' // 风险模块
import investmentInfo from './investmentInfo' // 投资模块
import intellectualPropertyInfo from './intellectualPropertyInfo' // 知识产权模块
import brandInfo from './brandInfo' // 品牌模块
import recruitInfo from './recruitInfo' // 招聘模块
import creditInfo from './creditInfo' // 信用模块
import store from '@/store'
import myHeader from './header'
import myFooter from '@/views/home/footer'
// import PDF from './PDF'
import pdf from 'vue-pdf'

export default {
  data() {
    return {
      activeTap: 'basicInfo', // 激活tab
      activeBtn: '',
      id: this.$route.params.id, // 企业id
      annals: undefined,
      basicInfo: {}, // 企业基本信息
      loading: false,
      rank: 4.2,
      tagRank: {}, // 标签评分
      myTagRank: {},
      viewVisible: false, // pdf弹窗
      fileType: 'pdf',
      pdfsrc: '', // 文件地址
      numPages: '', // 页数
      url: undefined
    }
  },
  components: {
    basicInfo,
    businessRisk,
    investmentInfo,
    intellectualPropertyInfo,
    brandInfo,
    recruitInfo,
    creditInfo,
    myHeader,
    myFooter,
    // PDF
    pdf
  },
  methods: {
    loadSuccess() {
      setTimeout(() => {
        this.loading = false
      }, 0.5 * 1000)
    },
    handleScrollTo(id, tab = undefined) {
      if (tab !== undefined) {
        this.activeTap = tab
        if (document.getElementById(id) !== null) {
          this.initPosition(id)
        } else {
          this.$nextTick(function() {
            this.initPosition(id)
          })
        }
      } else {
        this.activeBtn = id
        if (document.getElementById(id) !== null) {
          this.initPosition(id)
        }
      }
    },
    initPosition(id) {
      const offset = document.getElementById(id).offsetTop
      document.documentElement.scrollTop = offset + 400
    },
    initBasicInfoList() {
      var vue = this
      const data = {}
      data.id = vue.id
      console.log(data.id)
      detail.searchBasicInfo(data).then(resp => {
        console.log(resp)
        if (resp) {
          vue.basicInfo = resp
          // this.updateDetailClickRate()
        } else {
          this.$router.push({ path: '/notFound' })
        }
      })
    },
    // 初始化标签
    initTagRank() {
      var vue = this
      const data = {}
      data.id = vue.id
      detail.searchTagInfo(data).then(resp => {
        console.log(resp)
        if (resp) {
          vue.tagRank = resp.data
          // 使符合格式
          vue.tagRank.totScore /= 2
          vue.tagRank.investmentScore /= 2
          vue.tagRank.intellectualPropertyScore /= 2
          vue.tagRank.brandScore /= 2
          vue.tagRank.recruitScore /= 2
          vue.tagRank.creditScore /= 2
        } else {
          this.$router.push({ path: '/notFound' })
        }
      })
    },
    // 预览
    hadlePreview(item) {
      console.log('item = ', item)
      // var url = ''
      const data = {}
      data.id = item
      detail.searchEntReporturl(data).then(resp => {
        console.log(resp.data.reportURL)
        this.url = resp.data.reportURL
        this.viewVisible = true
        this.pdfsrc = pdf.createLoadingTask(this.url)
        this.pdfsrc.then(pdf => {
          this.numPages = pdf.numPages
        }).catch(() => {})
      }).catch(err => {
        console.log(err)
      })
      // console.log(row.wjYsmc)
      // if (!/\.(pdf|PDF)$/.test(item.AttachmentName)) { // 非pdf文件
      //   window.open(
      //     'https://view.officeapps.live.com/op/view.aspx?src=' + item.AttachmentPath + '/anli?id=' + item.MessageAttachmentId,
      //     '_blank'
      //   )
      //   return false
      // } else { // pdf文件
      //   const url = item.AttachmentPath + '/anli?id=' + item.MessageAttachmentId
      //   this.viewVisible = true
      //   // 以下代码高能
      //   this.pdfsrc = pdf.createLoadingTask(url)
      //   this.pdfsrc.then(pdf => {
      //     this.numPages = pdf.numPages
      //   }).catch(() => {})
      // }
      // const url = 'http://121.36.13.179/static/pdf/ent_report.pdf'
      // console.log(this.url)
      // this.viewVisible = true
      // 以下代码高能
      // this.pdfsrc = pdf.createLoadingTask(url)
      // this.pdfsrc.then(pdf => {
      //   this.numPages = pdf.numPages
      // }).catch(() => {})
    },
    closeDialog(done) {
      done()
    },
    HandleDownload() {
      var location = this.url
      window.open(location)
    }
  },
  created() {
    this.initBasicInfoList()
    this.initTagRank()
  },
  computed: {
    listenTcaptcha() {
      return this.$store.state.captcha.tcaptcha
    }
  },
  watch: {
    listenTcaptcha: function(nv, ov) {
      if (this.$store.state.captcha.tcaptcha) {
        this.initBasicInfoList()
        this.initTagRank()
        // this.initSelfRisk()
        // this.initPromptMessage()
        this.activeTap = this.$route.query.activeTap || 'basicInfo'
        store.dispatch('Tcaptcha', false)
      }
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.cunx {
  border: 1px solid #209c16;
  color: #209c16;
  padding: 5px 20px;
  text-align: center;
  font-size: 14px;
  line-height: 22px;
}
.el-header {
  height: 55px;
  background: #3a71d8;
  min-width: 1200px;
  .list-header {
    height: 100%;
    max-width: 1200px;
    margin: 0 auto;
    .logo {
      height: 100%;
      line-height: 55px;
      img {
        vertical-align: middle;
      }
    }
    .header-right {
      line-height: 55px;
      .searchtip-ipt {
        width: 100%;
        height: 36px;
      }
    }
  }
}
.el-main {
  padding: 0 !important;
  .self-row {
    width: 1200px;
    margin: 20px auto !important;
  }
  .top-row {
    height: 230px;
    padding: 18px;
    background: #ffffff;
    border: 1px solid rgba(242, 242, 242, 1);
    .top-row-inner {
      width: 100%;
      height: 100%;
      background: #eef3fb;
      padding: 20px;
      h2 {
        font-size: 22px;
        margin-top: 0px !important;
        font-weight: normal;
        color: #000;
      }
      .logo {
        height: 106px;
        width: 106px;
      }
      .inner-row1 {
        font-size: 16px;
        color: #333;
        font-weight: normal;
        margin: 10px;
      }
      .inner-row-text {
        font-size: 14px;
        color: #666;
      }
      .row-margin {
        margin: 2px 0px 5px 10px;
      }
    }
  }
  .bjrisk-row {
    background: #fff;
    border: 1px solid rgba(242, 242, 242, 1);
    height: 50px;
    .bj-img {
      text-align: center;
      height: 100%;
      line-height: 48px;
      border-right: solid 1px #e2e2e2;
      img {
        vertical-align: middle;
      }
    }
    .bj-img2 {
      text-align: center;
      height: 100%;
      line-height: 48px;
      img {
        vertical-align: middle;
      }
    }
    .risk-wenzi {
      font-size: 14px;
      color: #666;
      text-decoration: none;
      text-align: center;
      position: relative;
      .red {
        color: #ff0000;
      }
      .o-red {
        margin-left: 5px;
        color: #ff0000;
      }
      .first-title:hover {
        color: #3a71d8;
      }
    }
  }
  .self-stick .content-row {
    width: 100%;
  }
  .info-row {
    margin-top: 20px !important;
    .module-btn {
      background: #eef3fb;
      color: #666;
      padding: 8px;
      border-radius: 0;
      border: 1px solid rgba(242, 242, 242, 0.1);
    }
    .module-btn:hover {
      background: #3a71d8;
      color: #fff;
    }
    .active {
      background: #3a71d8;
      color: #fff;
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
    .right-col {
      padding-right: 0 !important;
      .el-row {
        height: 220px;
        margin-bottom: 20px;
        img {
          height: 100%;
          width: 100%;
        }
      }
    }
  }
}
</style>
