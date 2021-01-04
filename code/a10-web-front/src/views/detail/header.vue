<template>
  <div>
    <el-row class="list-header">
      <el-col :span="12" class="logo">
        <router-link to="/">
          <img src="../../assets/index/list-logo.png" width="120px" />
        </router-link>
      </el-col>
      <el-col :span="11" :offset="1" class="header-right">
        <el-tooltip
          class="item"
          effect="dark"
          :content="tipword"
          placement="left"
          :manual="true"
          v-model="iptTip"
        >
          <el-autocomplete
            :debounce="700"
            :placeholder="placeholder"
            :trigger-on-focus="false"
            class="searchtip-ipt"
            v-model="keyword"
            :fetch-suggestions="hadnleSearchTip"
            @select="handleSelect"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              class="search-btn"
              @click="handleShowCap"
            ></el-button>
            <template slot-scope="{ item }">
              <div class="name" v-if="item.highlightField === 'enterpriseName'">
                <span v-html="item.highlightValue"></span>
              </div>
              <div class="name" v-else>
                <span v-html="item.enterpriseName"></span>
                <span style="float: right">
                  <el-popover placement="right" popper-class="my-tooltip" trigger="hover">
                    <span v-html="item.highlightValue"></span>
                    <el-button
                      slot="reference"
                      type="primary"
                      size="mini"
                      plain
                    >{{item.highlightField | highlightFilter}}</el-button>
                  </el-popover>
                </span>
              </div>
            </template>
          </el-autocomplete>
        </el-tooltip>
        <Captcha @valid="handleTcaptchaValid"></Captcha>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { searchTip } from '@/api/home'
import Captcha from '@/components/TCaptcha'
import { highlightFilter } from '../../filters'

export default {
  filters: {
    highlightFilter
  },
  data() {
    return {
      keyword: '',
      iptTip: false,
      placeholder: '请输入企业名称、人名等关键词',
      showDetail: false,
      id: undefined,
      tipword: '请输入关键字'
    }
  },
  components: {
    Captcha
  },
  methods: {
    hadnleSearchTip(queryString, cb) {
      if (this.keyword.trim() !== '') {
        if (this.validKeyWord(this.keyword)) {
          const data = {}
          data.keyword = this.keyword.trim()
          data.page = 1
          data.rows = 5
          searchTip(data)
            .then(resp => {
              setTimeout(() => {
                cb(resp.rows)
              }, 1000 * 0.5)
            })
            .catch(err => {
              console.error(err)
              cb([])
            })
        } else {
          this.showTip()
          cb([])
        }
      } else {
        cb([])
      }
    },
    handleSelect(item) {
      this.id = item.id
      this.keyword = item.enterpriseName
      this.showDetail = true
      this.$root.captcha.show()
    },
    handleTcaptchaValid(resp) {
      if (resp.success) {
        sessionStorage.clear()
        // 验证用户状态是否过期
        // if (this.$store.state.user.expire) {
        //   location.reload()
        // } else {
        //   sessionStorage.setItem('keyword', this.keyword)
        //   if (this.showDetail) {
        //     this.$router.push({ path: '/detail/' + this.id })
        //     location.reload()
        //   } else {
        //     this.$router.push({ path: '/list', params: { key: this.keyword }})
        //   }
        // }
        sessionStorage.setItem('keyword', this.keyword)
        if (this.showDetail) {
          this.$router.push({ path: '/detail/' + this.id })
          location.reload()
        } else {
          this.$router.push({ path: '/list', params: { key: this.keyword }})
        }
      }
    },
    handleShowCap() {
      if (this.keyword !== '') {
        if (this.validKeyWord()) {
          this.showDetail = false
          this.$root.captcha.show()
        } else {
          this.showTip()
        }
      } else {
        this.showTip()
      }
    },
    validKeyWord(key = this.keyword) {
      this.keyword = key.replace(
        /[^\a-\z\A-\Z0-9\u4E00-\u9FA5\s\-\（\）]/g,
        ''
      )
      var newKeyWord = this.keyword.replace(/[\s\-\（\）]/g, '')
      if (newKeyWord.length < 4) {
        if (
          !/^([\u4e00-\u9fa5]{2})$/.test(
            newKeyWord.replace(/[\a-\z\A-\Z0-9]/g, '')
          )
        ) {
          if (!/^([\u4e00-\u9fa5]{2,})|([A-Za-z0-9]{4,})$/.test(newKeyWord)) {
            this.tipword = '请输入至少2个汉字或者4位字母'
            return false
          }
        }
      }
      return true
    },
    showTip() {
      this.iptTip = true
      setTimeout(() => {
        this.iptTip = false
      }, 1.5 * 1000)
    }
  },
  computed: {
    listenExpire() {
    //   return this.$store.state.user.expire
    }
  },
  watch: {
    listenExpire: function(nv, ov) {
    //   if (this.$store.state.user.expire) {
    //     this.$root.captcha.show()
    //   }
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.el-header {
  height: 55px;
  background: #3a71d8;
  min-width: 1200px;
  .list-header {
    height: 100%;
    max-width: 1200px;
    margin: 0 auto;
    .logo {
      height: 100%;
      line-height: 55px;
      img {
        vertical-align: middle;
      }
    }
    .header-right {
      line-height: 55px;
      .searchtip-ipt {
        width: 100%;
        height: 36px;
      }
    }
  }
}
</style>
