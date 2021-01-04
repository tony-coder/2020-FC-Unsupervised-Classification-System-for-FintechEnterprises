<template>
  <div>
    <el-table
      ref="filterTable"
      v-loading="loading"
      :data="tableData"
      style="width: 100%"
      height="250"
    >
      <el-table-column
        prop="date"
        label="id"
        sortable
        width="250"
        column-key="id"
      />
      <el-table-column
        prop="tag"
        label="标签"
        width="400"
        :filters="[{ text: '风险', value: '风险' }, { text: '投资', value: '投资' },{ text: '创新', value: '创新' },{ text: '品牌', value: '品牌' },{ text: '招聘', value: '招聘' },{ text: '信用', value: '信用' }]"
        :filter-method="filterTag"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag
            effect="plain"
            disable-transitions
          >{{ scope.row.tag }}</el-tag>
          <!-- <el-tag
            :type="scope.row.tag === '家' ? 'primary' : 'success'"
            disable-transitions
          >{{ scope.row.tag }}</el-tag> -->
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  props: {
    tableData: {
      type: Array,
      // default: function () { return [] }
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {

    }
  },
  methods: {
    filterTag(value, row) {
      return row.tag.slice(0, 1) === value
    }
  }
}
</script>
