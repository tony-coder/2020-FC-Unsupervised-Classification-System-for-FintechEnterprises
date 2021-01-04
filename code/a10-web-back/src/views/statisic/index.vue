<template>
  <div class="dashboard-editor-container">
    <div style="margin-bottom:20px;">
      <h2>
        <strong>统计数据参考</strong>
      </h2>
      <small>基于群体数据得出的统计学参考结果。</small>
    </div>
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-select v-model="clusterid" placeholder="请选择">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <dataset :key="timer" :chart-data="chardata" />
    </el-row>
    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="12">
        <div class="chart-wrapper">
          <barChart :key="timer" :mytitle="leftbartitle" :bardata="leftbardata" :xname="leftxname" :xlebal="leftxlebal" />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="12">
        <div class="chart-wrapper">
          <barChart :key="timer" :mytitle="rightbartitle" :bardata="rightbardata" :xname="rightxname" :xlebal="rightxlebal" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import dataset from '@/components/Dataset'
import barChart from '@/components/BarChart'
import { getchartdata, getbardata } from '@/api/statisic'
export default {
  components: {
    dataset,
    barChart
  },
  data() {
    return {
      leftbartitle: '企业等级总体分布',
      leftxname: '企业等级',
      leftbardata: [], // 3.38, 3.36, 8.92, 13.02, 11.87, 15.69, 24.89, 11.55, 4.79, 2.15, 0.38
      leftxlebal: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
      rightbartitle: '企业各簇百分比分布',
      rightbardata: [],
      rightxlebal: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
      rightxname: '簇编号',
      options: [{
        value: 0,
        label: '簇1'
      }, {
        value: 1,
        label: '簇2'
      }, {
        value: 2,
        label: '簇3'
      }, {
        value: 3,
        label: '簇4'
      }, {
        value: 4,
        label: '簇5'
      },
      {
        value: 5,
        label: '簇6'
      },
      {
        value: 6,
        label: '簇7'
      },
      {
        value: 7,
        label: '簇8'
      },
      {
        value: 8,
        label: '簇9'
      },
      {
        value: 9,
        label: '簇10'
      },
      {
        value: 10,
        label: '簇11'
      },
      {
        value: 11,
        label: '簇12'
      },
      {
        value: 12,
        label: '簇13'
      },
      {
        value: 13,
        label: '簇14'
      },
      {
        value: 14,
        label: '簇15'
      }
      ],
      clusterid: 0,
      chardata: {
        // 'dimensions': [],
        'source': []
      },
      mydata: undefined,
      entnum: 0,
      timer: ''
    }
  },
  watch: {
    clusterid(val) {
      // console.log(this.clusterid)
      this.changechart()
      this.timer = new Date().getTime()
    }
  },
  created() {
    this.initchart()
    this.initbardata()
  },
  methods: {
    initchart() {
      const data = {}
      data.id = this.clusterid
      getchartdata(data).then(resp => {
        console.log(resp)
        this.mydata = resp.data
        this.entnum = this.mydata[this.clusterid].ent_num
        var res = this.formatdata()
        console.log(res)
        this.chardata['source'] = res
        // this.chardata['dimensions'] = ['product', '等级0', '等级1', '等级2']
        this.timer = new Date().getTime()
      }).catch()
    },
    changechart() {
      this.entnum = this.mydata[this.clusterid].ent_num
      var res = this.formatdata()
      this.chardata['source'] = res
    },
    formatdata() {
      var res = []
      var tmpdata = this.mydata[this.clusterid]
      var tmp = []
      tmp = ['product', '风险', '投资', '创新', '品牌', '招聘', '信用', '资产', '总分']
      res.push(tmp)

      // tmp = this.solve(tmpdata, 0, '等级0')
      // res.push(tmp)
      tmp = this.solve(tmpdata, 1, '等级1')
      res.push(tmp)
      tmp = this.solve(tmpdata, 2, '等级2')
      res.push(tmp)
      tmp = this.solve(tmpdata, 3, '等级3')
      res.push(tmp)
      tmp = this.solve(tmpdata, 4, '等级4')
      res.push(tmp)
      tmp = this.solve(tmpdata, 5, '等级5')
      res.push(tmp)
      tmp = this.solve(tmpdata, 6, '等级6')
      res.push(tmp)
      tmp = this.solve(tmpdata, 7, '等级7')
      res.push(tmp)
      tmp = this.solve(tmpdata, 8, '等级8')
      res.push(tmp)
      tmp = this.solve(tmpdata, 9, '等级9')
      res.push(tmp)
      tmp = this.solve(tmpdata, 10, '等级10')
      res.push(tmp)

      return res
    },
    solve(data, index, target) {
      var tmp = []
      tmp.push(target)
      const title = ['risk_module_type', 'investment_module_type', 'creativity_module_type', 'brand_module_type',
        'recruit_module_type', 'credit_module_type', 'company_baseinfo_module_type', 'ent_type']
      for (var i = 0; i < title.length; i++) {
        tmp.push(data[title[i]][index])
      }
      return tmp
    },
    // formatdata() {
    //   var res = []
    //   var tmpdata = this.mydata[this.clusterid]
    //   var tmp = {}
    //   tmp = this.solve(tmpdata['risk_module_type'], '风险')
    //   res.push(tmp)
    //   tmp = this.solve(tmpdata['investment_module_type'], '投资')
    //   res.push(tmp)
    //   tmp = this.solve(tmpdata['creativity_module_type'], '创新')
    //   res.push(tmp)
    //   tmp = this.solve(tmpdata['brand_module_type'], '品牌')
    //   res.push(tmp)
    //   tmp = this.solve(tmpdata['recruit_module_type'], '招聘')
    //   res.push(tmp)
    //   tmp = this.solve(tmpdata['credit_module_type'], '信用')
    //   res.push(tmp)
    //   tmp = this.solve(tmpdata['company_baseinfo_module_type'], '基本')
    //   res.push(tmp)
    //   tmp = this.solve(tmpdata['ent_type'], '总分')
    //   res.push(tmp)
    //   console.log(res)

    //   return res
    // },
    // solve(data, target) {
    //   var tmp = {}
    //   tmp.product = target
    //   tmp.等级0 = data[0]
    //   tmp.等级1 = data[1]
    //   tmp.等级2 = data[2]
    //   tmp.等级3 = data[3]
    //   tmp.等级4 = data[4]
    //   tmp.等级5 = data[5]
    //   tmp.等级6 = data[6]
    //   tmp.等级7 = data[7]
    //   tmp.等级8 = data[8]
    //   tmp.等级9 = data[9]
    //   tmp.等级10 = data[10]
    //   return tmp
    // },
    initbardata() {
      getbardata().then(resp => {
        this.leftbardata = resp.leftbar
        this.rightbardata = resp.rightbar
        this.timer = new Date().getTime()
      })
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
