<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="32">
      <el-col :span="8">
        <div style="margin-bottom:20px;">
          <h2>
            <strong>企业聚类分析</strong>
          </h2>
          <small>企业属性聚类的可视化展示</small>
        </div>
      </el-col>
      <el-col :span="16">
        <!-- <el-checkbox-group
          v-model="checkboxGroup1"
          :min="1"
          :max="3"
        >
          <el-checkbox v-for="tag in tags" :key="tag" :label="tag">{{ tag }}</el-checkbox>
        </el-checkbox-group> -->
        <div style="margin-top: 20px">
          <el-radio v-model="radio" label="1" border size="medium">二维图</el-radio>
          <el-radio v-model="radio" label="2" border size="medium">三维图</el-radio>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="32">
      <div v-show="type==='2d'" class="chart-wrapper">
        <scatter :key="timer" height="600%" width="100%" :chart-data="chart2dData" />
      </div>
      <div v-show="type==='3d'" class="chart-wrapper">
        <scatter3d :key="timer" height="600%" width="100%" :chart-data="chart3dData" />
      </div>
    </el-row>
    <!-- <el-row>
      <div class="chart-wrapper">
        <scatter3d height="500%" width="100%" />
      </div>
    </el-row> -->
    <!-- <div class="chart-container">
      <scatter height="100%" width="100%" />
    </div>
    <div class="chart-container">
      <scatter3d height="100%" width="100%" />
    </div>
  </div> -->
  </div>
</template>
<script>
import scatter from '@/components/Scatter'
import scatter3d from '@/components/3D-Scatter'
import { get2dcluster, get3dcluster } from '@/api/cluster'
export default {
  components: {
    scatter,
    scatter3d
  },
  data() {
    return {
      // checkboxGroup1: ['标签一'],
      // tags: ['标签一', '标签二', '标签三', '标签四', '标签五', '标签六', '标签七', '标签八'],
      radio: '1',
      type: '2d',
      timer: '',
      chart2dData: {},
      chart3dData: {}
    }
  },
  watch: {
    // checkbradiooxGroup1: {
    //   handler(newValue, oldValue) {
    //     // for (let i = 0; i < newValue.length; i++) {
    //     //   if (oldValue[i] !== newValue[i]) {
    //     //     console.log(newValue)
    //     //   }
    //     // }
    //     if (newValue.length === 3) {
    //       this.type = '3d'
    //       this.timer = new Date().getTime()
    //     } else if (newValue.length === 2) {
    //       this.type = '2d'
    //       this.timer = new Date().getTime()
    //     }
    //   }
    // }
    radio(val) {
      if (this.radio === '1') {
        this.type = '2d'
        this.timer = new Date().getTime()
      } else if (this.radio === '2') {
        this.type = '3d'
        this.timer = new Date().getTime()
      }
    }
  },
  created() {
    this.init2dclusterdata()
    this.init3dclusterdata()
  },
  methods: {
    init2dclusterdata() {
      get2dcluster().then(resp => {
        console.log(resp)
        this.chart2dData = resp.data
        this.timer = new Date().getTime()
      }).catch()
    },
    init3dclusterdata() {
      get3dcluster().then(resp => {
        console.log(resp)
        this.chart3dData = resp.data
        this.timer = new Date().getTime()
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.chart-container{
  position: relative;
  width: 100%;
  height: calc(100vh - 84px);
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

