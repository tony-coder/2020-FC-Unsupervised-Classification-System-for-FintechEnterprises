// 储存全局使用的常量
const tcaptcha = {
  appid: 2015753454
}
// 查找范围
const scope = [
  { name: '企业名', val: '1' },
  { name: '股东', val: '2' },
  { name: '法人代表', val: '3' },
  { name: '联系方式', val: '4' }
]
// 企业类型
const type = [
  { name: '有限责任公司', val: '有限责任公司' },
  { name: '股份有限公司', val: '股份有限公司' },
  { name: '独资企业', val: '独资企业' },
  { name: '合伙制企业', val: '合伙制企业' },
  { name: '其他类型', val: '其他' }
]
// 企业状态
const status = [
  { name: '在业', val: '在业' },
  { name: '存续', val: '存续' },
  // { name: '筹建', val: '筹建' },
  // { name: '清算', val: '清算' },
  // { name: '迁入', val: '迁入' },
  { name: '迁出', val: '迁出' },
  // { name: '停业', val: '停业' },
  // { name: '撤销', val: '撤销' },
  { name: '吊销', val: '吊销' },
  { name: '注销', val: '注销' },
  { name: '其他状态', val: '其他' }
]
// 注册资本
const registfund = [
  { name: '500万以下', val: '0-500' },
  { name: '500-1000万', val: '500-1000' },
  { name: '1000-5000万', val: '1000-5000' },
  { name: '5000万以上', val: '5000-0' }
]
// 成立日期
const establishDate = [
]
getYear()
function getYear() {
  const year = new Date().getFullYear()
  for (let i = 0; i < 7; i++) {
    var data = {}
    data.name = (year - i).toString()
    data.val = (year - i).toString()
    establishDate.push(data)
  }
}
// 风险列表
const riskType = [
  { name: '行政处罚', val: '1' },
  { name: '经营异常', val: '2' },
  { name: '工商部失信', val: '3' },
  { name: '欠税', val: '4' },
  { name: '司法风险失信', val: '5' },
  { name: '股权出质登记', val: '6' }
]
// 企业风险查询时间列表
const dateScope = [
  { name: '一天内', val: 1 },
  { name: '一周内', val: 7 },
  { name: '一月内', val: 30 },
  { name: '一年内', val: 365 },
  { name: '两年内', val: 365 * 2 },
  { name: '三年内', val: 365 * 3 },
  { name: '四年内', val: 365 * 4 }
]

const riskTypeName = ['', '行政处罚', '经营异常', '工商部失信', '欠税', '司法风险失信', '股权出质登记']

const hotCity = [
  { name: '武汉', val: '420100' },
  { name: '无锡', val: '320200' },
  { name: '合肥', val: '340100' },
  { name: '福州', val: '350100' },
  { name: '济南', val: '370100' },
  { name: '南宁', val: '450100' },
  { name: '三亚', val: '460200' },
  { name: '海口', val: '460100' },
  { name: '郑州', val: '410100' },
  { name: '长沙', val: '430100' },
  { name: '厦门', val: '350200' },
  { name: '长春', val: '220100' },
  { name: '东莞', val: '441900' },
  { name: '佛山', val: '440600' },
  { name: '贵阳', val: '520100' },
  { name: '金华', val: '330700' },
  { name: '嘉兴', val: '330400' },
  { name: '昆明', val: '530100' },
  { name: '宁波', val: '330200' },
  { name: '南昌', val: '360100' },
  { name: '青岛', val: '370200' },
  { name: '泉州', val: '350500' },
  { name: '沈阳', val: '210100' },
  { name: '温州', val: '330300' }
]

const hotProvince = [
  { name: '北京', val: '110000' },
  { name: '上海', val: '310000' },
  { name: '天津', val: '120000' },
  { name: '重庆', val: '500000' },
  { name: '江苏', val: '320000' },
  { name: '广东', val: '440000' },
  { name: '河北', val: '130000' },
  { name: '河南', val: '410000' },
  { name: '安徽', val: '340000' },
  { name: '浙江', val: '330000' },
  { name: '福建', val: '350000' },
  { name: '甘肃', val: '620000' },
  { name: '广西', val: '450000' },
  { name: '贵州', val: '520000' },
  { name: '云南', val: '530000' },
  { name: '江西', val: '360000' },
  { name: '湖北', val: '420000' },
  { name: '四川', val: '510000' },
  { name: '宁夏', val: '640000' },
  { name: '青海', val: '630000' },
  { name: '山东', val: '370000' },
  { name: '陕西', val: '610000' },
  { name: '山西', val: '140000' },
  { name: '新疆', val: '650000' },
  { name: '西藏', val: '540000' },
  { name: '海南', val: '460000' },
  { name: '湖南', val: '430000' },
  { name: '黑龙江', val: '230000' },
  { name: '内蒙古', val: '150000' },
  { name: '吉林', val: '220000' },
  { name: '辽宁', val: '210000' },
  { name: '香港', val: '810000' }
]

export default {
  tcaptcha,
  scope,
  type,
  status,
  registfund,
  establishDate,
  riskType,
  dateScope,
  riskTypeName,
  hotCity,
  hotProvince
}
