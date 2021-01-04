<template>
  <el-container>
    <el-header height="54px">
      <el-row class="list-header">
        <!-- logo -->
        <el-col :span="12" class="logo">
          <router-link to="/">
            <img src="../../assets/index/list-logo.png" width="120px"/>
          </router-link>
        </el-col>
        <!-- 顶部搜索框 -->
        <el-col :span="11" :offset="1" class="header-right">
          <!-- ------搜索框------ -->
          <el-tooltip
            class="item"
            effect="dark"
            :content="tipword"
            placement="left"
            :manual="true"
            v-model="iptTip"
          >
            <el-autocomplete
              :placeholder="placeholder"
              :debounce="700"
              class="searchtip-ipt"
              v-model="keyword"
              :trigger-on-focus="false"
              :fetch-suggestions="querySearch"
              @select="handleSelect"
            >
              <el-button
                slot="append"
                icon="el-icon-search"
                class="search-btn"
                @click="handleShowCap"
              ></el-button>
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
          <Captcha @valid="handleTcaptchaValid"></Captcha>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-row class="content-row" :gutter="40">
        <!-- 页面左侧 -->
        <el-col :span="17" class="left-col">
          <!-- Tabs 标签页 分隔内容上有关联但属于不同类别的数据集合 https://element.eleme.cn/#/zh-CN/component/tabs -->
          <!-- 卡片化的标签页 -->
          <el-tabs type="border-card" v-model="activeTap" @tab-click="handleTabClick">
            <el-tab-pane name="first" label="企业">
              <!-- Card 卡片 将信息聚合在卡片容器中展示 https://element.eleme.cn/#/zh-CN/component/card -->
              <el-card class="box-card" shadow="never">
                <!-- Collapse 折叠面板 通过折叠面板收纳内容区域 https://element.eleme.cn/#/zh-CN/component/collapse -->
                <!-- 这里效果是当什么都没选时折叠已选条件框；当有条件选中时，展开已选条件框 -->
                <el-collapse-transition>
                  <div slot="header" class="tags-header" v-if="enterpriseTags.length>0">
                    <el-row>
                      <el-col :span="3">
                        <span>已选条件</span>
                      </el-col>
                      <el-col :span="19">
                        <!-- 循环打印所有已选选项标签 -->
                        <el-tag
                          v-for="tag in enterpriseTags"
                          :key="tag.name"
                          closable
                          @close="handleClose(tag,'enterpriseTags',true)"
                        >{{tag.name}}</el-tag>
                      </el-col>
                      <el-col :span="2">
                        <el-button
                          style="float: right; padding: 3px 0"
                          type="text"
                          class="clear-all"
                          @click="handleRemoveTag('','enterpriseTags')"
                        >全部清除</el-button>
                      </el-col>
                    </el-row>
                  </div>
                </el-collapse-transition>
                <!-- 这里是可折叠的搜索条件选择区 企业部分 -->
                <el-collapse-transition>
                  <!-- 当show1 为 true 时，显示该div -->
                  <div v-show="show1">
                    <!-- 查找范围 -->
                    <el-row class="cond-row">
                      <span>查找范围</span>
                      <el-button
                        type="text"
                        v-for="item in scopeList"
                        :key="item.key"
                        @click="handleAddTag(item,'scope','enterpriseTags')"
                      >{{item.name}}</el-button>
                    </el-row>
                    <!-- 下面选择框的效果为选中后即折叠，不允许多选 -->
                    <!-- 企业类型 -->
                    <transition name="slide-fade">
                      <!-- 当 企业类型 没有选中时显示 -->
                      <el-row class="cond-row" v-show="condition.type===undefined">
                        <span>企业类型</span>
                        <el-button
                          type="text"
                          v-for="item in typeList"
                          :key="item.val"
                          @click="handleAddTag(item,'type','enterpriseTags')"
                        >{{item.name}}</el-button>
                        <!-- Popover 弹出框 -->
                        <!-- v-model	状态是否可见 -->
                        <el-popover
                          placement="bottom"
                          width="180"
                          trigger="click"
                          v-model="entTypePop"
                        >
                          <el-form label-position="right" label-width="20px" size="mini">
                            <el-form-item label="企业类型">
                              <el-input clearable v-model="entType" type="text"></el-input>
                            </el-form-item>
                            <el-form-item>
                              <el-button
                                type="primary"
                                style="float: right"
                                @click="handleSubmitType"
                              >确定</el-button>
                            </el-form-item>
                          </el-form>
                          <el-button type="text" slot="reference">
                            自定义
                            <i class="el-icon-caret-bottom el-icon--right"></i>
                          </el-button>
                        </el-popover>
                      </el-row>
                    </transition>
                    <!-- 企业状态 -->
                    <transition name="slide-fade">
                      <el-row class="cond-row" v-show="condition.enterpriseStatus===undefined">
                        <span>企业状态</span>
                        <el-button
                          type="text"
                          v-for="item in statusList"
                          :key="item.val"
                          @click="handleAddTag(item,'enterpriseStatus','enterpriseTags')"
                        >{{item.name}}</el-button>
                      </el-row>
                    </transition>
                    <!-- 注册资本 -->
                    <transition name="slide-fade">
                      <el-row class="cond-row" v-show="condition.registeredCapitalNum===undefined">
                        <span>注册资本</span>
                        <el-button
                          type="text"
                          v-for="item in registfundList"
                          :key="item.val"
                          @click="handleAddTag(item,'registeredCapitalNum','enterpriseTags')"
                        >{{item.name}}</el-button>
                        <el-popover
                          placement="bottom"
                          width="180"
                          trigger="click"
                          v-model="registfundPop"
                        >
                          <el-form label-position="right" label-width="20px" size="mini">
                            <el-form-item label="从">
                              <el-input
                                suffix-icon="icon iconfont icon-wan"
                                clearable
                                v-model="registfund_begin"
                                type="number"
                              ></el-input>
                            </el-form-item>
                            <el-form-item label="至">
                              <el-input
                                suffix-icon="icon iconfont icon-wan"
                                clearable
                                v-model="registfund_end"
                                type="number"
                              ></el-input>
                            </el-form-item>
                            <el-form-item>
                              <el-button
                                type="primary"
                                style="float: right"
                                @click="handleSubmitRegistFund"
                              >确定</el-button>
                            </el-form-item>
                          </el-form>
                          <el-button type="text" slot="reference">
                            自定义
                            <i class="el-icon-caret-bottom el-icon--right"></i>
                          </el-button>
                        </el-popover>
                      </el-row>
                    </transition>
                    <!-- 成立日期 -->
                    <transition name="slide-fade">
                      <el-row class="cond-row" v-if="condition.dateOfEstablishment===undefined">
                        <span>成立日期</span>
                        <el-button
                          type="text"
                          v-for="item in establishDateList"
                          :key="item.val"
                          @click="handleAddTag(item,'dateOfEstablishment','enterpriseTags')"
                        >{{item.name}}</el-button>
                        <el-popover
                          placement="bottom"
                          width="180"
                          trigger="click"
                          v-model="establishPop"
                        >
                          <el-form label-position="right" label-width="20px" size="mini">
                            <el-form-item label="从">
                              <el-input
                                suffix-icon="icon iconfont icon-nian"
                                clearable
                                v-model="establish_begin"
                                type="number"
                              ></el-input>
                            </el-form-item>
                            <el-form-item label="至">
                              <el-input
                                suffix-icon="icon iconfont icon-nian"
                                clearable
                                v-model="establish_end"
                                type="number"
                              ></el-input>
                            </el-form-item>
                            <el-form-item>
                              <el-button
                                type="primary"
                                style="float: right"
                                @click="handleSubmitEstablish"
                              >确定</el-button>
                            </el-form-item>
                          </el-form>
                          <el-button type="text" slot="reference">
                            自定义
                            <i class="el-icon-caret-bottom el-icon--right"></i>
                          </el-button>
                        </el-popover>
                      </el-row>
                    </transition>
                  </div>
                </el-collapse-transition>
              </el-card>
            </el-tab-pane>
            <!-- <el-tab-pane name="second" label="风险信息">
              <el-card class="box-card" shadow="never">
                <el-collapse-transition>
                  <div slot="header" class="tags-header" v-if="riskTags.length>0">
                    <el-row>
                      <el-col :span="3">
                        <span>已选条件</span>
                      </el-col>
                      <el-col :span="19">
                        <el-tag
                          v-for="tag in riskTags"
                          :key="tag.name"
                          closable
                          @close="handleClose(tag,'riskTags',true)"
                        >{{tag.name}}</el-tag>
                      </el-col>
                      <el-col :span="2">
                        <el-button
                          style="float: right; padding: 3px 0"
                          type="text"
                          class="clear-all"
                          @click="handleRemoveTag('','riskTags')"
                        >全部清除</el-button>
                      </el-col>
                    </el-row>
                  </div>
                </el-collapse-transition> -->
                <!-- 这里是可折叠的搜索条件选择区 风险部分 -->
                <!-- <el-collapse-transition>
                  <div v-show="show2">
                    <transition name="slide-fade">
                      <el-row class="cond-row" v-if="condition.riskType===undefined">
                        <span>风险类型</span>
                        <el-button
                          type="text"
                          v-for="item in riskTypeList"
                          @click="handleAddTag(item,'riskType','riskTags')"
                          :key="item.val"
                        >{{item.name}}</el-button>
                      </el-row>
                    </transition>
                    <transition name="slide-fade">
                      <el-row class="cond-row" v-if="condition.dateScope===undefined">
                        <span>日&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;期</span>
                        <el-button
                          type="text"
                          v-for="item in dateScopeList"
                          :key="item.val"
                          @click="handleAddTag(item,'dateScope','riskTags')"
                        >{{item.name}}</el-button>
                      </el-row>
                    </transition>
                  </div>
                </el-collapse-transition>
              </el-card>
            </el-tab-pane> -->
            <el-tab-pane name="third" label="聚簇分类">
              <el-card class="box-card" shadow="never">
                <el-collapse-transition>
                  <div slot="header" class="tags-header" v-if="clusterTags.length>0">
                    <el-row>
                      <el-col :span="3">
                        <span>已选条件</span>
                      </el-col>
                      <el-col :span="19">
                        <el-tag
                          v-for="tag in clusterTags"
                          :key="tag.name"
                          closable
                          @close="handleClose(tag,'clusterTags',true)"
                        >{{tag.name}}</el-tag>
                      </el-col>
                      <el-col :span="2">
                        <el-button
                          style="float: right; padding: 3px 0"
                          type="text"
                          class="clear-all"
                          @click="handleRemoveTag('','clusterTags')"
                        >全部清除</el-button>
                      </el-col>
                    </el-row>
                  </div>
                </el-collapse-transition>
                <!-- 这里是可折叠的搜索条件选择区 聚簇分类部分 -->
                <el-collapse-transition>
                  <div v-show="show3">
                    <transition name="slide-fade">
                      <el-row class="cond-row">
                        <el-col :span="4">
                          <el-checkbox
                            v-model="riskRankChecked"
                            @change="handleCheckBoxChange('riskRank','riskRankList','riskRankChecked')"
                          ></el-checkbox>
                          <span>&nbsp;&nbsp;风险</span>
                        </el-col>
                        <!-- <span>风险</span> -->
                        <!-- <el-button type="text" v-for="item in riskRankList" @click="handleAddTag(item,'riskRank','clusterTags')" :key="item.val">{{item.name}}</el-button> -->
                        <el-col :span="20">
                          <el-slider
                            v-if="riskRankChecked===true"
                            v-model="riskRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('riskRank','riskRankList')"
                          ></el-slider>
                          <el-slider
                            v-else
                            disabled
                            v-model="riskRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('riskRank','riskRankList')"
                          ></el-slider>
                        </el-col>
                      </el-row>
                    </transition>
                    <transition name="slide-fade">
                      <el-row class="cond-row">
                        <el-col :span="4">
                          <el-checkbox
                            v-model="investmentRankChecked"
                            @change="handleCheckBoxChange('investmentRank','investmentRankList','investmentRankChecked')"
                          ></el-checkbox>
                          <span>&nbsp;&nbsp;投资</span>
                        </el-col>
                        <!-- <el-button type="text" v-for="item in investmentRankList" @click="handleAddTag(item,'investmentRank','clusterTags')" :key="item.val">{{item.name}}</el-button> -->
                        <el-col :span="20">
                          <el-slider
                            v-if="investmentRankChecked===true"
                            v-model="investmentRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('investmentRank','investmentRankList')"
                          ></el-slider>
                          <el-slider
                            v-else
                            disabled
                            v-model="investmentRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('investmentRank','investmentRankList')"
                          ></el-slider>
                        </el-col>
                      </el-row>
                    </transition>
                    <transition name="slide-fade">
                      <el-row class="cond-row">
                        <el-col :span="4">
                          <el-checkbox
                            v-model="creatityRankChecked"
                            @change="handleCheckBoxChange('creatityRank','creatityRankList','creatityRankChecked')"
                          ></el-checkbox>
                          <span>&nbsp;&nbsp;创新能力</span>
                        </el-col>
                        <!-- <el-button type="text" v-for="item in creatityRankList" @click="handleAddTag(item,'creatityRank','clusterTags')" :key="item.val">{{item.name}}</el-button> -->
                        <el-col :span="20">
                          <el-slider
                            v-if="creatityRankChecked===true"
                            v-model="creatityRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('creatityRank','creatityRankList')"
                          ></el-slider>
                          <el-slider
                            v-else
                            disabled
                            v-model="creatityRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                          ></el-slider>
                        </el-col>
                      </el-row>
                    </transition>
                    <transition name="slide-fade">
                      <el-row class="cond-row">
                        <el-col :span="4">
                          <el-checkbox
                            v-model="brandRankChecked"
                            @change="handleCheckBoxChange('brandRank','brandRankList','brandRankChecked')"
                          ></el-checkbox>
                          <span>&nbsp;&nbsp;品牌</span>
                        </el-col>
                        <!-- <el-button type="text" v-for="item in brandRankList" @click="handleAddTag(item,'brandRank','clusterTags')" :key="item.val">{{item.name}}</el-button> -->
                        <el-col :span="20">
                          <el-slider
                            v-if="brandRankChecked===true"
                            v-model="brandRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('brandRank','brandRankList')"
                          ></el-slider>
                          <el-slider
                            v-else
                            disabled
                            v-model="brandRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('brandRank','brandRankList')"
                          ></el-slider>
                        </el-col>
                      </el-row>
                    </transition>
                    <transition name="slide-fade">
                      <el-row class="cond-row">
                        <el-col :span="4">
                          <el-checkbox
                            v-model="recruitRankChecked"
                            @change="handleCheckBoxChange('recruitRank','recruitRankList','recruitRankChecked')"
                          ></el-checkbox>
                          <span>&nbsp;&nbsp;招聘</span>
                        </el-col>
                        <!-- <el-button type="text" v-for="item in recruitRankList" @click="handleAddTag(item,'recruitRank','clusterTags')" :key="item.val">{{item.name}}</el-button> -->
                        <el-col :span="20">
                          <el-slider
                            v-if="recruitRankChecked===true"
                            v-model="recruitRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('recruitRank','recruitRankList')"
                          ></el-slider>
                          <el-slider
                            v-else
                            disabled
                            v-model="recruitRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('recruitRank','recruitRankList')"
                          ></el-slider>
                        </el-col>
                      </el-row>
                    </transition>
                    <transition name="slide-fade">
                      <el-row class="cond-row">
                        <el-col :span="4">
                          <el-checkbox
                            v-model="creditRankChecked"
                            @change="handleCheckBoxChange('creditRank','creditRankList','creditRankChecked')"
                          ></el-checkbox>
                          <span>&nbsp;&nbsp;信用</span>
                        </el-col>
                        <!-- <el-button type="text" v-for="item in creditRankList" @click="handleAddTag(item,'creditRank','clusterTags')" :key="item.val">{{item.name}}</el-button> -->
                        <el-col :span="20">
                          <el-slider
                            v-if="creditRankChecked===true"
                            v-model="creditRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('creditRank','creditRankList')"
                          ></el-slider>
                          <el-slider
                            v-else
                            disabled
                            v-model="creditRankList"
                            range
                            show-stops
                            :min="0"
                            :max="10"
                            :marks="marks"
                            @change="handleSliderChange('creditRank','creditRankList')"
                          ></el-slider>
                        </el-col>
                      </el-row>
                    </transition>
                  </div>
                </el-collapse-transition>
              </el-card>
            </el-tab-pane>
          </el-tabs>
          <div v-show="activeTap === 'first'" class="list-l-topbk">
            <div class="sq" @click="show1 = !show1">
              <a>
                {{show1?'收起':'展开'}}
                <i :class="[show1 ? 'el-icon-arrow-up':'el-icon-arrow-down']"></i>
              </a>
            </div>
          </div>
          <!-- <div v-if="activeTap === 'second'" class="list-l-topbk">
            <div class="sq" @click="show2 = !show2">
              <a>
                {{show2?'收起':'展开'}}
                <i :class="[show2 ? 'el-icon-arrow-up':'el-icon-arrow-down']"></i>
              </a>
            </div>
          </div> -->
          <div v-if="activeTap === 'third'" class="list-l-topbk">
            <div class="sq" @click="show3 = !show3">
              <a>
                {{show2?'收起':'展开'}}
                <i :class="[show3 ? 'el-icon-arrow-up':'el-icon-arrow-down']"></i>
              </a>
            </div>
          </div>
          <!-- 显示数据 -->
          <!-- 使用v-loading在接口为请求到数据之前，显示加载中，直到请求到数据后消失 -->
          <el-card
            v-if="activeTap === 'first'"
            class="list-card animated fadeInLeft"
            shadow="never"
            v-loading="loading"
          >
            <div class="totla-text">
              为您找到了
              <span>{{companyTotal>100?companyTotal+'+':companyTotal}}</span> 家符合条件的企业
              <el-button size="mini" style="float:right;text-align: center" type="primary" plain @click="handleCompare">对比</el-button>
            </div>
            <el-card shadow="never">
              <div slot="header" class="result-title">
                <span>公司名称</span>
                <el-col :span="3" style="float:right;text-align: center">状态</el-col>
              </div>

              <el-checkbox-group v-model="checkList" :max="5" @change="handleCheckedEntChange">
                <el-row class="result-list" v-for="item in enterpriseList" :key="item.id">
                  <el-checkbox :label="item.id"></el-checkbox>
                  <!-- <el-col :span="1">
                      <el-checkbox v-model="item.id" style="margin-top:120px;float:right" size="medium" @change="handleCheckedEntChange(item.id)"></el-checkbox>
                  </el-col> -->
                  <!-- 点击进入企业详情 -->
                  <div @click="showDetailPage(item.id)">
                    <!-- 企业照片 默认 -->
                    <el-col :span="5" class="company-img">
                      <img src="../../assets/index/list-img.png" />
                    </el-col>
                    <el-col :span="11" class="company-content">
                      <el-row>
                        <h2>{{item.enterpriseName | showLine}}</h2>
                      </el-row>
                      <!-- 标签 -->
                      <el-row >
                        <!-- 风险 -->
                        <el-col :span="5" class="bj-img2" v-if="item.riskRank==10">
                          <el-tag type="danger">极高风险</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.riskRank>=7 && item.riskRank<=9">
                          <el-tag type="warning">高风险</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.riskRank>=4 && item.riskRank<=6">
                          <el-tag type="info">中等风险</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.riskRank!=null && item.riskRank<=3 && item.riskRank>0">
                          <el-tag type="success">低风险</el-tag>
                        </el-col>
                        <!-- 投资水平 -->
                        <el-col :span="6" class="bj-img2" v-if="item.investmentRank!=null && item.investmentRank<=3 && item.investmentRank>0">
                          <el-tag type="danger">低投资水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.investmentRank>=4 && item.investmentRank<=6">
                          <el-tag type="warning">中等投资水平</el-tag>
                        </el-col>
                        <el-col :span="6" class="bj-img2" v-if="item.investmentRank>=7 && item.investmentRank<=9">
                          <el-tag type="info">高投资水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.investmentRank==10">
                          <el-tag type="success">极高投资水平</el-tag>
                        </el-col>
                        <!-- 创新水平 -->
                        <el-col :span="6" class="bj-img2" v-if="item.creativityRank!=null && item.creativityRank<=3 && item.creativityRank>0">
                          <el-tag type="danger">低创新水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.creativityRank>=4 && item.creativityRank<=6">
                          <el-tag type="warning">中等创新水平</el-tag>
                        </el-col>
                        <el-col :span="6" class="bj-img2" v-if="item.creativityRank>=6 && item.creativityRank<=9">
                          <el-tag type="info">高创新水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.creativityRank==10">
                          <el-tag type="success">极高创新水平</el-tag>
                        </el-col>
                        <!-- 品牌水平 -->
                        <el-col :span="6" class="bj-img2" v-if="item.brandRank!=null && item.brandRank<=3 && item.brandRank>0">
                          <el-tag type="danger">低品牌水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.brandRank>=4 && item.brandRank<=6">
                          <el-tag type="warning">中等品牌水平</el-tag>
                        </el-col>
                        <el-col :span="6" class="bj-img2" v-if="item.brandRank>=7 && item.brandRank<=9">
                          <el-tag type="info">高品牌水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.brandRank==10">
                          <el-tag type="success">极高品牌水平</el-tag>
                        </el-col>
                        <!-- 用人需求 -->
                        <el-col :span="6" class="bj-img2" v-if="item.recruitRank!=null && item.recruitRank<=3 && item.recruitRank>0">
                          <el-tag type="danger">低用人需求</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.recruitRank>=4 && item.recruitRank<=6">
                          <el-tag type="warning">中等用人需求</el-tag>
                        </el-col>
                        <el-col :span="6" class="bj-img2" v-if="item.recruitRank>=7 && item.recruitRank<=9">
                          <el-tag type="info">高用人需求</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.recruitRank==10">
                          <el-tag type="success">极高用人需求</el-tag>
                        </el-col>
                        <!-- 信用 -->
                        <el-col :span="5" class="bj-img2" v-if="item.creditRank!=null && item.creditRank<=3 && item.creditRank>0">
                          <el-tag type="danger">低信用</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.creditRank>=4 && item.creditRank<=6">
                          <el-tag type="warning">中等信用</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.creditRank>=7 && item.creditRank<=9">
                          <el-tag type="info">高信用</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.creditRank==10">
                          <el-tag type="success">极高信用</el-tag>
                        </el-col>
                        <!-- 资产 -->
                        <el-col :span="5" class="bj-img2" v-if="item.baseRank!=null && item.baseRank<=3 && item.baseRank>0">
                          <el-tag type="danger">低资产</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.baseRank>=4 && item.baseRank<=6">
                          <el-tag type="warning">中等资产</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.baseRank>=7 && item.baseRank<=9">
                          <el-tag type="info">高资产</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.baseRank==10">
                          <el-tag type="success">极高资产</el-tag>
                        </el-col>
                      </el-row>
                      <el-row>
                        <span>
                          法人代表：
                          <span>{{item.legalRepresentative | showLine}}</span>
                        </span>
                      </el-row>
                      <el-row>
                        <el-col :span="12">
                          <span>
                            注册资本：{{item.registeredCapital | showLine}}
                            <span
                              v-if="item.registeredCapital"
                            >万人民币</span>
                          </span>
                        </el-col>
                        <el-col :span="12">
                          <span>
                            电话：
                            <span>{{item.phoneNumber | showLine}}</span>
                          </span>
                        </el-col>
                      </el-row>
                      <el-row>
                        <el-col :span="12">
                          <span>成立时间：{{item.dateOfEstablishment | showLine}}</span>
                        </el-col>
                        <el-col :span="12">
                          <span>
                            邮箱：
                            <span>{{item.email | showLine}}</span>
                          </span>
                        </el-col>
                      </el-row>
                      <el-row>
                        <span>地址：{{item.address | showLine}}</span>
                      </el-row>
                    </el-col>
                    <el-col :span="7">
                      <RaddarChart
                      v-bind:tagRankList=item.tagRankList
                      v-bind:enterpriseName=item.enterpriseName
                      >
                      </RaddarChart>
                    </el-col>
                  </div>
                </el-row>
              </el-checkbox-group>
              <el-row v-if="companyTotal===0" class="result-list">
                <div class="no-data">未查询到符合条件的企业</div>
              </el-row>
            </el-card>
            <el-row class="page-row" v-show="companyTotal>condition.rows">
              <!-- Pagination 分页 当数据量过多时，使用分页分解数据 https://element.eleme.cn/#/zh-CN/component/pagination-->
              <el-pagination
                :current-page="condition.page"
                background
                small="small"
                :page-size="condition.rows"
                layout="prev, pager, next"
                @current-change="handleCurrentChange"
                :total="companyTotal"
              ></el-pagination>
            </el-row>
          </el-card>
          <!-- <el-card
            v-if="activeTap === 'second'"
            class="list-card animated fadeInLeft"
            shadow="never"
            v-loading="loading"
          >
            <div class="totla-text">
              为您找到了
              <span>{{riskTotal>100 ? riskTotal+'+':riskTotal}}</span> 家符合条件的企业
            </div>
            <el-card shadow="never">
              <div slot="header" class="result-title">
                <span>公司名称</span>
                <el-col :span="3" style="float:right;text-align: center">状态</el-col>
              </div>
              <el-row class="result-list" v-for="item in riskList" :key="item.id">
                <div @click="showDetailPage(item.id,'businessRisk')">
                  <el-col :span="21" class="company-content" style="padding-left: 20px">
                    <div>
                      <el-row>
                        <el-col :span="12">
                          <span>企业名称：{{item.enterpriseName | showLine}}</span>
                        </el-col>
                        <el-col :span="12" class="jg-col">
                          <span>注册资本：{{item.registeredCapital | showLine}}</span>
                        </el-col>
                      </el-row>
                      <el-row>
                        <el-col :span="12">
                          <span>成立日期：{{item.dateOfEstablishment | showLine}}</span>
                        </el-col>
                      </el-row>
                    </div>
                  </el-col>
                  <el-col :span="3" class="company-status">
                    <el-tag type="danger" class="company-tag">{{riskTypeName[item.type]}}</el-tag>
                  </el-col>
                </div>
              </el-row>
              <el-row v-if="riskTotal===0" class="result-list">
                <div class="no-data">未查询到符合条件的企业</div>
              </el-row>
            </el-card>
            <el-row class="page-row" v-show="riskTotal>riskCondition.rows">
              <el-pagination
                :current-page="riskCondition.page"
                background
                small="small"
                :page-size="riskCondition.rows"
                layout="prev, pager, next"
                @current-change="handleCurrentChange"
                :total="riskTotal"
              ></el-pagination>
            </el-row>
          </el-card> -->
          <el-card
            v-if="activeTap === 'third'"
            class="list-card animated fadeInLeft"
            shadow="never"
            v-loading="loading"
          >
            <div class="totla-text">
              为您找到了
              <span>{{clusterTotal>100?clusterTotal+'+':clusterTotal}}</span> 家符合条件的企业
            </div>
            <el-card shadow="never">
              <div slot="header" class="result-title">
                <span>公司名称</span>
                <el-col :span="3" style="float:right;text-align: center">状态</el-col>
              </div>
              <el-row class="result-list" v-for="item in clusterList" :key="item.id">
                <!-- 点击进入企业详情 -->
                <div @click="showDetailPage(item.id)">
                  <!-- 企业照片 默认 -->
                  <el-col :span="6" class="company-img">
                    <img src="../../assets/index/list-img.png" />
                  </el-col>
                  <el-col :span="11" class="company-content">
                    <el-row>
                      <h2>{{item.enterpriseName | showLine}}</h2>
                    </el-row>
                    <!-- 标签 -->
                      <el-row >
                        <!-- 风险 -->
                        <el-col :span="5" class="bj-img2" v-if="item.riskRank==10">
                          <el-tag type="danger">极高风险</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.riskRank>=7 && item.riskRank<=9">
                          <el-tag type="warning">高风险</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.riskRank>=4 && item.riskRank<=6">
                          <el-tag type="info">中等风险</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.riskRank!=null && item.riskRank<=3 && item.riskRank>0">
                          <el-tag type="success">低风险</el-tag>
                        </el-col>
                        <!-- 投资水平 -->
                        <el-col :span="6" class="bj-img2" v-if="item.investmentRank!=null && item.investmentRank<=3 && item.investmentRank>0">
                          <el-tag type="danger">低投资水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.investmentRank>=4 && item.investmentRank<=6">
                          <el-tag type="warning">中等投资水平</el-tag>
                        </el-col>
                        <el-col :span="6" class="bj-img2" v-if="item.investmentRank>=7 && item.investmentRank<=9">
                          <el-tag type="info">高投资水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.investmentRank==10">
                          <el-tag type="success">极高投资水平</el-tag>
                        </el-col>
                        <!-- 创新水平 -->
                        <el-col :span="6" class="bj-img2" v-if="item.creativityRank!=null && item.creativityRank<=3 && item.creativityRank>0">
                          <el-tag type="danger">低创新水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.creativityRank>=4 && item.creativityRank<=6">
                          <el-tag type="warning">中等创新水平</el-tag>
                        </el-col>
                        <el-col :span="6" class="bj-img2" v-if="item.creativityRank>=6 && item.creativityRank<=9">
                          <el-tag type="info">高创新水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.creativityRank==10">
                          <el-tag type="success">极高创新水平</el-tag>
                        </el-col>
                        <!-- 品牌水平 -->
                        <el-col :span="6" class="bj-img2" v-if="item.brandRank!=null && item.brandRank<=3 && item.brandRank>0">
                          <el-tag type="danger">低品牌水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.brandRank>=4 && item.brandRank<=6">
                          <el-tag type="warning">中等品牌水平</el-tag>
                        </el-col>
                        <el-col :span="6" class="bj-img2" v-if="item.brandRank>=7 && item.brandRank<=9">
                          <el-tag type="info">高品牌水平</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.brandRank==10">
                          <el-tag type="success">极高品牌水平</el-tag>
                        </el-col>
                        <!-- 用人需求 -->
                        <el-col :span="6" class="bj-img2" v-if="item.recruitRank!=null && item.recruitRank<=3 && item.recruitRank>0">
                          <el-tag type="danger">低用人需求</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.recruitRank>=4 && item.recruitRank<=6">
                          <el-tag type="warning">中等用人需求</el-tag>
                        </el-col>
                        <el-col :span="6" class="bj-img2" v-if="item.recruitRank>=7 && item.recruitRank<=9">
                          <el-tag type="info">高用人需求</el-tag>
                        </el-col>
                        <el-col :span="7" class="bj-img2" v-if="item.recruitRank==10">
                          <el-tag type="success">极高用人需求</el-tag>
                        </el-col>
                        <!-- 信用 -->
                        <el-col :span="5" class="bj-img2" v-if="item.creditRank!=null && item.creditRank<=3 && item.creditRank>0">
                          <el-tag type="danger">低信用</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.creditRank>=4 && item.creditRank<=6">
                          <el-tag type="warning">中等信用</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.creditRank>=7 && item.creditRank<=9">
                          <el-tag type="info">高信用</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.creditRank==10">
                          <el-tag type="success">极高信用</el-tag>
                        </el-col>
                        <!-- 资产 -->
                        <el-col :span="5" class="bj-img2" v-if="item.baseRank!=null && item.baseRank<=3 && item.baseRank>0">
                          <el-tag type="danger">低资产</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.baseRank>=4 && item.baseRank<=6">
                          <el-tag type="warning">中等资产</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.baseRank>=7 && item.baseRank<=9">
                          <el-tag type="info">高资产</el-tag>
                        </el-col>
                        <el-col :span="5" class="bj-img2" v-if="item.baseRank==10">
                          <el-tag type="success">极高资产</el-tag>
                        </el-col>
                      </el-row>
                    <el-row>
                      <span>
                        法人代表：
                        <span>{{item.legalRepresentative | showLine}}</span>
                      </span>
                    </el-row>
                    <el-row>
                      <el-col :span="12">
                        <span>
                          注册资本：{{item.registeredCapital | showLine}}
                          <span
                            v-if="item.registeredCapital"
                          >万人民币</span>
                        </span>
                      </el-col>
                      <el-col :span="12">
                        <span>
                          电话：
                          <span>{{item.phoneNumber | showLine}}</span>
                        </span>
                      </el-col>
                    </el-row>
                    <el-row>
                      <el-col :span="12">
                        <span>成立时间：{{item.dateOfEstablishment | showLine}}</span>
                      </el-col>
                      <el-col :span="12">
                        <span>
                          邮箱：
                          <span>{{item.email | showLine}}</span>
                        </span>
                      </el-col>
                    </el-row>
                    <el-row>
                      <span>地址：{{item.address | showLine}}</span>
                    </el-row>
                  </el-col>
                  <el-col :span="7">
                    <RaddarChart
                    v-bind:tagRankList=item.tagRankList
                    v-bind:enterpriseName=item.enterpriseName
                    ></RaddarChart>
                  </el-col>
                </div>
              </el-row>
              <el-row v-if="clusterTotal===0" class="result-list">
                <div class="no-data">未查询到符合条件的企业</div>
              </el-row>
            </el-card>
            <el-row class="page-row" v-show="clusterTotal>clusterCondition.rows">
              <!-- Pagination 分页 当数据量过多时，使用分页分解数据 https://element.eleme.cn/#/zh-CN/component/pagination-->
              <el-pagination
                :current-page="clusterCondition.page"
                background
                small="small"
                :page-size="clusterCondition.rows"
                layout="prev, pager, next"
                @current-change="handleCurrentChange"
                :total="clusterTotal"
              ></el-pagination>
            </el-row>
          </el-card>
        </el-col>
        <!-- 页面右侧 -->
        <el-col :span="7" class="right-col">
          <el-row>
            <img src="../../assets/index/details-img01.png" alt />
          </el-row>
        </el-col>
        <!-- 工具栏模块 -->
        <el-tooltip placement="top" content="返回顶部">
          <back-to-top
            :custom-style="myBackToTopStyle"
            :visibility-height="300"
            :back-position="0"
            transition-name="fade"
          />
        </el-tooltip>
      </el-row>
      <el-dialog title="对比图" :visible.sync="dialogFormVisible" width="60%" height="100%">
        <bar-chart :EntList="compareEntList" :key="timer"></bar-chart>
      </el-dialog>
    </el-main>
    <my-footer></my-footer>
  </el-container>
</template>

<script>
import { search, searchTip, searchRisk, searchCluster } from '@/api/home'
import { searchCompareEntInfo } from '@/api/detail'
import _ from 'lodash' // 引入lodash Lodash 是一个一致性、模块化、高性能的 JavaScript 实用工具库 https://www.lodashjs.com/
import constant from '@/common/constant'
import { showLine } from '../../filters'
import myFooter from '@/views/home/footer'
import { myBackToTopStyle } from '@/utils'
import BackToTop from '@/components/BackToTop'
import RaddarChart from './RaddarChart'
import store from '@/store'
import Captcha from '@/components/TCaptcha'
import BarChart from './BarChart'

export default {
  components: {
    myFooter,
    RaddarChart,
    BackToTop,
    Captcha,
    showLine,
    BarChart
  },
  data() {
    return {
      checkList: [],
      marks: {
        1: '低',
        2: '较低',
        3: '中等',
        4: '较高',
        5: '高'
      },
      placeholder: '请输入企业名称、人名等关键词', // 搜索提示
      activeTap: 'first', // 选中的tab
      show1: true,
      show2: true,
      show3: true,
      // 在data 中定义初始化，loading: false，同时在mounted()中将 this.loading设置为true
      // 再去请求接口在接口的回调函数中，将 this.loading 设为false，到达效果
      loading: false,
      keyword: undefined,
      multiEntList: [],
      scope: new Set([]), // 储存查找范围选中tag，因为查找范围可多选
      // 企业
      scopeList: constant.scope, // 查找范围选择列表
      typeList: constant.type, // 企业类型选择列表
      statusList: constant.status, // 企业状态选择列表
      registfundList: constant.registfund, // 注册资本选择列表
      establishDateList: constant.establishDate, // 成立日期选择列表
      // 风险
      riskTypeList: constant.riskType, // 风险类型选择列表
      riskTypeName: constant.riskTypeName, // 风险标签
      dateScopeList: constant.dateScope, // 企业风险查询时间选择列表
      // 聚簇分类
      riskRankList: [0, 10], // 企业风险等级选择列表
      investmentRankList: [0, 10], // 投资等级选择列表
      creatityRankList: [0, 10], // 创新能力等级选择列表
      brandRankList: [0, 10], // 品牌等级选择列表
      recruitRankList: [0, 10], // 招聘等级选择列表
      creditRankList: [0, 10], // 信用等级选择列表

      riskRankChecked: true, // 选中风险等级
      investmentRankChecked: true, // 选中投资等级
      creatityRankChecked: true, // 选中创新能力等级
      brandRankChecked: true, // 选中品牌等级
      recruitRankChecked: true, // 选中招聘等级
      creditRankChecked: true, // 选中信用等级

      // 企业搜索属性
      condition: {
        // searchtype: 'ent',  // 搜索类型
        keyword: undefined, // 关键词
        multiEntList: [],
        // 企业查询
        searchType: [], // 选中的查找范围
        type: undefined, // 企业类型
        enterpriseStatus: undefined, // 企业状态
        registeredCapitalNum: undefined, // 注册资金
        dateOfEstablishment: undefined, // 成立时间
        // provinceCode: undefined,  // 所在省的编码
        riskType: undefined, // 风险类型
        dateScope: undefined, // 执行日期
        page: 1,
        rows: 10
      },
      // 风险搜索属性
      riskCondition: {
        // searchtype: 'risk',  // 搜索类型
        keyword: undefined,
        multiEntList: [],
        type: undefined, // 风险类型
        days: undefined, // 执行日期
        page: 1,
        rows: 10
      },
      // 聚簇分类搜索属性
      clusterCondition: {
        // searchtype: 'cluster',  // 搜索类型
        keyword: undefined,
        multiEntList: [],
        riskRank: [0, 10], // 风险等级
        investmentRank: [0, 10], // 投资等级
        creatityRank: [0, 10], // 创新能力等级
        brandRank: [0, 10], // 品牌等级
        recruitRank: [0, 10], // 招聘等级
        creditRank: [0, 10], // 信用等级
        page: 1,
        rows: 10
      },
      entTypePop: false, // 是否弹出自定义企业类型输入框
      entType: '', // 自定义企业类型
      registfundPop: false, // 是否弹出自定义注册资本输入框
      registfund_begin: '', // 自定义起始注册资本
      registfund_end: '', // 自定义结束注册资本
      establishPop: false, // 是否弹出自定义成立时间输入框
      establish_begin: '', // 自定义起始成立时间
      establish_end: '', // 自定义结束成立时间
      companyTotal: undefined, // 企业搜索结果数量
      riskTotal: undefined, // 风险搜索结果数量
      clusterTotal: undefined, // 聚簇分类搜索结果数量
      enterpriseList: [], // 搜索到的企业对象列表
      riskList: [], // 搜索到的风险结果对象
      clusterList: [], // 搜索到的聚簇结果对象
      // activeTap: 'first', // tab当前选中部分
      enterpriseTags: [], // "企业部分"选中条件标签
      riskTags: [], // "风险部分"选中条件标签
      clusterTags: [], // "聚簇分类部分"选中条件标签
      tagRankList: [1, 2, 3, 4, 5, 6, 7], //
      showDetail: false,
      myBackToTopStyle: myBackToTopStyle,
      tipword: '请输入关键字',
      iptTip: false,
      reSearch: false, // 重新搜索
      dialogFormVisible: false,
      compareEntList: [], // 对比企业结果列表
      timer: '' // 时间戳
    }
  },
  mounted() {
    this.initCondition()
    this.handleSearch()
    store.dispatch('Tcaptcha', false)
  },
  methods: {
    // 添加选中标签
    // item,'registeredCapitalNum','enterpriseTags'
    // item,'scope','enterpriseTags'
    handleAddTag(item, type, tagType) {
      const stringCond = new Set(['scope']) // new 一个set，初始只含一个'scope'
      if (stringCond.has(type)) {
        // 如果 type 是“查找范围”
        this.scope.add(item.val)
      } else {
        this.condition[type] = item.val // 其他查找属性
      }
      item.type = type
      // tagType[] 列表中是否包含当前选中标签
      if (
        _.find(this[tagType], { val: item.val, type: item.type }) === undefined
      ) {
        this[tagType].push(item)
      }
      this.handleSearch()
    },
    // 关闭选中标签
    // tag,'enterpriseTags',true
    // tag:{'val':'','type':''}
    handleClose(tag, tagType, search = false) {
      _.remove(this[tagType], tag) // 在tagType集合中删除tag e.g. enterpriseTags['a','b','c']在中删去'a'
      const stringCond = new Set(['scope'])
      if (stringCond.has(tag.type)) {
        // 如果 type 是“查找范围”
        this.scope.delete(tag.val)
        sessionStorage.removeItem('scope')
      } else {
        // 其他搜索属性
        this.condition[tag.type] = undefined
      }
      // if (tag.type === 'provinceCode') {
      //   this.handleClearAddress()
      // } else {
      //   if (search) {
      //     this.handleSearch()
      //   }
      // }
      if (search) this.handleSearch()
    },
    // 关闭所有选中标签
    handleRemoveTag(type, tagType) {
      if (type === '') {
        // 全部清除
        const tags = _.cloneDeep(this[tagType])
        for (const tag of tags) {
          this.handleClose(tag, tagType)
        }
        sessionStorage.removeItem(tagType)
        this.handleSearch() // 重新搜索
      } else {
        // this.condition[type].clear()
        // this[tagType] = _.filter(this[tagType], function(o) {
        //   return o.type !== type
        // })
      }
      // this.handleClearAddress()  // 清除所选地区
    },
    // 点击tab切换时，实时更新结果页面
    handleTabClick(tab, event) {
      sessionStorage.setItem('activeTap', this.activeTap)
      this.checkList = [] // 清空选择框
      this.handleSearch()
    },
    //  提交自定义企业类型
    handleSubmitType() {
      if (this.entType == null || this.entType === '') {
        this.$message.error('不能为空')
        return
      }
      const item = {}
      item.name = this.entType
      item.val = this.entType
      this.handleAddTag(item, 'type', 'enterpriseTags')
      this.entTypePop = false
    },
    // 提交自定义注册资本
    handleSubmitRegistFund() {
      this.registfund_begin = Number.parseInt(this.registfund_begin)
      this.registfund_end = Number.parseInt(this.registfund_end)
      if (
        Number.isNaN(this.registfund_begin) &&
        Number.isNaN(this.registfund_end)
      ) {
        this.registfundPop = false
        return
      } else {
        if (this.registfund_begin < 0 || this.registfund_end < 0) {
          this.$message.error('数值必须大于0')
          return
        }
        if (this.registfund_end <= this.registfund_begin) {
          this.$message.error('结束数值必须大于起始数值')
          return
        }
        const item = {} // item对象
        // left==null,right!=null
        if (
          Number.isNaN(this.registfund_end) &&
          !Number.isNaN(this.registfund_begin)
        ) {
          item.name = `${this.registfund_begin}万以上`
          item.val = `${this.registfund_begin}-0`
        }
        // left!=null,right==null
        if (
          !Number.isNaN(this.registfund_end) &&
          Number.isNaN(this.registfund_begin)
        ) {
          item.name = `${this.registfund_end}万以下`
          item.val = `0-${this.registfund_end}`
        }
        // left!=null,right!=null
        if (
          !Number.isNaN(this.registfund_end) &&
          !Number.isNaN(this.registfund_begin)
        ) {
          item.name = `${this.registfund_end}-${this.registfund_begin}万`
          item.val = `${this.registfund_end}-${this.registfund_begin}`
        }
        this.handleAddTag(item, 'registeredCapitalNum', 'enterpriseTags')
      }
      this.registfundPop = false
    },
    // 提交自定义注册时间
    handleSubmitEstablish() {
      this.establish_begin = Number.parseInt(this.establish_begin)
      this.establish_end = Number.parseInt(this.establish_end)
      if (
        Number.isNaN(this.establish_begin) &&
        Number.isNaN(this.establish_end)
      ) {
        this.establishPop = false
        return
      } else {
        const Year = new Date().getFullYear()
        if (this.establish_end < 0 || this.establish_begin < 0) {
          this.$message.error('数值必须大于0')
          return
        }
        if (this.establish_end < this.establish_begin) {
          this.$message.error('结束数值必须大于或等于起始数值')
          return
        }
        if (this.establish_end > Year || this.establish_begin > Year) {
          this.$message.error('成立时间不能大于当前年份')
          return
        }
        const item = {}
        if (
          Number.isNaN(this.establish_begin) &&
          !Number.isNaN(this.establish_end)
        ) {
          item.name = `${this.establish_end}年之前`
          item.val = `0-${this.establish_end}`
        }
        if (
          !Number.isNaN(this.establish_begin) &&
          Number.isNaN(this.establish_end)
        ) {
          item.name = `${this.establish_begin}年之后`
          item.val = `${this.establish_begin}-0`
        }
        if (
          !Number.isNaN(this.establish_begin) &&
          !Number.isNaN(this.establish_end)
        ) {
          if (this.establish_begin === this.establish_end) {
            item.name = this.establish_begin.toString()
            item.val = this.establish_begin.toString()
          } else {
            item.name = `${this.establish_begin}-${this.establish_end}年`
            item.val = `${this.establish_begin}-${this.establish_end}`
          }
        }
        this.handleAddTag(item, 'dateOfEstablishment', 'enterpriseTags')
        this.establishPop = false
      }
    },
    // 滑块值修改处理
    handleSliderChange(type, tagType) {
      this.clusterCondition[type] = this[tagType]
      console.log(this.clusterCondition[type])
      this.handleSearch()
    },
    // 多选框修改处理
    handleCheckBoxChange(type, tagType, checkBox) {
      if (this[checkBox] === true) {
        this.clusterCondition[type] = this[tagType]
      } else {
        this.clusterCondition[type] = [0, 0]
      }
      console.log(this.clusterCondition[type])
      this.handleSearch()
    },
    // 搜索
    handleSearch(page = 1) {
      if (this.reSearch) {
        sessionStorage.clear()
        sessionStorage.setItem('keyword', this.keyword)
        location.reload()
      } else {
        this.showDetail = false
        this.loading = true
        if (this.activeTap === 'first') {
          this.condition.page = page
          // scope: new Set([])
          this.condition.searchType = Array.from(this.scope) // 查找范围 e.g. ['1','2']为选中企业名和股东
          // this.condition.keyword = this.reSearch ? this.keyword : this.condition.keyword  // 废话，没意义
          search(this.condition).then(resp => {
            if (resp.data !== undefined) {
              console.log(resp)
              this.enterpriseList = resp.data
              this.companyTotal = Number.parseInt(resp.companyTotal)
              setTimeout(() => {
                this.loading = false
              }, 0.5 * 1000)
              window.scrollTo(1, 0)
            }
          })
        } else if (this.activeTap === 'second') {
          this.riskCondition.page = page
          this.riskCondition.keyword = this.condition.keyword
          if (
            this.riskCondition.keyword === undefined ||
            this.riskCondition.keyword.trim() === ''
          ) {
            // 提示
          }
          this.riskCondition.type = this.condition.riskType
          this.riskCondition.days = this.condition.dateScope
          searchRisk(this.riskCondition).then(resp => {
            console.log(resp)
            this.riskList = resp.data
            this.riskTotal = Number.parseInt(resp.riskTotal)
            setTimeout(() => {
              this.loading = false
            }, 0.5 * 1000)
            window.scrollTo(1, 0)
          })
        } else {
          this.clusterCondition.page = page
          this.clusterCondition.keyword = this.condition.keyword
          if (
            this.clusterCondition.keyword === undefined ||
            this.clusterCondition.keyword.trim() === ''
          ) {
            // 提示
          }
          searchCluster(this.clusterCondition).then(resp => {
            console.log(resp)
            this.clusterList = resp.data
            this.clusterTotal = Number.parseInt(resp.clusterTotal)
            setTimeout(() => {
              this.loading = false
            }, 0.5 * 1000)
            window.scrollTo(1, 0)
          })
        }
        this.storeCondition()
        this.reSearch = false
      }
      // 测试
      // this.companyTotal=100
      // this.enterpriseList=[{
      //     id :'abcdefgh',
      //     enterpriseName: 'abcdefgh',
      //     legalRepresentative:'',
      //     registeredCapitalNum:'2000',
      //     phoneNumber:'',
      //     dateOfEstablishment:'2019 2 16',
      //     email:'',
      //     address : '',
      //     highlightField:'enterpriseName',
      //     highlightValue:'abcdefgh'
      //   },{
      //     id:'eftghjdfa',
      //     enterpriseName:'eftghjdfa',
      //     legalRepresentative:'',
      //     registeredCapitalNum:'3000',
      //     phoneNumber:'',
      //     dateOfEstablishment:'2019 6 23',
      //     email:'',
      //     address : ''
      //   }
      // ]
      // this.riskTotal=10
      // this.riskList=[{id:'12345', enterpriseName:"12345",type:'1'}]
      // this.loading=false
    },
    showTip() {
      this.iptTip = true
      setTimeout(() => {
        this.iptTip = false
      }, 1.5 * 1000)
    },
    // 搜索关键字校验
    validKeyWord(key = this.keyword.trim()) {
      if (this.condition) {
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
      }
      return true
    },
    querySearch(queryString, cb) {
      if (this.keyword.trim() !== '') {
        if (this.validKeyWord(this.keyword)) {
          const data = {}
          data.keyword = this.keyword.trim()
          data.searchType = '0'
          data.page = 1
          data.rows = 5
          searchTip(data)
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
    handleSelect(item) {
      this.id = item.id
      this.keyword = item.enterpriseName
      this.showDetail = true
      this.$root.captcha.show()
    },
    handleShowCap() {
      this.keyword = this.keyword.trim()
      if (this.keyword !== '') {
        this.reSearch = true
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
    handleTcaptchaValid(resp) {
      if (resp.success) {
        sessionStorage.clear()
        sessionStorage.setItem('keyword', this.keyword)
        if (this.showDetail) {
          this.showDetailPage(this.id)
        } else {
          this.condition.page = 1
          this.riskCondition.page = 1
          this.handleSearch()
        }
      } else {
        this.reSearch = false
      }
    },
    // 跳转到企业详情页面
    showDetailPage(id, activeTap = 'basicInfo') {
      var location =
        window.location.origin + `/detail/${id}?activeTap=${activeTap}`
      window.open(location)
    },
    // 处理	currentPage 改变 val为当前页面
    handleCurrentChange(val) {
      console.log(val)
      this.handleSearch(val)
    },
    // 企业选中处理
    handleCheckedEntChange(val) {
      // console.log(val)
      console.log(this.checkList)
    },
    // 生成企业对比图
    handleCompare() {
      const data = {}
      data.ent = this.checkList
      searchCompareEntInfo(data).then(resp => {
        this.compareEntList = resp.data
        this.timer = new Date().getTime() // 重加载柱状图组件
        // console.log(this.compareEntList)
        this.dialogFormVisible = true
      }).catch(err => {
        console.log(err.message)
      })
      this.dialogFormVisible = true
    },
    // 将当前状态储存到 localStorage
    storeCondition() {
      sessionStorage.setItem('condition', JSON.stringify(this.condition))
      if (this.keyword !== '' && this.keyword !== undefined) {
        sessionStorage.setItem('keyword', this.keyword)
      }
      if (this.scope.size > 0) {
        sessionStorage.setItem('scope', JSON.stringify(Array.from(this.scope)))
      }
      if (this.enterpriseTags.length >= 0) {
        sessionStorage.setItem(
          'enterpriseTags',
          JSON.stringify(this.enterpriseTags)
        )
      }
      if (this.riskTags.length >= 0) {
        sessionStorage.setItem('riskTags', JSON.stringify(this.riskTags))
      }
      if (this.clusterTags.length >= 0) {
        sessionStorage.setItem('clusterTags', JSON.stringify(this.clusterTags))
      }
      if (this.multiEntList.length > 0) {
        sessionStorage.setItem(
          'multiEntList',
          JSON.stringify(this.multiEntList)
        )
      }
    },
    // 从 localStorage 初始化
    initCondition() {
      // localStorage 和 sessionStorage 属性允许在浏览器中存储 key/value 对的数据
      // sessionStorage 用于临时保存同一窗口(或标签页)的数据，在关闭窗口或标签页之后将会删除这些数据
      if (sessionStorage.getItem('condition')) {
        this.condition = JSON.parse(sessionStorage.getItem('condition')) // 如果浏览器储存了condition键值对，则以json格式加载到this.condition
      }
      if (
        sessionStorage.getItem('keyword') !== null &&
        sessionStorage.getItem('keyword') !== undefined
      ) {
        this.keyword = sessionStorage.getItem('keyword')
        this.condition.keyword = this.keyword
        this.riskCondition.keyword = this.keyword
        this.clusterCondition.keyword = this.keyword
      }
      if (sessionStorage.getItem('scope')) {
        this.scope = new Set(JSON.parse(sessionStorage.getItem('scope')))
      }
      if (sessionStorage.getItem('enterpriseTags') !== null) {
        this.enterpriseTags = JSON.parse(
          sessionStorage.getItem('enterpriseTags')
        )
      }
      if (sessionStorage.getItem('riskTags') !== null) {
        this.riskTags = JSON.parse(sessionStorage.getItem('riskTags'))
      }
      if (sessionStorage.getItem('clusterTags') !== null) {
        this.riskTags = JSON.parse(sessionStorage.getItem('clusterTags'))
      }
      if (sessionStorage.getItem('activeTap') !== null) {
        this.activeTap = sessionStorage.getItem('activeTap')
      }
      if (sessionStorage.getItem('multiEntList') != null) {
        this.multiEntList = sessionStorage.getItem('multiEntList')
        this.condition.multiEntList = this.multiEntList
        this.riskCondition.multiEntList = this.multiEntList
        this.clusterCondition.multiEntList = this.multiEntList
      }
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.high-light {
  color: red;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
/* 可以设置不同的进入和离开动画 */
/* 设置持续时间和动画函数 */
.slide-fade-enter-active {
  transition: all 0.5s ease;
}
.slide-fade-leave-active {
  transition: all 0.5s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter, .slide-fade-leave-to
    /* .slide-fade-leave-active for below version 2.1.8 */ {
  transform: translateX(10px);
  opacity: 0;
}
.el-form-item {
  margin-bottom: 0 !important;
}
.el-cascader {
  margin-left: 10px;
}
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
.el-main {
  min-width: 1200px;
  .content-row {
    cursor: pointer;
    max-width: 1200px;
    margin: 0 auto 40px !important;
    .box-card {
      border-radius: 0;
      border: 0;
    }
    .left-col {
      padding: 0 !important;
    }
    .tags-header {
      padding: 5px 5px 20px 20px;
      border-bottom: 1px solid #e9eeef;
      span {
        margin-right: 6px;
      }
      .el-tag {
        background: none;
        border-radius: 0;
        border: 1px solid #0000ff;
        color: #666;
        font-size: 14px;
        margin-bottom: 4px;
      }
      .clear-all {
        color: #3a71d8;
        font-weight: normal;
      }
    }
    .cond-row {
      padding: 12px 12px 0 12px;
      margin-left: 10px;
      span {
        color: #999;
        font-weight: normal;
        font-size: 14px;
        padding-right: 16px;
      }
      button {
        color: #333;
        font-weight: normal;
        padding: 4px 10px;
        border-radius: 0;
      }
      button:hover {
        color: #fff;
        background: #3a71d8;
      }
      .el-button + .el-button {
        margin-left: 0;
      }
    }
    .cond-row:last-child {
      margin-bottom: 15px;
    }
    .list-l-topbk {
      width: 80px;
      height: 25px;
      line-height: 25px;
      font-size: 12px;
      color: #3a71d8;
      text-decoration: none;
      border: 1px solid #e9eeef;
      border-top: 0;
      text-align: center;
      margin: 0 auto;
      background: #fff;
    }
    .list-card {
      margin-top: 20px;
      padding: 20px;
      .totla-text {
        font-size: 14px;
        color: #666;
        margin-bottom: 10px;
        margin-left: 30px;
        span {
          color: #3a71d8;
        }
      }
      .result-title {
        margin: -5px -20px -5px 10px;
      }
      .result-list {
        padding-bottom: 5px;
        border-bottom: 1px solid #e9eeef;
        .company-img {
          text-align: center;
          padding-top: 25px;
          img {
            width: 70%;
          }
        }
        .company-content {
          padding-top: 10px;
          color: #666;
          font-size: 14px;
          h2 {
            font-size: 20px;
            color: #000;
            font-weight: normal;
            margin-bottom: 4px;
            letter-spacing: 1px;
            line-height: 22px;
          }
          .el-row {
            padding: 6px 0;
          }
          .jg-col {
            /*border-left: 1px solid #666;*/
            padding-left: 15px;
          }
        }
        .company-status {
          vertical-align: middle;
          display: table-cell;
          text-align: center;
          height: 100%;
          line-height: 185px;
        }
      }
      .result-list:last-child {
        border-bottom: 0;
      }
      .result-list:hover {
        background: #f5f7fa;
      }
      .no-data {
        text-align: center;
        color: #999;
        line-height: 200px;
      }
      .page-row {
        text-align: center;
        margin: 20px;
      }
    }
    .right-col {
      padding-right: 0 !important;
      .el-row {
        height: 220px;
        margin-bottom: 20px;
        img {
          height: 100%;
          width: 100%;
        }
      }
    }
  }
}
</style>
