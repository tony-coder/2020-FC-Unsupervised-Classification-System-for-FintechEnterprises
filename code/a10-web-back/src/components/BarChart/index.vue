<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
export default {
  props: {
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
    },
    mytitle: {
      type: String,
      default: 'default'
    },
    bardata: {
      type: Array,
      // default: function () { return [] }
      default: () => []
    },
    xlebal: {
      type: Array,
      // default: function () { return [] }
      default: () => []
    },
    xname: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      chart: null
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.chart.setOption({
        title: {
          show: true,
          text: this.mytitle,
          textStyle: {
            color: 'black'
          },
          padding: [0, 0, 10, 100] // 位置
        },
        legend: {},
        color: ['#3398DB'],
        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '13%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            name: this.xname,
            type: 'category',
            data: this.xlebal,
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis: [
          {
            name: '百分比(%)',
            type: 'value',
            min: 0,
            max: 100,
            axisLabel: {// 文字样式
              formatter: '{value}%'
            }
          }
        ],
        series: [
          {
            // name: '直接访问',
            type: 'bar',
            barWidth: '60%',
            // data: [3.38, 3.36, 8.92, 13.02, 11.87, 15.69, 24.89, 11.55, 4.79, 2.15, 0.38],
            data: this.bardata,
            itemStyle: {
              normal: {
                label: {
                  show: true, // 开启显示
                  position: 'top', // 在上方显示
                  textStyle: { // 数值样式
                    color: 'black',
                    fontFamily: '微软雅黑',
                    fontSize: 12
                  },
                  formatter: '{c}%' // 模板变量有 {a}、{b}、{c}、{d}，分别表示系列名，数据名，数据值，百分比。{d}数据会根据value值计
                }
              }
            }
          }
        ]
      })
    }
  }
}
</script>
