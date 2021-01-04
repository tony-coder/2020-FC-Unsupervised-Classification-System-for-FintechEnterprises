<template>
  <!-- el-container：外层容器。当子元素包含 <el-header> 或 <el-footer> 时，全部子元素会垂直上下排列，否则水平左右排列 -->
  <el-container>
    <el-alert title="暂不支持IE浏览器,请使用最新的谷歌或360浏览器！" center type="warning" description v-if="isIe"></el-alert>
    <!-- el-header：顶栏容器 -->
    <el-header height="0px">
      <!-- <el-col :span="12" class="logo">
        <img width="50px" height="50px" src="../../assets/index/logo.jpg" />
      </el-col>
      <el-col :span="12" class="header-right">
        <span>后台登录 | 注册</span>
      </el-col>-->
    </el-header>
    <!-- el-main：主要区域容器 -->
    <el-main>
      <!-- 搜索 -->
      <el-row class="search-box">
        <el-row>
          <el-col :span="20">
            &nbsp;
          </el-col>
          <el-col :span="4" class="header-right">
            <!-- <el-link :underline="false" href="https://element.eleme.io">后台登录</el-link> -->
            <a href="http://121.36.26.23:9528/#/dashboard/index">后台登录</a>
            <span> | </span>
            <el-button type = "text" @click="logindialogVisible = true" style="color: #fff;">登录</el-button>
            <span> | </span>
            <el-button type = "text" @click="registerdialogVisible = true" style="color: #fff;">注册</el-button>
          </el-col>
          <!-- <div class="block"><el-avatar :size="50" :src="circleUrl"></el-avatar></div> -->
        </el-row>
        <div class="search-col">
          <!-- 搜索框附近的背景图片 -->
          <img class="search-box-img animated pulse" src="../../assets/index/banner-font.png" />
          <!-- 搜索选项 -->
          <div class="search-box-type">
            <!-- @change当输入框失焦的时候触发 -->
            <el-radio-group v-model="radio" size="small" @change="handleTypeChange">
              <el-radio-button label="全部"></el-radio-button>
              <el-radio-button label="查企业"></el-radio-button>
              <el-radio-button label="查股东"></el-radio-button>
              <el-radio-button label="查老板"></el-radio-button>
              <el-radio-button label="联系方式"></el-radio-button>
              <el-radio-button label="批量查询"></el-radio-button>
            </el-radio-group>
          </div>
          <div class="search-box-input">
            <!-- Tooltip 文字提示,常用于展示鼠标 hover 时的提示信息 https://element.eleme.cn/#/zh-CN/component/tooltip -->
            <el-tooltip
              class="item"
              effect="dark"
              :content="tipword"
              placement="left"
              :manual="true"
              v-model="iptTip"
            >
              <!-- 
                autocomplete 是一个可带输入建议的输入框组件，fetch-suggestions 是一个返回输入建议的方法属性
                https://element.eleme.cn/#/zh-CN/component/input
              -->
              <el-autocomplete
                ref="searchIpt"
                class="search-ipt"
                :debounce="700"
                :trigger-on-focus="false"
                v-model="condition.key"
                :fetch-suggestions="querySearch"
                :placeholder="placeholder"
                @select="handleSelect"
                :autofocus="true"
              >
                <!-- 按钮 https://element.eleme.cn/#/zh-CN/component/button -->
                <!-- slot="append" 在输入框中嵌套按钮 append是在右边 prepend是在左边 -->
                <el-button
                  slot="append"
                  icon="el-icon-search"
                  class="search-btn"
                  @click="handlerSearch"
                >查一查</el-button>
                <!-- 使用scoped slot自定义输入建议的模板。该 scope 的参数为item，表示当前输入建议对象。 -->
                <template slot-scope="{ item }">
                  <div class="name" v-if="item.Field === 'enterpriseName'">
                    <span v-html="item.Value"></span>
                  </div>
                  <div class="name" v-else>
                    <span v-html="item.enterpriseName"></span>
                    <span style="float: right">
                      <el-popover placement="right" popper-class="my-tooltip" trigger="hover">
                        <span v-html="item.Value"></span>
                        <el-button
                          slot="reference"
                          type="primary"
                          size="mini"
                          plain
                        >{{item.Field | highlightFilter}}</el-button>
                      </el-popover>
                    </span>
                  </div>
                </template>
              </el-autocomplete>
            </el-tooltip>
            <!-- 验证码组件 -->
            <Captcha @valid="handleTcaptchaValid"></Captcha>
          </div>
        </div>
      </el-row>
      <!-- 特别功能 -->
      <el-row></el-row>
      <!-- 热搜 -->
      <el-row class="hot-search-row">
        <el-row :gutter="12" class="hot-search-div">
          <h2>热搜企业</h2>
          <!-- index:索引值;item:每一项 -->
          <el-col
            :span="8"
            v-for="(item,index) in hotList"
            :key="item.id"
            class="hot-search-col animated fadeInUp"
          >
            <el-card shadow="hover" class="hot-search-card" @click.native="hotEntSearch(item.id)">
              <el-col :span="6" class="xh">{{'企'+String(index+1).padStart(2,'0')}}</el-col>
              <el-col :span="18" class="content">
                <el-row class="name name-show">{{item.enterpriseName}}</el-row>
                <!-- <el-row class="person name-show">
                      法人代表：
                      <span>{{item.legalRepresentative}}</span>
                </el-row>-->
              </el-col>
            </el-card>
          </el-col>
        </el-row>
      </el-row>
      <!-- 按区域查询 -->
      <!-- <el-row class="area-search-row">
        <h2>按区域查询</h2>
        <el-row class="hot-city-row">
          <el-col :span="3"><el-button type="text" class="title">热门城市</el-button></el-col>
          <el-col :span="21">
              <el-col :span="8" v-for="i in Math.round(hotCity.length)" :key="i">
                <el-col :span="4" v-for="(item,index) in hotCity" :key="item.val" v-if="index>=6*(i-1) && index < 6*i">
                  <el-button type="text" class="area">{{item.name}}</el-button>
                </el-col>
              </el-col>
          </el-col>
        </el-row>
        <el-row class="hot-province-row">
          <el-col :span="3"><el-button type="text" class="title">按省份</el-button></el-col>
          <el-col :span="21">
            <el-col :span="8" v-for="i in Math.round(hotProvince.length)" :key="i">
              <el-col :span="4" v-for="(item,index) in hotProvince" :key="item.val" v-if="index>=6*(i-1) && index < 6*i">
                <el-button type="text" class="area">{{item.name}}</el-button>
              </el-col>
            </el-col>
          </el-col>
        </el-row>
      </el-row> -->
      <!-- 系统优势宣传 -->
      <el-row class="tip-row">
        <el-row class="notice">
          <el-col :span="8" class="notice-box">
            <el-col :span="6">
              <img src="../../assets/index/min-img01.png" />
            </el-col>
            <el-col :span="18">
              <el-row class="text-1">海量企业</el-row>
              <el-row class="text-2">千万家强企业信息，随时搜索查询</el-row>
            </el-col>
          </el-col>
          <el-col :span="8" class="notice-box second">
            <el-col :span="6" :offset="3">
              <img src="../../assets/index/min-img02.png" />
            </el-col>
            <el-col :span="15">
              <el-row class="text-1">权威来源</el-row>
              <el-row class="text-2">数据与权威网站同步，实时更新</el-row>
            </el-col>
          </el-col>
          <el-col :span="8" class="notice-box">
            <el-col :span="6" :offset="3">
              <img src="../../assets/index/min-img03.png" />
            </el-col>
            <el-col :span="15">
              <el-row class="text-1">多维信息</el-row>
              <el-row class="text-2">工商、关联、失信、多类信息齐全</el-row>
            </el-col>
          </el-col>
        </el-row>
      </el-row>
      <!-- 弹出框 -->
      <el-dialog title="上传文件" :visible.sync="dialogFormVisible" width="50%">
        <img src="../../assets/index/sample.png" width="700px" />
        <upload-excel-component :on-success="handleSuccess" :before-upload="beforeUpload" />
        下载Excel示例文件并填充企业名录信息上传文件不超过2M，仅支持Excel（csv、xlsx）
        <a href="http://121.36.13.179/static/example/%E6%A0%B7%E4%BE%8B.xlsx" download="sample.csv">Excel示例文件</a>
        <!-- <el-form>
          <el-upload ref="upload" 
            class="upload-demo"
            accept=".xml, .csv"
            :auto-upload="false" 
            :limit="3"
            drag
            :http-request="uploadFile"
            multiple
            :on-success="uploadSuccessHandle"
            :on-error="uploadFailHandle"
            action="uploadFile()"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              将文件拖到此处，或
              <em>点击上传</em>
            </div>
            <div
              class="el-upload__tip"
              slot="tip"
            >下载Excel示例文件并填充企业名录信息上传文件不超过2M，仅支持Excel（xls、xlsx）文件VIP单次免费查询数量为200家，超过需使用增值服务</div>
          </el-upload>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <span class="template-download">
            <i class="el-icon-download"></i>格式模板下载：data.xlsx
          </span>
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitUpload">确定上传</el-button>
        </span> -->
      </el-dialog>
      <el-dialog title="用户登录" :visible.sync="logindialogVisible" width="30%">
        <el-form>
          <el-form-item label="用户名" :label-width="formLabelWidth">
            <!-- <i class="el-icon-user"></i> -->
            <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" :label-width="formLabelWidth">
            <el-input v-model="form.password" show-password :type="'password'" placeholder="请输入密码"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="logindialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleLogin">登 录</el-button>
        </div>
    </el-dialog>
    <el-dialog title="用户注册" :visible.sync="registerdialogVisible" width="30%">
        <el-form>
          <el-form-item label="用户名" :label-width="formLabelWidth">
            <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" :label-width="formLabelWidth">
            <el-input v-model="form.password" show-password :type="'password'"  placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" :label-width="formLabelWidth">
            <el-input :type="'password'" v-model="form.checkPass" placeholder="请确认密码"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="registerdialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleRegister">注 册</el-button>
        </div>
    </el-dialog>
    </el-main>
    <!-- el-footer：底栏容器 -->
    <my-footer></my-footer>
  </el-container>
</template>

<script>
import { searchTip, searchHot } from '@/api/home'
import { isPhone, isTel } from '../../utils/validate'
import { isDisableWord, isIE } from '@/utils'
import Captcha from '@/components/TCaptcha' // 验证码组件
import store from '@/store'
import { highlightFilter } from '../../filters'
import constant from '@/common/constant'
import myFooter from './footer'
import axios from 'axios'
import UploadExcelComponent from '@/components/UploadExcel'

export default {
  name: 'index',
  components: {
    Captcha,
    myFooter,
    highlightFilter,
    UploadExcelComponent
  },
  // data: {

  // },
  data() {
    return {
      form: {
        username: '',
        password: '',
        checkPass: ''
      },
      // 默认选中全部
      radio: '全部',
      tipword: '请输入关键字',
      placeholder: '请输入企业名称、人名等关键词',
      id: '',
      showDetail: false, // 为显示详情
      // 当前状态（选中状态）
      condition: {
        key: '',
        keyword: '',
        searchType: '0',
        page: '1',
        rows: '5'
      },
      iptTip: false, // 是否显示提示 iptTip 置为true是显示提示；false时不显示
      // 热搜企业对象
      hotList: {},
      isIe: false,
      dialogFormVisible: false, // 是否显示对话框
      logindialogVisible: false, // 登录对话框
      registerdialogVisible: false, // 注册对话框
      multiSearchData: [], // 批量搜索数据
      formLabelWidth: '80px',
      hotCity: constant.hotCity,
      hotProvince: constant.hotProvince
    }
  },
  // Vue 的生命周期钩子 实例创建完成后调用 初始化处理数据
  created() {
    this.isIe = isIE()
    this.initHotInfo()
  },
  methods: {
    handlerSearch() {
      // 搜索关键词不为空
      if (this.condition.key.trim() !== '') {
        if (this.validKeyWord()) {
          this.showDetail = false
          this.$root.captcha.show() // 显示验证码
        } else {
          this.showTip() // 输入有问题 显示提示，延时1.5s
        }
      } else {
        this.showTip() // 输入为空 显示提示，延时1.5s
      }
    },
    showTip() {
      this.iptTip = true
      // setTimeout() 方法用于在指定的毫秒数后调用函数或计算表达式。
      setTimeout(() => {
        this.iptTip = false
      }, 1.5 * 1000)
    },
    // 验证验证码
    handleTcaptchaValid(res) {
      // 成功
      if (res.success) {
        console.log(res.success)
        // sessionStorage用于本地存储一个会话（session）中的数据，这些数据只有在同一个会话中的页面才能访问并且当会话结束后数据也随之销毁。
        // 因此sessionStorage不是一种持久化的本地存储，仅仅是会话级别的存储。
        sessionStorage.clear() // 清除所有本地sessionStorage
        sessionStorage.setItem('keyword', this.condition.keyword) // 添加sessionStorage 搜索关键词
        if (this.condition.searchType !== '0') {
          var enterpriseTags = []
          var scope = []
          var tag = {}
          tag.name = this.radio
          tag.val = this.condition.searchType
          tag.type = 'scope'
          enterpriseTags.push(tag)
          scope.push(this.condition.searchType)
          // 将当前信息储存到全局变量上
          sessionStorage.setItem(
            'enterpriseTags',
            JSON.stringify(enterpriseTags)
          )
          sessionStorage.setItem('scope', JSON.stringify(scope))
        }

        if (this.showDetail) {
          this.$router.push({ path: '/detail/' + this.id }) // 转到详情页面
        } else {
          this.$router.push({ path: '/list', params: { keyword: this.keyword }}) // 转到列表页面
        }
      }
    },
    // 处理搜索选择类型改变的事件
    handleTypeChange(val) {
      console.log(val)
      const type = {
        全部: '0',
        查企业: '1',
        查股东: '2',
        查老板: '3',
        联系方式: '4',
        批量查询: '5'
      }
      var currentType = type[val]
      switch (currentType) {
        case '0':
          this.placeholder = '请输入企业名称、人名等关键词'
          break
        case '1':
          this.placeholder = '请输入企业名称、注册号或统一社会信用代码'
          break
        case '2':
          this.placeholder = '请输入股东名称'
          this.radio = '全部'
          currentType = 0
          this.$message.error('由于数据不足，此功能暂未开放')
          break
        case '3':
          this.placeholder = '请输入老板名称'
          this.radio = '全部'
          currentType = 0
          this.$message.error('由于数据不足，此功能暂未开放')
          break
        case '4':
          this.placeholder = '请输入联系方式'
          this.radio = '全部'
          currentType = 0
          this.$message.error('由于数据不足，此功能暂未开放')
          break
        case '5':
          this.dialogFormVisible = true
          // var location = window.location.origin + '/batch';
          // window.open(location);
          this.radio = '全部'
          currentType = 0
          break
        default:
          this.placeholder = '请输入企业名称、人名等关键词'
      }
      this.condition.searchType = currentType // 设置当前搜索类型
      // 一般来讲，获取DOM元素，需document.querySelector（".input1"）获取这个dom节点，然后在获取input1的值。
      // 但是用ref绑定之后，我们就不需要在获取dom节点了，直接在上面的input上绑定input1，然后$refs里面调用就行。
      // 然后在javascript里面这样调用：this.$refs.input1 这样就可以减少获取dom节点的消耗了

      // ref="searchIpt"
      this.$refs.searchIpt._data.suggestions = [] // 清空建议框中的建议
      var vue = this
      this.$refs.searchIpt.fetchSuggestions(this.condition.key, function(data) {
        // 重新获取建议
        vue.$refs.searchIpt._data.suggestions = data
      })
      this.$refs.searchIpt.focus()
    },
    // 处理建议框中选中后的动作
    handleSelect(item) {
      this.id = item.id
      this.condition.keyword = item.enterpriseName
      this.condition.key = item.enterpriseName
      this.showDetail = true
      this.$root.captcha.show()
    },
    // 获取热搜企业列表
    initHotInfo() {
      // then()方法是异步执行。
      searchHot().then(response => {
        this.hotList = response.data.items
      })
    },
    // 点击热搜企业，跳转企业详情
    hotEntSearch(id) {
      this.$router.push({ path: '/detail/' + id })
    },
    // querySearch(queryString, cb)，在该方法中你可以在你的输入建议数据准备好时通过 cb(data) 返回到 autocomplete 组件中
    querySearch(queryString, cb) {
      // v-model="condition.key"
      if (this.condition.key.trim() !== '') {
        if (this.validKeyWord(this.condition.key)) {
          this.condition.keyword = this.condition.key.trim()
          // 测试使用
          // var result = [
          //   { highlightField: "enterpriseName", highlightValue: "test1" },
          //   { highlightField: "enterpriseName", highlightValue: "test2" },
          //   {
          //     highlightField: "legalRepresentative",
          //     highlightValue: "kkkk",
          //     enterpriseName: "test3"
          //   }
          // ];
          // cb(result);
          searchTip(this.condition)
            .then(response => {
              setTimeout(() => {
                cb(response.data)
              }, 1000 * 0.5)
            })
            .catch(err => {
              console.error(err)
              cb([])
            })
        } else {
          cb([])
          this.showTip()
        }
      } else {
        cb([])
      }
    },
    beforeUpload(file) {
      const isLt1M = file.size / 1024 / 1024 < 2
      if (isLt1M) {
        return true
      }
      this.$message({
        message: 'Please do not upload files larger than 1m in size.',
        type: 'warning'
      })
      return false
    },
    handleSuccess({ results, header }) {
      const tableData = results
      const tableHeader = header
      // console.log(tableData)
      // console.log(tableHeader)
      var head = tableHeader[0]
      for (var value of tableData) {
        console.log(value[head])
        this.multiSearchData.push(value[head])
      }
      console.log(this.multiSearchData)
      this.dialogFormVisible = false
      sessionStorage.clear()
      sessionStorage.setItem('multiEntList', JSON.stringify(this.multiSearchData))
      this.$router.push({ path: '/list', params: { keyword: this.keyword }}) // 转到列表页面
    },
    uploadSuccessHandle(e) {
      this.dialogFormVisible = false
    },
    uploadFailHandle(e) {
      this.$message.error('文件上传失败')
      // this.dialogFormVisible=false;
    },
    // 文件上传
    submitUpload() {
      this.$refs.upload.submit()
    },
    // 自定义文件上传方法
    uploadFile(params) {
      console.log('uploadFile', params)
      console.log('uploadFile', params.file)
      const _file = params.file
      const isLt2M = _file.size / 1024 / 1024 < 2
      // 通过 FormData 对象上传文件
      var formData = new FormData()
      formData.append('file', _file)
      console.log(formData.get('file'))

      if (!isLt2M) {
        this.$message.error('请上传2M以下的.xlsx文件')
        return false
      }
      // 发起请求
      // RequestUploads(formData).then(resp => {
      //   console.log('_RequestUploads_', resp)
      //   if (resp.code === 2000) {
      //     this.$message({
      //       type: 'success',
      //       message: resp.msg
      //     })
      //     // 隐藏弹出框
      //     this.dialogFormVisible = false
      //   } else {
      //     console.log('上传失败')
      //     this.$message({
      //       type: 'warning',
      //       message: resp.msg
      //     })
      //   }
      // })
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        transformRequest: [function(data) {
          return data
        }]
      }
      axios.post('/bfx/upload/', formData, config).then(
        function(response) { console.log(response) })
        .catch(function(error) {
          console.log(error)
        })
      // axios({
      //   method: 'post',
      //   url: '/bfx/upload',
      //   data: formData,
      //   headers: {
      //     'Content-Type': 'multipart/form-data' // 文件上传
      //     // 'Content-Type': 'application/x-www-form-urlencoded',  // 表单
      //     // 'Content-Type': 'application/json;charset=UTF-8'  // json
      //   }
      // }).then(function(response) {
      //   console.log(response)
      //   alert(response.data.message)
      // }).catch(function(reason) {

      // })
    },
    // 用户登录
    handleLogin() {
      console.log(this.form)
      if (this.form.username.trim() !== '' && this.form.password.trim() !== '') {
        this.$store.dispatch('Login', this.form).then(() => {
          // this.$router.push({ path: '/' }) // 重定向回主页
          this.$message({
            message: '登录成功',
            type: 'success'
          })
          this.logindialogVisible = false
        }).catch(err => {
          console.log(err)
          // this.$message.error('错了哦，这是一条错误消息')
          this.$message.error(err.message)
          this.form.username = ''
          this.form.password = ''
        })
      } else {
        this.$message.error('用户名或密码不允许为空')
      }
    },
    // 用户注册
    handleRegister() {
      if (this.form.username !== '' && this.form.password !== '' && this.form.checkPass !== '') {
        if (this.form.password !== this.form.checkPass) {
          this.form.username = ''
          this.form.password = ''
          this.form.checkPass = ''
          this.$message.error('前后两次密码输入不同，请重新输入')
          return false
        } else {
          this.$store.dispatch('Register', this.form).then(() => {
            this.$message({
              message: '注册成功',
              type: 'success'
            })
            this.logindialogVisible = false
          }).catch(err => {
            console.log(err)
            this.$message.error(err.message)
            this.form.username = ''
            this.form.password = ''
            this.form.checkPass = ''
          })
        }
      } else {
        this.$message.error('用户名或密码不允许为空')
      }
    },
    // 搜索关键字校验
    validKeyWord(key = this.condition.key.trim()) {
      switch (this.condition.searchType) {
        case '0':
          this.condition.key = key.replace(
            /[^\a-\z\A-\Z0-9\u4E00-\u9FA5\s\-\（\）]/g,
            ''
          )
          var newKeyWord = this.condition.key.replace(/[\s\-\（\）]/g, '')
          if (newKeyWord.length < 4) {
            if (
              !/^([\u4e00-\u9fa5]{2})$/.test(
                newKeyWord.replace(/[\a-\z\A-\Z0-9]/g, '')
              )
            ) {
              if (
                !/^([\u4e00-\u9fa5]{2,})|([A-Za-z0-9]{4,})$/.test(newKeyWord)
              ) {
                this.tipword = '请输入至少2个汉字或者4位数字字母'
                return false
              } else {
                if (isDisableWord(newKeyWord)) {
                  this.tipword = '搜索词太宽泛啦'
                  return false
                }
              }
            } else {
              if (isDisableWord(newKeyWord)) {
                this.tipword = '搜索词太宽泛啦'
                return false
              }
            }
          } else {
            if (isDisableWord(newKeyWord)) {
              this.tipword = '搜索词太宽泛啦'
              return false
            }
          }
          break
        case '1':
          this.condition.key = key.replace(
            /[^\a-\z\A-\Z0-9\u4E00-\u9FA5\s\（\）]/g,
            ''
          )
          newKeyWord = this.condition.key.replace(/[\s\-\（\）]/g, '')
          if (newKeyWord.length < 4) {
            if (
              !/^([\u4e00-\u9fa5]{2})$/.test(
                newKeyWord.replace(/[\a-\z\A-\Z0-9]/g, '')
              )
            ) {
              if (
                !/^([\u4e00-\u9fa5]{2,})|([A-Za-z0-9]{4,})$/.test(newKeyWord)
              ) {
                this.tipword = '请输入至少2个汉字或者4位数字字母'
                return false
              } else {
                if (isDisableWord(newKeyWord)) {
                  this.tipword = '搜索词太宽泛啦'
                  return false
                }
              }
            } else {
              if (isDisableWord(newKeyWord)) {
                this.tipword = '搜索词太宽泛啦'
                return false
              }
            }
          } else {
            if (isDisableWord(newKeyWord)) {
              this.tipword = '搜索词太宽泛啦'
              return false
            }
          }
          break
        case '2':
        case '3':
        case '4':
          this.condition.key = key.replace(
            /[^\a-\z\A-\Z0-9\u4E00-\u9FA5\s]/g,
            ''
          )
          if (!/^([\u4e00-\u9fa5\s]{2,20})$/.test(this.condition.key.trim())) {
            this.tipword = '请输入2-20个汉字'
            return false
          }
          break
        case '5':
          this.condition.key = key.replace(
            /[^\a-\z\A-\Z0-9\u4E00-\u9FA5\-]/g,
            ''
          )
          if (
            !isPhone(this.condition.key.trim()) &&
            !isTel(this.condition.key.trim())
          ) {
            this.tipword = '请输入正确的联系方式'
            return false
          }
          break
        default:
          return true
      }
      return true
    }
  },
  // 计算属性允许我们对指定的视图，复杂的值计算。这些值将绑定到依赖项值，只在需要时更新
  computed: {
    listenTcaptcha() {
      this.$store.state.captcha.tcaptcha
    }
  },
  // watch主要用于监控vue实例的变化，它监控的变量当然必须在data里面声明才可以，它可以监控一个变量，也可以是一个对象
  watch: {
    listenTcaptcha: function(native, overflow) {
      if (this.$store.state.captcha.tcaptcha) {
        store.dispatch('Tcaptcha', false)
      }
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.el-alert--warning {
  background-color: #dce7f3 !important;
  color: #409eff !important;
}
.el-width {
  width: 4.16667%;
}
.el-width1 {
  width: 5%;
}
.el-header {
  width: 1200px;
  margin: 0 auto;
  line-height: 54px;
  padding: 0;
  .logo {
    height: 100%;
    img {
      cursor: pointer;
    }
  }
  .header-right {
    text-align: right;
    color: #666666;
    font-size: 14px;
  }
}
.el-main {
  min-width: 1200px;
  padding: 0;
  .search-box {
    min-width: 1200px;
    height: 520px;
    max-width: 100%;
    margin: 0 auto;
    background: url("../../assets/index/banner-bg.png") no-repeat; //
    background-size: 100% 100%;
    text-align: center;
    .search-col {
      width: 680px;
      margin: 20px auto;
      img {
        margin: 5% 0 30px;
        width: 670px;
      }
      .search-box-input {
        margin: 10px auto;
        width: 90%;
        height: 48px;
        .search-ipt {
          height: 46px !important;
          width: 100%;
          background-color: rgba(255, 255, 255, 0.8);
          border-radius: 5px;
          .search-btn {
            border-left: 1px solid #e2e2e2;
            border-radius: 0;
            color: #3a71d8;
            font-weight: normal;
          }
        }
      }
    }
  }
  .hot-search-row {
    min-width: 1200px;
    background: #fff url("../../assets/index/qiye-bg-16.png") no-repeat bottom
      right; //
    max-width: 100%;
    padding-bottom: 80px;
    .hot-search-div {
      text-align: center;
      width: 1200px;
      margin: 0 auto !important;
      cursor: pointer;
      h2 {
        margin: 20px auto 40px;
        font-size: 24px;
        color: #333;
        font-weight: normal;
      }
      .hot-search-col {
        margin: 10px 0;
        height: 90px;
        .name-show {
          white-space: nowrap;
          text-overflow: ellipsis;
          overflow: hidden;
        }
        .hot-search-card {
          height: 100%;
          padding: 11px;
          .xh {
            height: 100%;
            line-height: 68px;
            font-size: 30px;
            color: #fe5054;
            font-weight: normal;
            text-align: center;
            border-right: 1px solid #e2e2e2;
          }
          .content {
            height: 100%;
            text-align: left;
            font-size: 14px;
            .name {
              margin: 10px;
            }
            .person {
              margin: 15px 10px 0;
              color: #999;
            }
          }
        }
      }
    }
  }
  .area-search-row {
    h2 {
      text-align: center;
      margin: 40px auto;
      font-size: 24px;
      color: #333;
      font-weight: normal;
    }
    .hot-city-row,
    .hot-province-row {
      width: 1200px;
      margin: 20px auto;
    }
    .hot-province-row {
      border-top: 1px solid #e2e2e2;
      padding-top: 20px;
    }
    .title {
      font-size: 16px;
      color: #3a71d8;
    }
    .area {
      color: #666;
    }
    .area:hover {
      color: #3a71d8;
      /*background: #3a71d8;*/
    }
  }
  .tip-row {
    margin-top: 30px;
    height: 160px;
    background: #ececec;
    .notice {
      width: 1200px;
      margin: 50px auto !important;
      height: 60px;
      .notice-box {
        height: 100%;
        .text-1 {
          height: 50%;
          font-weight: normal;
          font-size: 24px;
          color: #333;
          margin: 4px 0;
        }
        .text-2 {
          font-size: 14px;
          color: #666;
        }
      }
      .second {
        border-left: 1px solid #d4d4d4;
        border-right: 1px solid #d4d4d4;
      }
    }
  }
}
</style>
