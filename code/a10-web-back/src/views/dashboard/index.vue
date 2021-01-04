<template>
  <div class="dashboard-container">
    <div class="dashboard-text">您好: {{ name }}</div>
    <el-row>
      <div>
        <panel-group :key="timer" :user-count="userCount" :ent-count="entCount" />
      </div>
    </el-row>
    <el-row>
      <wordCloudChart
        id="echarts05"
        :title="title"
        :data="echarts05Data"
        :width="width"
        :height="height"
      />
    </el-row>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import PanelGroup from './components/PanelGroup'
import wordCloudChart from '@/components/WordCloudChart'
import { getinitdata } from '@/api/dashboard'

export default {
  name: 'Dashboard',
  components: {
    PanelGroup,
    wordCloudChart
  },
  data() {
    return {
      data: null,
      userCount: 0,
      entCount: 0,
      timer: 0,
      title: '',
      width: '100%',
      height: '400px',
      echarts05Data: [
        {
          name: '风险',
          value: 15000
        },
        {
          name: '投资',
          value: 10081
        },
        {
          name: '知识产权',
          value: 9386
        },
        {
          name: '创新',
          value: 7500
        },
        {
          name: '招聘',
          value: 7500
        },
        {
          name: '信用',
          value: 6500
        },
        {
          name: '投资',
          value: 6500
        },
        {
          name: '创新',
          value: 6000
        },
        {
          name: '信用',
          value: 4500
        },
        {
          name: '知识产权',
          value: 3800
        },
        {
          name: '风险',
          value: 3000
        },
        {
          name: '知识产权',
          value: 2500
        },
        {
          name: '投资',
          value: 2300
        },
        {
          name: '安全',
          value: 2000
        },
        {
          name: '基本',
          value: 1900
        },
        {
          name: '用人需求',
          value: 1800
        },
        {
          name: '风险',
          value: 1700
        },
        {
          name: '创新',
          value: 1600
        },
        {
          name: '用人需求',
          value: 1500
        },
        {
          name: '基本',
          value: 1200
        },
        {
          name: '风险',
          value: 1100
        },
        {
          name: '招聘',
          value: 900
        },
        {
          name: '信用',
          value: 700
        }
      ]
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      getinitdata().then(resp => {
        this.userCount = resp.data.userNum
        this.entCount = resp.data.entNum
        this.timer = new Date().getTime()
      }).catch()
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
