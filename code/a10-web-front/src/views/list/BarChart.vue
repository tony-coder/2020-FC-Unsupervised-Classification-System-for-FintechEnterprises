<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
// import resize from './mixins/resize'

// const animationDuration = 6000

export default {
//   mixins: [resize],
  props: {
    EntList: undefined,
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '300px'
    }
  },
  data() {
    return {
      chart: null,
      leg: []
    }
  },
  mounted() {
    for (const val of this.EntList) {
      this.leg.push(val['name'])
    }
    console.log(this.leg)
    this.$nextTick(() => {
      this.initChart()
    })
    console.log('init')
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  // watch: {
  //   comparedata(compareEntList) {
  //     console.log(compareEntList)
  //     this.initChart()
  //   }
  // },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')

      this.chart.setOption({
        toolbox: {
          show: true,
          feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ['line', 'bar'] },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          top: 10,
          left: '2%',
          right: '2%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [{
          type: 'category',
          data: ['风险', '投资', '创新', '品牌', '招聘', '信用', '基本'],
          axisTick: {
            alignWithLabel: true
          }
        }],
        yAxis: [{
          type: 'value',
          max: 10,
          min: 0,
          axisTick: {
            show: false
          }
        }],
        legend: {
          orient: 'horizontal',
          top: '8%',
          right: '0%',
          data: this.leg
        },
        // series: [{
        //   name: '879f0cc70bca77a4bd25cb90ce54608f',
        //   type: 'bar',
        //   // stack: 'vistors',
        //   barWidth: 20,
        //   data: [1, 3.2, 6, 3, 8.8, 7, 4],
        //   animationDuration: 6000
        // }, {
        //   name: 'f99f0c54e8d3737d0a9784fde735b36e',
        //   type: 'bar',
        //   // stack: 'vistors',
        //   barWidth: 20,
        //   data: [3.5, 7, 10, 3.4, 1.7, 8, 5],
        //   animationDuration: 6000
        // }, {
        //   name: '42f919f0c04fc1af7054e8a107d5903a',
        //   type: 'bar',
        //   // stack: 'vistors',
        //   barWidth: 20,
        //   data: [0, 3, 0, 7, 0, 2, 3],
        //   animationDuration: 6000
        // }]
        series: this.EntList
      })
    }
  }
}
</script>
