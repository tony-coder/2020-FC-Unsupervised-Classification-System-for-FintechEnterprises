<template>
  <div class="dashboard-editor-container">
    <div style="margin-bottom:20px;">
      <h2>
        <strong>数据测试</strong>
      </h2>
      <small>输入企业信息，预测企业分类并打上标签</small>
    </div>
    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="12">
        <el-row>
          <span><b>训练</b></span>
        </el-row>
        <el-row>
          <div style="margin-bottom:10px;">
            <span><b>上传训练文件</b></span>
          </div>
          <el-upload
            ref="upload1"
            class="upload-demo"
            action="/api/api/bfx/upload/train"
            :before-upload="beforeUpload"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :on-success="handlesuccess1"
            :file-list="fileList1"
            :auto-upload="false"
          >
            <el-button slot="trigger" size="small" type="primary">导入训练数据</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload1">上传</el-button>
            <div slot="tip" class="el-upload__tip">只能上传zip文件，且不超过100Mb</div>
          </el-upload>
        </el-row>
        <el-row>
          <el-col :span="12">
            <div v-show="istrain==true">
              <el-button type="primary" @click="handleTrain">开始训练</el-button>
            </div>
            <div v-show="istrain==false">
              <el-button type="primary" disabled @click="handleTrain">开始训练</el-button>
            </div>
          </el-col>
          <el-col v-show="istrainsuccess" :span="12">
            <div>
              数据处理总用时: {{ trainTotTime }}s | 训练用时: {{ trainTime }}s
              <el-button type="success" @click="downloadRes(trainurl)">训练结果下载</el-button>
            </div>
          </el-col>
        </el-row>
        <hr>
        <el-row>
          <span><b>预测</b></span>
        </el-row>
        <el-row>
          <!-- <uploader :url="url" @fun="changePredictbtn" /> -->
          <div style="margin-bottom:10px;">
            <span><b>上传测试文件</b></span>
          </div>
          <el-upload
            ref="upload2"
            class="upload-demo"
            action="/api/api/bfx/upload/predict"
            :before-upload="beforeUpload"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :on-success="handlesuccess2"
            :file-list="fileList2"
            :auto-upload="false"
          >
            <el-button slot="trigger" size="small" type="primary">导入测试数据</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload2">上传</el-button>
            <div slot="tip" class="el-upload__tip">只能上传zip文件，且不超过100Mb</div>
          </el-upload>
        </el-row>
        <el-row>
          <div style="margin-bottom:10px;">
            <el-radio v-model="radio" label="1">默认模型</el-radio>
            <el-radio v-show="istrainsuccess==true" v-model="radio" label="2">新模型</el-radio>
            <el-radio v-show="istrainsuccess==false" v-model="radio" label="2" disabled>新模型</el-radio>
          </div>
          <el-col :span="12">
            <div v-show="ispredict==true">
              <el-button type="primary" @click="handlePredict">开始预测</el-button>
            </div>
            <div v-show="ispredict==false">
              <el-button type="primary" disabled @click="handlePredict">开始预测</el-button>
            </div>
          </el-col>
          <el-col :span="12">
            <div v-show="isResult">
              <span>数据处理总用时: {{ predictTotTime }}s | 预测用时: {{ predictTime }}s</span>
              <el-button type="success" @click="downloadRes(downloadurl)">预测结果下载</el-button>
            </div>
          </el-col>
        </el-row>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="12">
        <div style="margin-bottom:10px;">
          <span><b>测试页面使用说明</b></span>
        </div>
        <div>
          <p>
            1. 用户可以根据自己的需要选择使用默认模型进行预测，或者选择自己上传训练数据来训练模型，并使用新模型进行预测，默认使用系统自带的默认模型
          </p>
          <p>
            2. 需要训练数据时，请点击导入训练数据并选择训练数据文件(要求为压缩包的形式)导入，当完成导入时下方会显示文件名，点击上传进行训练
            请耐心等待几秒钟即可完成训练，并有训练成功的提示和相关用时。
          </p>
          <p>
            3. 需要测试数据时，请点击预测标题下的导入测试数据文件(要求为压缩包的形式)，当完成导入时下方会显示文件夹名，点击开始预测对测试数据进行预测，
            请耐心等待几秒钟即可完成预测，并会有预测成功和下载结果文件的提示。
          </p>
          <p>
            4. 预测成功后，请点击结果下载按钮进行结果的下载
          </p>
          <p>
            5. 如有意外情况不能训练或测试，请退出浏览器并清空浏览器缓存，或者更换浏览器，推荐使用chrome浏览器
          </p>
          <p>
            6. 所有训练数据和测试数据的文件格式和命名严格对照"服创大赛训练集-Inspur"中所给的数据集
          </p>
        </div>
        <!-- <div class="chart-wrapper">
          <myform :key="timer" :table-data="tableData" :loading="loading" />
        </div> -->
      </el-col>
    </el-row>
    <!-- <el-row>
      <el-row>
        <uploader :url="url" />
      </el-row>
      <div style="margin-bottom:10px;">
        <el-radio v-model="radio" label="1">默认模型</el-radio>
        <el-radio v-model="radio" label="2">新模型</el-radio>
      </div>
      <div>
        <el-button type="primary" @click="handlePredict">开始预测</el-button>
      </div>
    </el-row> -->
  </div>
</template>
<script>
// import myform from './components/form'
// import uploader from '@/components/Upload/globalUploader'
import { getresultData, stratTrain } from '@/api/test'
export default {
  components: {
    // uploader
    // myform
  },
  data() {
    return {
      title: '生成标签',
      width: '100%',
      height: '400px',
      url: '/api/api/bfx/upload/predict',
      fileList1: [],
      fileList2: [],
      tableData: [],
      timer: '',
      loading: false,
      trainTotTime: '',
      trainTime: '',
      predictTotTime: '',
      predictTime: '',
      radio: '1',
      trainurl: '',
      downloadurl: '',
      istrain: false,
      ispredict: false,
      istrainsuccess: false,
      isResult: false
    }
  },
  watch: {

  },
  methods: {
    submitUpload1() {
      this.$refs.upload1.submit()
    },
    submitUpload2() {
      this.$refs.upload2.submit()
    },
    handleRemove(file, fileList) {
      console.log(file, fileList)
    },
    handlePreview(file) {
      console.log(file)
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
    },
    handlesuccess1(response, file, fileList) {
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
    handlesuccess2(response, file, fileList) {
      if (response.data.message === '上传成功') {
        this.ispredict = true
        this.$notify({
          title: '成功',
          message: response.data.message,
          type: 'success'
        })
      } else {
        this.ispredict = false
        this.$notify.error({
          title: '错误',
          message: response.data.message
        })
      }
    },
    handlePredict() {
      this.loading = true
      const data = {}
      data.model = this.radio
      getresultData(data).then(resp => {
        console.log(resp)
        this.predictTime = resp.predictTime
        this.predictTotTime = resp.totlTime
        this.downloadurl = resp.url
        this.isResult = true
        // const data = resp.data.res
        // for (var i = 0; i < data.length; i++) {
        //   var tmp = { id: '', tag: [] }
        //   tmp.id = data[i].id
        //   // 风险
        //   if (data[i].riskScore === 1) {
        //     tmp.tag.push('风险低')
        //   } else if (data[i].riskScore === 2) {
        //     tmp.tag.push('风险较低')
        //   } else if (data[i].riskScore === 3) {
        //     tmp.tag.push('风险中等')
        //   } else if (data[i].riskScore === 4) {
        //     tmp.tag.push('风险较高')
        //   } else if (data[i].riskScore === 5) {
        //     tmp.tag.push('风险高')
        //   }
        //   // 投资
        //   if (data[i].investmentScore === 1) {
        //     tmp.tag.push('投资低')
        //   } else if (data[i].investmentScore === 2) {
        //     tmp.tag.push('投资较低')
        //   } else if (data[i].investmentScore === 3) {
        //     tmp.tag.push('投资中等')
        //   } else if (data[i].investmentScore === 4) {
        //     tmp.tag.push('投资较高')
        //   } else if (data[i].investmentScore === 5) {
        //     tmp.tag.push('投资高')
        //   }
        //   // 创新水平
        //   if (data[i].investmentScore === 1) {
        //     tmp.tag.push('创新水平低')
        //   } else if (data[i].investmentScore === 2) {
        //     tmp.tag.push('创新水平较低')
        //   } else if (data[i].investmentScore === 3) {
        //     tmp.tag.push('创新水平中等')
        //   } else if (data[i].investmentScore === 4) {
        //     tmp.tag.push('创新水平较高')
        //   } else if (data[i].investmentScore === 5) {
        //     tmp.tag.push('创新水平高')
        //   }
        //   // 品牌
        //   if (data[i].brandScore === 1) {
        //     tmp.tag.push('品牌低')
        //   } else if (data[i].brandScore === 2) {
        //     tmp.tag.push('品牌较低')
        //   } else if (data[i].brandScore === 3) {
        //     tmp.tag.push('品牌中等')
        //   } else if (data[i].brandScore === 4) {
        //     tmp.tag.push('品牌较高')
        //   } else if (data[i].brandScore === 5) {
        //     tmp.tag.push('品牌高')
        //   }
        //   // 招聘
        //   if (data[i].recruitScore === 1) {
        //     tmp.tag.push('招聘低')
        //   } else if (data[i].recruitScore === 2) {
        //     tmp.tag.push('招聘较低')
        //   } else if (data[i].recruitScore === 3) {
        //     tmp.tag.push('招聘中等')
        //   } else if (data[i].recruitScore === 4) {
        //     tmp.tag.push('招聘较高')
        //   } else if (data[i].recruitScore === 5) {
        //     tmp.tag.push('招聘高')
        //   }
        //   // 信用
        //   if (data[i].creditScore === 1) {
        //     tmp.tag.push('信用低')
        //   } else if (data[i].creditScore === 2) {
        //     tmp.tag.push('信用较低')
        //   } else if (data[i].creditScore === 3) {
        //     tmp.tag.push('信用中等')
        //   } else if (data[i].creditScore === 4) {
        //     tmp.tag.push('信用较高')
        //   } else if (data[i].creditScore === 5) {
        //     tmp.tag.push('信用高')
        //   }
        //   this.tableData.push(tmp)
        // }
        this.timer = new Date().getTime()
        this.loading = false
      }).catch((err) => {
        this.$message.error(err)
        this.loading = false
        this.isResult = false
      })
    },
    handleTrain() {
      stratTrain().then(resp => {
        this.istrainsuccess = true
        this.trainTotTime = resp.totlTime
        this.trainTime = resp.trainTime
        this.trainurl = resp.url
        this.$notify({
          title: '成功',
          message: resp.message,
          type: 'success'
        })
      }).catch()
    },
    changePredictbtn(data) {
      this.ispredict = data
    },
    downloadRes(url) {
      location.href = 'http://121.36.13.179' + url
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
