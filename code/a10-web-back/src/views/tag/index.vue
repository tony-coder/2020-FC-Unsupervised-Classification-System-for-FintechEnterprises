<template>
  <div class="dashboard-editor-container">
    <div style="margin-bottom:20px;">
      <h2>
        <strong>企业标签分析</strong>
      </h2>
      <small>基于聚类得出的标签</small>
    </div>
    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="12">
        <div class="chart-wrapper">
          <wordCloudChart
            id="echarts05"
            :title="title"
            :data="echarts05Data"
            :width="width"
            :height="height"
          />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="12">
        <div class="chart-wrapper">
          <pieChart
            :width="width"
            :height="height"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import wordCloudChart from '@/components/WordCloudChart'
import pieChart from '@/components/PieChart'
export default {
  components: {
    wordCloudChart,
    pieChart
  },
  data() {
    return {
      title: '标签分析',
      width: '100%',
      height: '400px',
      echarts05Data: [
        {
          name: '十九大精神',
          value: 15000
        },
        {
          name: '两学一做',
          value: 10081
        },
        {
          name: '中华民族',
          value: 9386
        },
        {
          name: '马克思主义',
          value: 7500
        },
        {
          name: '民族复兴',
          value: 7500
        },
        {
          name: '社会主义制度',
          value: 6500
        },
        {
          name: '国防白皮书',
          value: 6500
        },
        {
          name: '创新',
          value: 6000
        },
        {
          name: '民主革命',
          value: 4500
        },
        {
          name: '文化强国',
          value: 3800
        },
        {
          name: '国家主权',
          value: 3000
        },
        {
          name: '武装颠覆',
          value: 2500
        },
        {
          name: '领土完整',
          value: 2300
        },
        {
          name: '安全',
          value: 2000
        },
        {
          name: '从严治党',
          value: 1900
        },
        {
          name: '现代化经济体系',
          value: 1800
        },
        {
          name: '国防动员',
          value: 1700
        },
        {
          name: '信息化战争',
          value: 1600
        },
        {
          name: '局部战争',
          value: 1500
        },
        {
          name: '教育',
          value: 1200
        },
        {
          name: '职业教育',
          value: 1100
        },
        {
          name: '兵法',
          value: 900
        },
        {
          name: '一国两制',
          value: 800
        },
        {
          name: '特色社会主义思想',
          value: 700
        }
      ]
    }
  }
}
</script>
<style lang="scss" scoped>
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
