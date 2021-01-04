<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
// import resize from "./mixins/resize";

const animationDuration = 3000

export default {
//   mixins: [resize],
  props: {
    tagRankList: undefined,
    enterpriseName: String,
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
      chart: null
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
    // console.log(this.enterpriseName)
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
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        radar: {
          radius: '66%',
          center: ['50%', '42%'],
          splitNumber: 10,
          splitArea: {
            // show: false,
            areaStyle: {
              color: 'rgba(127,95,132,.3)',
              opacity: 1,
              shadowBlur: 45,
              shadowColor: 'rgba(0,0,0,.5)',
              shadowOffsetX: 0,
              shadowOffsetY: 15
            }
          },
          indicator: [
            { name: '风险', max: 10 },
            { name: '投资', max: 10 },
            { name: '创新', max: 10 },
            { name: '品牌', max: 10 },
            { name: '招聘', max: 10 },
            { name: '信用', max: 10 },
            { name: '基本', max: 10 }
          ]
        },
        legend: {
          left: 'center',
          bottom: '10',
          data: [this.enterpriseName]
        },
        series: [
          {
            type: 'radar',
            symbolSize: 0,
            areaStyle: {
              normal: {
                shadowBlur: 13,
                shadowColor: 'rgba(0,0,0,.2)',
                shadowOffsetX: 0,
                shadowOffsetY: 10,
                opacity: 1
              }
            },
            data: [
              {
                value: this.tagRankList,
                name: this.enterpriseName,
                // 设置区域边框和区域的颜色
                // itemStyle: {
                //   normal: {
                //     color: 'rgba(255,225,0,.3)',
                //     lineStyle: {
                //       color: 'rgba(255,225,0,.3)'
                //     }
                //   }
                // }
                // 在拐点处显示数值
                label: {
                  normal: {
                    show: true,
                    formatter: function(params) {
                      return params.value
                    }
                  }
                }
              }
            ],
            animationDuration: animationDuration
          }
        ]
      })
    }
  }
}
</script>
