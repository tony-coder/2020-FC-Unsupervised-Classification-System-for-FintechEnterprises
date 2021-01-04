<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
import echartsGL from 'echarts-gl'
// import axios from 'axios'
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
      var symbolSize = 2.5
      this.chart.setOption({
        grid3D: {},
        legend: {
          data: ['簇0', '簇1', '簇2', '簇3', '簇4', '簇5', '簇6', '簇7', '簇8', '簇9', '簇10', '簇11', '簇12', '簇13', '簇14'],
          left: 'center'
        },
        tooltip: {
        // trigger: 'axis',
          showDelay: 0,
          formatter: function(params) {
            if (params.value.length > 1) {
              return params.seriesName + ' :<br/>' +
               'x: ' + params.value[0] + ' ' +
                'y: ' + params.value[1] + ' ' +
                'z: ' + params.value[2] + ''
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
        xAxis3D: {
          type: 'category'
        },
        yAxis3D: {},
        zAxis3D: {},
        // dataset: {
        //   dimensions: [
        //     'x',
        //     'y',
        //     'z'
        //   ],
        //   // source: [['Income', 'Life Expectancy', 'Population', 'Country', 'Year'], [815, 34.05, 351014, 'Australia', 1800], [1314, 39, 645526, 'Canada', 1800], [985, 32, 321675013, 'China', 1800], [864, 32.2, 345043, 'Cuba', 1800], [1244, 36.5731262, 977662, 'Finland', 1800], [1803, 33.96717024, 29355111, 'France', 1800], [1639, 38.37, 22886919, 'Germany', 1800], [926, 42.84559912, 61428, 'Iceland', 1800], [1052, 25.4424, 168574895, 'India', 1800], [1050, 36.4, 30294378, 'Japan', 1800], [579, 26, 4345000, 'North Korea', 1800], [576, 25.8, 9395000, 'South Korea', 1800], [658, 34.05, 100000, 'New Zealand', 1800], [1278, 37.91620899, 868570, 'Norway', 1800], [1213, 35.9, 9508747, 'Poland', 1800], [1430, 29.5734572, 31088398, 'Russia', 1800], [1221, 35, 9773456, 'Turkey', 1800], [3431, 38.6497603, 12327466, 'United Kingdom', 1800], [2128, 39.41, 6801854, 'United States', 1800], [834, 34.05, 342440, 'Australia', 1810], [1400, 39.01496774, 727603, 'Canada', 1810], [985, 32, 350542958, 'China', 1810], [970, 33.64, 470176, 'Cuba', 1810], [1267, 36.9473378, 1070625, 'Finland', 1810], [1839, 37.4, 30293172, 'France', 1810], [1759, 38.37, 23882461, 'Germany', 1810], [928, 43.13915533, 61428, 'Iceland', 1810], [1051, 25.4424, 171940819, 'India', 1810], [1064, 36.40397538, 30645903, 'Japan', 1810]]
        //   source: this.chartData
        // },
        // series: [
        //   {
        //     type: 'scatter3D',
        //     symbolSize: symbolSize,
        //     encode: {
        //       x: 'x',
        //       y: 'y',
        //       z: 'z',
        //       tooltip: [0, 1, 2, 3, 4]
        //     }
        //   }
        // ]
        series: [
          {
            name: '簇0',
            type: 'scatter3D',
            data: this.chartData['label0'],
            symbolSize: symbolSize
          },
          {
            name: '簇1',
            type: 'scatter3D',
            data: this.chartData['label1'],
            symbolSize: symbolSize
          },
          {
            name: '簇2',
            type: 'scatter3D',
            data: this.chartData['label2'],
            symbolSize: symbolSize
          },
          {
            name: '簇3',
            type: 'scatter3D',
            data: this.chartData['label3'],
            symbolSize: symbolSize
          },
          {
            name: '簇4',
            type: 'scatter3D',
            data: this.chartData['label4'],
            symbolSize: symbolSize
          },
          {
            name: '簇5',
            type: 'scatter3D',
            data: this.chartData['label5'],
            symbolSize: symbolSize
          },
          {
            name: '簇6',
            type: 'scatter3D',
            data: this.chartData['label6'],
            symbolSize: symbolSize
          },
          {
            name: '簇7',
            type: 'scatter3D',
            data: this.chartData['label7'],
            symbolSize: symbolSize
          },
          {
            name: '簇8',
            type: 'scatter3D',
            data: this.chartData['label8'],
            symbolSize: symbolSize
          },
          {
            name: '簇9',
            type: 'scatter3D',
            data: this.chartData['label9'],
            symbolSize: symbolSize
          },
          {
            name: '簇10',
            type: 'scatter3D',
            data: this.chartData['label10'],
            symbolSize: symbolSize
          },
          {
            name: '簇11',
            type: 'scatter3D',
            data: this.chartData['label11'],
            symbolSize: symbolSize
          },
          {
            name: '簇12',
            type: 'scatter3D',
            data: this.chartData['label12'],
            symbolSize: symbolSize
          },
          {
            name: '簇13',
            type: 'scatter3D',
            data: this.chartData['label13'],
            symbolSize: symbolSize
          },
          {
            name: '簇14',
            type: 'scatter3D',
            data: this.chartData['label14'],
            symbolSize: symbolSize
          }
        ]
      })
    }
  }
}
</script>
