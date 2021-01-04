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
      default: '500px'
    },
    autoResize: {
      type: Boolean,
      default: true
    },
    chartData: {
      type: Object,
      required: true
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
          text: '企业聚簇分布情况',
          subtext: '抽样数据来自: 大熊维尼'
        },
        grid: {
          left: '3%',
          right: '7%',
          bottom: '3%',
          containLabel: true
        },
        tooltip: {
        // trigger: 'axis',
          showDelay: 0,
          formatter: function(params) {
            if (params.value.length > 1) {
              return params.seriesName + ' :<br/>' +
                'x: ' + params.value[0] + ' ' +
                'y: ' + params.value[1] + ' '
            } else {
              return params.seriesName + ' :<br/>' +
                params.name + ' : ' +
                params.value + ' '
            }
          },
          axisPointer: {
            show: true,
            type: 'cross',
            lineStyle: {
              type: 'dashed',
              width: 1
            }
          }
        },
        toolbox: {
          feature: {
            dataZoom: {},
            brush: {
              type: ['rect', 'polygon', 'clear']
            }
          }
        },
        brush: {
        },
        legend: {
          data: ['簇0', '簇1', '簇2', '簇3', '簇4', '簇5', '簇6', '簇7', '簇8', '簇9', '簇10', '簇11', '簇12', '簇13', '簇14'],
          left: 'center'
        },
        xAxis: [
          {
            type: 'value',
            scale: true,
            // axisLabel: {
            //   formatter: '{value} cm'
            // },
            splitLine: {
              show: false
            }
          }
        ],
        yAxis: [
          {
            type: 'value',
            scale: true,
            // axisLabel: {
            //   formatter: '{value} kg'
            // },
            splitLine: {
              show: false
            }
          }
        ],
        series: [
          {
            name: '簇0',
            type: 'scatter',
            data: this.chartData['label0']
            // markArea: {
            //   silent: true,
            //   itemStyle: {
            //     color: 'transparent',
            //     borderWidth: 1,
            //     borderType: 'dashed'
            //   },
            //   data: [[{
            //     name: '女性分布区间',
            //     xAxis: 'min',
            //     yAxis: 'min'
            //   }, {
            //     xAxis: 'max',
            //     yAxis: 'max'
            //   }]]
            // },
            // markPoint: {
            //   data: [
            //     { type: 'max', name: '最大值' },
            //     { type: 'min', name: '最小值' }
            //   ]
            // },
            // markLine: {
            //   lineStyle: {
            //     type: 'solid'
            //   },
            //   data: [
            //     { type: 'average', name: '平均值' },
            //     { xAxis: 160 }
            //   ]
            // }
          },
          {
            name: '簇1',
            type: 'scatter',
            data: this.chartData['label1']
          },
          {
            name: '簇2',
            type: 'scatter',
            data: this.chartData['label2']
          },
          {
            name: '簇3',
            type: 'scatter',
            data: this.chartData['label3']
          },
          {
            name: '簇4',
            type: 'scatter',
            data: this.chartData['label4']
          },
          {
            name: '簇5',
            type: 'scatter',
            data: this.chartData['label5']
          },
          {
            name: '簇6',
            type: 'scatter',
            data: this.chartData['label6']
          },
          {
            name: '簇7',
            type: 'scatter',
            data: this.chartData['label7']
          },
          {
            name: '簇8',
            type: 'scatter',
            data: this.chartData['label8']
          },
          {
            name: '簇9',
            type: 'scatter',
            data: this.chartData['label9']
          },
          {
            name: '簇10',
            type: 'scatter',
            data: this.chartData['label10']
          },
          {
            name: '簇11',
            type: 'scatter',
            data: this.chartData['label11']
          },
          {
            name: '簇12',
            type: 'scatter',
            data: this.chartData['label12']
          },
          {
            name: '簇13',
            type: 'scatter',
            data: this.chartData['label13']
          },
          {
            name: '簇14',
            type: 'scatter',
            data: this.chartData['label14']
          }
        ]
      })
    }
  }
}
</script>
