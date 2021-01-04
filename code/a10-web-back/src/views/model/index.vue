<template>
  <div class="dashboard-editor-container">
    <div style="margin-bottom:20px;">
      <h2>
        <strong>模型数据调整</strong>
      </h2>
      <small>调整模型参数权重</small>
    </div>
    <el-row :gutter="20">
      <el-col :span="8" :xs="24">&nbsp;</el-col>
      <el-col :span="8" :xs="24">
        <el-card>
          <el-form ref="form" :rules="rules" label-width="120px" :model="modelParas">
            <el-form-item label="风险权重" prop="risk_module_type">
              <el-input v-model="modelParas.risk_module_type" suffix-icon="el-icon-edit-outline" />
            </el-form-item>
            <el-form-item label="投资权重" prop="investment_module_type">
              <el-input v-model="modelParas.investment_module_type" suffix-icon="el-icon-edit-outline" />
            </el-form-item>
            <el-form-item label="知识产权权重" prop="creativity_module_type">
              <el-input v-model="modelParas.creativity_module_type" suffix-icon="el-icon-edit-outline" />
            </el-form-item>
            <el-form-item label="品牌权重" prop="brand_module_type">
              <el-input v-model="modelParas.brand_module_type" suffix-icon="el-icon-edit-outline" />
            </el-form-item>
            <el-form-item label="招聘权重" prop="recruit_module_type">
              <el-input v-model="modelParas.recruit_module_type" suffix-icon="el-icon-edit-outline" />
            </el-form-item>
            <el-form-item label="信用权重" prop="credit_module_type">
              <el-input v-model="modelParas.credit_module_type" suffix-icon="el-icon-edit-outline" />
            </el-form-item>
            <el-form-item label="基本信息权重" prop="base_module_type">
              <el-input v-model="modelParas.base_module_type" suffix-icon="el-icon-edit-outline" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit('form')">更新模型参数</el-button>
              <el-button @click="resetForm('form')">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
    <!-- <el-progress type="circle" :percentage="percentage" /> -->
  </div>
</template>

<script>
import { retrain, getModelParam } from '@/api/model'
export default {
  data() {
    return {
      modelParas: {
        risk_module_type: undefined,
        investment_module_type: undefined,
        creativity_module_type: undefined,
        brand_module_type: undefined,
        recruit_module_type: undefined,
        credit_module_type: undefined,
        base_module_type: undefined
      },
      rules: {
        risk_module_type: [
          { required: true, message: '请输入参数', trigger: 'change' }
        ],
        investment_module_type: [
          { required: true, message: '请输入参数', trigger: 'change' }
        ],
        creativity_module_type: [
          { required: true, message: '请输入参数', trigger: 'change' }
        ],
        brand_module_type: [
          { required: true, message: '请输入参数', trigger: 'change' }
        ],
        recruit_module_type: [
          { required: true, message: '请输入参数', trigger: 'change' }
        ],
        credit_module_type: [
          { required: true, message: '请输入参数', trigger: 'change' }
        ],
        base_module_type: [
          { required: true, message: '请输入参数', trigger: 'change' }
        ]
      }
      // percentage: 60
    }
  },
  watch: {
  },
  mounted() {
    this.initdata()
  },
  methods: {
    initdata() {
      getModelParam().then(resp => {
        this.modelParas = resp.data
      }).catch(err => {
        this.$message.error(err)
      })
    },
    onSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log('valid')
          retrain(this.modelParas).then(resp => {
            this.$notify({
              title: '训练成功',
              message: resp.message,
              type: 'success'
            })
          }).catch(err => {
            this.$message.error(err)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style lang="scss" scoped>
.chart-container{
  position: relative;
  width: 100%;
  height: calc(100vh - 84px);
}
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

