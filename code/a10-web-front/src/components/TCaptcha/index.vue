<template>
  <div ref="captcha" id="Captcha" @callback="captchaCallback">
    <slot></slot>
  </div>
</template>

<script>
// import { tcapatcha, verify } from "@/api/validation/token";
// import { getToken, setToken } from '../../utils/auth'
// import { getIPs } from '../../utils'
import constant from '@/common/constant'
import store from '@/store'

export default {
  data() {
    return {
      appid: constant.tcaptcha.appid
    }
  },
  mounted() {
    if (typeof window.TencentCaptcha !== 'function') {
      const URL = 'https://ssl.captcha.qq.com/TCaptcha.js'
      const scriptHeat = document.createElement('script')
      scriptHeat.type = 'text/javascript'
      scriptHeat.src = URL
      document.body.appendChild(scriptHeat)
      scriptHeat.onload = () => {
        this.init()
      }
    } else {
      this.init()
    }
  },
  methods: {
    init() {
      // 手动初始化并绑定到一个元素
      // new TencentCaptcha(element, appId, callback, options);
      const captcha = new window.TencentCaptcha(
        this.$refs.captcha,
        this.appid,
        res => {
          // this.$emit('callback', res)
          this.captchaCallback(res)
        }
      )
      this.$root.captcha = captcha
      store.dispatch('Tcaptcha', true)
    },
    // 回调函数
    captchaCallback(res) {
      console.log(res)
      // var userIp
      var vue = this
      // userIp = getIPs();  // 该语句失效

      // 验证成功
      // ticket 验证成功的票据，当且仅当 ret = 0 时 ticket 有值
      if (res.ticket !== '') {
        const res = {}
        res.success = true
        vue.$emit('valid', res)
      } else {
        // 验证失败
        console.log('error')
        var resp = {}
        resp.success = false
        vue.$emit('valid', resp)
      }
    }
  }
}
</script>
