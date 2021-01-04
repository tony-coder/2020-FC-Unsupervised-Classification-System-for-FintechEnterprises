# -*- coding: utf-8 -*-
# @Time    : 2020/5/2 10:32
# @Email   : 693497091@qq.com
from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, \
    TableStyle, PageTemplate, Frame
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, LongTable, TableStyle, \
    tableofcontents, PageBreak

import json
import datetime
import hashlib
import re
pdfmetrics.registerFont(TTFont('pingbold', '方正粗黑宋简体.ttf'))
pdfmetrics.registerFont(TTFont('ping', 'simhei.ttf'))
pdfmetrics.registerFont(TTFont('hv', 'simhei.ttf'))
pdfmetrics.registerFont(TTFont('song', 'STSONG.TTF'))


def get_ent_json(file_path):
    ent_json = open(file_path, encoding='utf-8')
    ent = json.load(ent_json)
    return ent


def list_is_not_None(l):
    if l is not None and len(l) != 0:
        return True
    else:
        return False

def cut_text(text, lenth):
    textArr = re.findall('.{' + str(lenth) + '}', text)
    textArr.append(text[(len(textArr) * lenth):])
    return textArr

    # 生成PDF文件
class PDFGenerator:
    def __init__(self):
        # self.canvas = canvas.Canvas("1.pdf")
        self.filename = "ent_report.pdf"
        self.header_path = ""
        self.entname = ""
        self.title_style = ParagraphStyle(name="TitleStyle", fontName="pingbold", fontSize=40, leading=25,
                                            spaceAfter=20, textColor=colors.black,
                                            underlineWidth=1, alignment=TA_LEFT, )

        self.sub_title_style = ParagraphStyle(name="SubTitleStyle", fontName="hv", fontSize=32,
                                              textColor=colors.HexColor(0x666666), alignment=TA_LEFT, )
        self.content_style = ParagraphStyle(name="ContentStyle", fontName="ping", fontSize=18, leading=25,
                                            spaceAfter=20,
                                            underlineWidth=1, alignment=TA_LEFT, )

        self.foot_style = ParagraphStyle(name="FootStyle", fontName="ping", fontSize=20,
                                         textColor=colors.HexColor(0xB4B4B4),
                                         leading=25, spaceAfter=20, alignment=TA_CENTER, )
        self.table_title_style = ParagraphStyle(name="TableTitleStyle", fontName="pingbold", fontSize=20, leading=25,
                                                spaceAfter=10, alignment=TA_LEFT, )
        self.sub_table_style = ParagraphStyle(name="SubTableTitleStyle", fontName="ping", fontSize=16, leading=25,
                                              spaceAfter=10, alignment=TA_LEFT, )
        self.footer_style = ParagraphStyle(name="ContentStyle", fontName="ping", fontSize=10, leading=25, spaceAfter=20,
                                           underlineWidth=1, alignment=TA_LEFT, )

        self.table_font_size = 10

        self.level_0_title = ParagraphStyle(name="DirectoryStyle", fontName="pingbold", fontSize=48, leading=25,
                                            spaceAfter=20, textColor=colors.HexColor(0x0071C1),
                                            underlineWidth=1, alignment=TA_LEFT, )
        self.level_1_title = ParagraphStyle(name="DirectoryStyle", fontName="pingbold", fontSize=28, leading=25,
                                            spaceAfter=20, textColor=colors.HexColor(0x0071C1),
                                            underlineWidth=1, alignment=TA_LEFT, )
        self.level_2_title = ParagraphStyle(name="DirectoryStyle", fontName="ping", fontSize=24, leading=25,
                                            spaceAfter=20, textColor=colors.HexColor(0x0071C1),
                                            underlineWidth=1, alignment=TA_LEFT, )
        self.level_3_title = ParagraphStyle(name="DirectoryStyle", fontName="ping", fontSize=20, leading=25,
                                            spaceAfter=20, textColor=colors.HexColor(0x0071C1),
                                            underlineWidth=1, alignment=TA_LEFT, )
        self.content = ParagraphStyle(name="Content", fontName="ping", fontSize=16, leading=15,
                                      spaceAfter=15, borderPadding=10,
                                      underlineWidth=1, alignment=TA_LEFT, )

        self.missing = ParagraphStyle(name="Content", fontName="ping", fontSize=16, leading=15,
                                      spaceAfter=15, alignment=TA_LEFT,
                                      justifyBreaks=1,
                                      firstLineIndent=32)

    def footer(self, canvas, doc):
        """
        设置页脚
        :param canvas:Canvas类型  pdf画布
        :param doc:doc类型   整个pdf文件
        """
        canvas.saveState()  # 先保存当前的画布状态
        pageNumber = ("%s" % canvas.getPageNumber())  # 获取当前的页码
        p = Paragraph(pageNumber, self.footer_style)
        w, h = p.wrap(1 * cm, 1 * cm)  # 申请一块1cm大小的空间，返回值是实际使用的空间
        p.drawOn(canvas, 10.5 * cm, 1 * cm)  # 将页码放在指示坐标处
        canvas.restoreState()

    def header(self, canvas, doc):
        """
        设置页眉
        :param canvas:Canvas类型  pdf画布
        :param doc:doc类型     整个pdf文件
        """
        canvas.saveState()
        p = Paragraph("<img src='%s' width='%d' height='%d'/>" % (self.header_path, 22 * cm * 0.72, 1.71 * cm * 0.72),
                      self.content_style)  # 使用一个Paragraph Flowable存放图片
        w, h = p.wrap(doc.width, doc.bottomMargin)
        p.drawOn(canvas, doc.leftMargin, doc.topMargin + doc.height - 0.5 * cm)  # 放置图片
        w, h = p.wrap(doc.width, doc.bottomMargin)
        canvas.line(doc.leftMargin, doc.bottomMargin + doc.height + 0.5 * cm, doc.leftMargin + doc.width,
                    doc.bottomMargin + doc.height + 0.5 * cm)  # 画一条横线
        canvas.restoreState()

    def first_page_info(self, story, entname,logo_path):  # 首页内容
        img = Image(logo_path)
        self.entname = entname
        img.drawHeight = 20 * mm
        img.drawWidth = 50 * mm
        img.hAlign = TA_LEFT
        story.append(img)
        story.append(Spacer(1, 10 * mm))
        entname_list = cut_text(entname,20)
        for name in entname_list:
            story.append(Paragraph(name, self.title_style))
        story.append(Spacer(1, 2 * mm))
        story.append(Paragraph("评估报告", self.level_0_title))
        # story.append(Paragraph(, self.title_style))

        # story.append(Paragraph("Evaluate Report of " + entname, self.sub_title_style))
        story.append(Spacer(1, 30 * mm))
        report_code = hashlib.md5(
            (datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + entname).encode("utf-8")).hexdigest()
        story.append(Paragraph("报告编号：" + report_code, self.content_style))
        story.append(Paragraph("报告日期：" + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'), self.content_style))
        story.append(Spacer(1, 60 * mm))
        story.append(Paragraph("@e企查 版权所有", self.foot_style))
        story.append(PageBreak())

    def dir_pdf(self, story):
        dir_style = ParagraphStyle(name="DirectoryStyle", fontName="pingbold", fontSize=32, leading=25,
                                   spaceAfter=20, textColor=colors.HexColor(0x0071C1),
                                   underlineWidth=1, alignment=TA_CENTER, )
        sub_table_style = ParagraphStyle(name="SubTableTitleStyle", fontName="pingbold", fontSize=17, leading=25,
                                         spaceAfter=10, alignment=TA_LEFT, )
        story.append(Paragraph("目录", dir_style))
        story.append(Spacer(1, 10 * mm))
        story.append(Paragraph("一、企业背景（工商信息、变更记录）", sub_table_style))
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("二、风险模块（行政，司法处罚、司法记录、各类欠款记录）", sub_table_style))
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("三、投资模块（投资金额、各类投资记录）", sub_table_style))
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("四、知识产权模块（商标信息、专利信息、软件著作权、网站备案）", sub_table_style))
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("五、品牌模块（高新技术信息、商标级别、质检通过率）", sub_table_style))
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("六、招聘模块（智联招聘、中华英才、前程无忧招聘记录）", sub_table_style))
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("七、信用模块（是否守合同重信用企业、信用评级）", sub_table_style))
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("八、企业总评", sub_table_style))
        story.append(Spacer(1, 3 * mm))
        story.append(PageBreak())

    def missing_story(self, story, missing_name):

        info = "截止" + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + \
               ",根据平台数据库分析，未查询到与" + missing_name + "的相关信息。不排除因信息公开来源尚未公开" \
                                                   "、公开形式存在差异等情况导致的信息与客观事实不完全一致的情形,仅供客户参考。"
        story.append(Paragraph(info, self.missing))
        # story.append(Spacer(1, 0.2 * mm))

    def add_line(self, story):
        self.add_content(story, "----------------------", "----------------------")

    def add_empty(self, story):
        story.append(Spacer(1, 2 * mm))

    def add_content(self, story, param_name, param_value, zero_judge=False):
        if param_value is None:
            param_value = "无"
        if zero_judge and (str(param_value) == "0" or str(param_value) == "0.0"):
            param_value = "无"
        story.append(Paragraph(param_name + str(param_value), self.content))
        # story.append(Spacer(1, 0.2 * mm))

    def baseinfo_module_pdf(self, story, ent_baseinfo):
        story.append(Paragraph("一、企业背景", self.level_1_title))
        story.append(Spacer(1, 4 * mm))
        if ent_baseinfo is None:
            self.missing_story(story, "企业背景")
            return
        story.append(Paragraph("1.1 工商信息", self.level_2_title))
        self.add_content(story, "企业名称：", self.entname)
        # ent_baseinfo["company_baseinfo_summary"] = None
        if list_is_not_None(ent_baseinfo.get("company_baseinfo_summary")):
            company_baseinfo_summary = ent_baseinfo.get('company_baseinfo_summary')[0]
            for ent in ent_baseinfo.get('company_baseinfo_summary'):
                if ent.get('entstatus') is not None and ent.get('entstatus') == '在营（开业）企业':
                    company_baseinfo_summary = ent
                    break
            self.add_content(story, "注册资本：", company_baseinfo_summary.get('regcap'))
            self.add_content(story, "从业人数：", company_baseinfo_summary.get('empnum'))
            self.add_content(story, "成立日期：", company_baseinfo_summary.get('estdate'))
            self.add_content(story, "吊销时间：", company_baseinfo_summary.get('revdate'))
            self.add_content(story, "企业状态：", company_baseinfo_summary.get('entstatus'))
            self.add_content(story, "经营（驻在）期限至：", company_baseinfo_summary.get('opto'))
            self.add_content(story, "企业（机构）类型：", company_baseinfo_summary.get('enttype'))
            self.add_content(story, "企业类别：", company_baseinfo_summary.get('entcat'))
            self.add_content(story, "行业门类：", company_baseinfo_summary.get('industryphy'))
            self.add_content(story, "注册资本（金）币种：", company_baseinfo_summary.get('regcapcur'))
            self.add_content(story, "业务类型：", company_baseinfo_summary.get('industryco'))
            self.add_content(story, "经营（驻在）期限自：", company_baseinfo_summary.get('opfrom'))
        else:
            self.missing_story(story, "工商信息")
        self.add_empty(story)
        story.append(Paragraph("1.2 变更信息", self.level_2_title))
        if list_is_not_None(ent_baseinfo.get('change_info')):
            change_info_list = ent_baseinfo.get('change_info')
            # for i in range(len(change_info_list)):
            #     if change_info_list[i].get('altdate') is None:
            #         change_info_list[i]['altdate'] = " null"
            # change_info_list = sorted(change_info_list, key=lambda e: e['altdate'], reverse=True)
            index = 0
            data_flag_dict = {"0": "无", "1": "核准通过", "2": "删除或者驳回或者不予受理"}
            self.add_line(story)
            for change_item in change_info_list:
                index += 1
                data_flag = None
                if change_item.get('dataflag') is not None:
                    data_flag = data_flag_dict[str(change_item['dataflag'])]

                self.add_content(story, "事件编号：", index)
                self.add_content(story, "备注：", change_item.get('remark'))
                self.add_content(story, "数据来源标志：", data_flag)
                self.add_content(story, "变更次数：", change_item.get('alttime'))
                self.add_content(story, "变更事项：", change_item.get('altitem'))
                self.add_content(story, "变更日期：", change_item.get('altdate'))
                self.add_content(story, "业务编号：", change_item.get('openo'))
                self.add_line(story)
        else:
            self.missing_story(story, "变更事项")
        self.add_empty(story)
        story.append(Paragraph("1.3 企业背景小计", self.level_2_title))
        if list_is_not_None(ent_baseinfo.get("company_baseinfo_module")):
            company_baseinfo_module = ent_baseinfo.get("company_baseinfo_module")[0]
            self.add_content(story, "注册资本等级：", company_baseinfo_module.get("regcap_type"), zero_judge=True)
            self.add_content(story, "从业人员等级：", company_baseinfo_module.get("empnum_type"), zero_judge=True)
            self.add_content(story, "企业背景等级：", company_baseinfo_module.get("company_baseinfo_module"), zero_judge=True)
        else:
            self.missing_story(story, "企业背景小计")

    def risk_module_pdf(self, story, ent_risk):  # 风险模块信息
        self.add_empty(story)
        story.append(Paragraph("二、风险模块", self.level_1_title))
        self.add_empty(story)
        if ent_risk is None:
            self.missing_story(story, "风险模块")
            return
        story.append(Paragraph("2.1 处罚记录", self.level_2_title))
        if list_is_not_None(ent_risk.get("administrative_punishment")):
            administrative_punishment = ent_risk.get("administrative_punishment")[0]
            self.add_content(story, "公司行政处罚次数：", administrative_punishment.get("is_punish"))
        else:
            self.add_content(story, "公司行政处罚次数：", 0)
        if list_is_not_None(ent_risk.get("business_risk_abnormal")):
            business_risk_abnormal = ent_risk.get("business_risk_abnormal")[0]
            self.add_content(story, "经营异常次数：", business_risk_abnormal.get("is_bra"))
        else:
            self.add_content(story, "经营异常次数：", 0)
        if list_is_not_None(ent_risk.get("business_risk_all_punish")):
            business_risk_all_punish = ent_risk.get("business_risk_all_punish")[0]
            self.add_content(story, "行政处罚记录次数：", business_risk_all_punish.get("is_brap"))
        else:
            self.add_content(story, "行政处罚记录次数：", 0)

        if list_is_not_None(ent_risk.get("exception_list")):
            exception_list = ent_risk.get("exception_list")[0]
            self.add_content(story, "异常次数：", exception_list.get("is_except"))
        else:
            self.add_content(story, "异常次数：", 0)

        if list_is_not_None(ent_risk.get("business_risk_rightpledge")):
            business_risk_rightpledge = ent_risk.get("business_risk_rightpledge")[0]
            self.add_content(story, "股权出质次数：", business_risk_rightpledge.get("pledgenum"))
        else:
            self.add_content(story, "股权出质次数：", 0)

        if list_is_not_None(ent_risk.get("justice_credit")):
            justice_credit = ent_risk.get("justice_credit")[0]
            self.add_content(story, "列入失信黑名单次数：", justice_credit.get("is_justice_credit"))
        else:
            self.add_content(story, "列入失信黑名单次数：", 0)

        if list_is_not_None(ent_risk.get("justice_credit_aic")):
            justice_credit_aic = ent_risk.get("justice_credit_aic")[0]
            self.add_content(story, "列入工商部失信企业次数：", justice_credit_aic.get("is_justice_creditaic"))
        else:
            self.add_content(story, "列入工商部失信企业次数",0)
        self.add_empty(story)
        story.append(Paragraph("2.2 各类欠款", self.level_2_title))
        self.add_empty(story)
        story.append(Paragraph("2.2.1 社会保险欠缴情况", self.level_3_title))
        if list_is_not_None(ent_risk.get("ent_social_security")):
            ent_social_security = ent_risk.get("ent_social_security")
            self.add_line(story)
            # if list_is_not_None(ent_risk.get("ent_social_security")):
            #     ent_social_security = ent_risk.get("ent_social_security")
            # for i in range(len(ent_social_security)):
            #     if ent_social_security[i].get('updatetime') is None:
            #         ent_social_security[i]['updatetime'] = " null"
            # ent_social_security = sorted(ent_social_security, key=lambda e: e['updatetime'], reverse=True)
            index = 0

            for ent in ent_social_security:
                index += 1
                self.add_content(story, "事件编号：", index)
                self.add_content(story, "单位参加城镇职工基本养老保险累计欠缴金额：", ent.get("unpaidsocialins_so110"))
                self.add_content(story, "单位参加失业保险累计欠缴金额：", ent.get("unpaidsocialins_so210"))
                self.add_content(story, "单位参加职工基本医疗保险累计欠缴金额：", ent.get("unpaidsocialins_so310"))
                self.add_content(story, "单位参加工伤保险累计欠缴金额：", ent.get("unpaidsocialins_so410"))
                self.add_content(story, "单位参加生育保险累计欠缴金额：", ent.get("unpaidsocialins_so510"))
                self.add_content(story, "更新时间：", ent.get("updatetime"))
                self.add_line(story)

            if list_is_not_None(ent_risk.get("ent_social_security_p")):
                ent_social_security_p = ent_risk.get("ent_social_security_p")[0]
                self.add_content(story, "保险欠缴总额：", ent_social_security_p.get("unpaid_sum"))
            else:
                self.add_content(story, "保险欠缴总额：", 0)
        else:
            self.missing_story(story, "保险欠缴信息")

        if list_is_not_None(ent_risk.get("business_risk_taxunpaid")):
            business_risk_taxunpaid = ent_risk.get("business_risk_taxunpaid")[0]
            self.add_content(story, "企业累计欠税额：", business_risk_taxunpaid.get("taxunpaidnum"))
        else:
            self.add_content(story, "企业累计欠税额：", 0)
        self.add_empty(story)
        story.append(Paragraph("2.3 司法纠纷", self.level_2_title))
        self.add_empty(story)
        story.append(Paragraph("2.3.1 开庭公告数据", self.level_3_title))

        if list_is_not_None(ent_risk.get("justice_declare")):
            justice_declare = ent_risk.get("justice_declare")
            self.add_line(story)
            index = 0
            for ent in justice_declare:
                index += 1
                self.add_content(story, "事件编号：", index)
                self.add_content(story, "公示日期：", ent.get("declaredate"))
                self.add_content(story, "上诉方(是为1，否则为0)：", ent.get("appellant"))
                self.add_content(story, "被诉方(是为1，否则为0)：", ent.get("defendant"))
                self.add_content(story, "公告类型：", ent.get("declarestyle"))
                self.add_line(story)

                if list_is_not_None(ent_risk.get("judge_declare_p")):
                    judge_declare_p = ent_risk.get("judge_declare_p")[0]
                    self.add_content(story, "开庭公告数据小计：", "")
                    self.add_content(story, "最新纠纷日期：", judge_declare_p.get("declaredate"))
                    self.add_content(story, "上诉方次数：", judge_declare_p.get("appellant_amount"))
                    self.add_content(story, "被诉方次数：", judge_declare_p.get("defendant_amount_type"))
                else:
                    self.missing_story(story, "开庭公告数据小计")
        else:
            self.missing_story(story, "开庭公告数据")
        self.add_empty(story)
        story.append(Paragraph("2.3.2 执行金额", self.level_3_title))
        if list_is_not_None(ent_risk.get("justice_enforced")):
            justice_enforced = ent_risk.get("justice_enforced")

            self.add_line(story)
            index = 0
            for ent in justice_enforced:
                index += 1
                self.add_content(story, "事件编号：", index)
                self.add_content(story, "执行金额：", ent.get("enforce_amount"))
                self.add_content(story, "执行日期：", ent.get("record_date"))
                self.add_line(story)

            if list_is_not_None(ent_risk.get("justice_enforced_p")):
                justice_enforced_p = ent_risk.get("justice_enforced_p")[0]
                self.add_content(story, "执行金额小计：", "")
                self.add_content(story, "最新执行日期：", justice_enforced_p.get("record_date"))
                self.add_content(story, "总执行金额：", justice_enforced_p.get("enforce_amount"))
            else:
                self.missing_story(story, "执行金额小计")
        else:
            self.missing_story(story, "执行金额")
        self.add_empty(story)
        story.append(Paragraph("2.3.3 裁判文书数据", self.level_3_title))
        if list_is_not_None(ent_risk.get("justice_judge_new")):
            justice_judge_new = ent_risk.get("justice_judge_new")
            self.add_line(story)
            index = 0
            for ent in justice_judge_new:
                self.add_content(story, "时间：", ent.get("time"))
                self.add_content(story, "案件标题：", ent.get("title"))
                self.add_content(story, "判决结果：", ent.get("judgeresult"))
                self.add_content(story, "案由：", ent.get("casecause"))
                self.add_content(story, "案由编码类型：", ent.get("evidence"))
                self.add_content(story, "依据：", ent.get("courtrank"))
                self.add_content(story, "法院等级：", ent.get("datatype"))
                self.add_content(story, "司法类型：", ent.get("latypes"))
                self.add_line(story)

            if list_is_not_None(ent_risk.get("justice_judge_new_count")):
                justice_judge_new_count = ent_risk.get("justice_judge_new_count")[0]
                self.add_content(story, "裁判文书数据小计：", "")
                self.add_content(story, "案件纠纷次数：", justice_judge_new_count.get("judge_new_count"))
            else:
                self.missing_story(story, "裁判文书数据小计")

        else:
            self.missing_story(story, "裁判文书数据")

        self.add_empty(story)
        story.append(Paragraph("2.4 风险小计", self.level_2_title))
        if list_is_not_None(ent_risk.get("risk_module")):
            risk_module = ent_risk.get("risk_module")[0]
            story.append(Paragraph("2.4.1 风险属性等级", self.level_3_title))
            self.add_content(story, "行政处罚等级：", risk_module.get("is_punish_type"), zero_judge=True)
            self.add_content(story, "经营异常等级：", risk_module.get("is_bra_type"), zero_judge=True)
            self.add_content(story, "行政处罚次数等级：", risk_module.get("is_brap_type"), zero_judge=True)
            self.add_content(story, "股权出质等级：", risk_module.get("pledgenum_type"), zero_judge=True)
            self.add_content(story, "欠税等级：", risk_module.get("taxunpaidnum_type"), zero_judge=True)
            self.add_content(story, "欠缴保险等级：", risk_module.get("unpaid_sum_type"), zero_judge=True)
            self.add_content(story, "异常等级：", risk_module.get("is_except_type"), zero_judge=True)
            self.add_content(story, "最新纠纷日期等级：", risk_module.get("latest_date_type"), zero_judge=True)
            self.add_content(story, "原告总数等级：", risk_module.get("appellant_amount_type"), zero_judge=True)
            self.add_content(story, "被告总数等级：", risk_module.get("defendant_amount_type"), zero_judge=True)
            self.add_content(story, "工商部失信等级：", risk_module.get("is_justice_credit_type"), zero_judge=True)
            self.add_content(story, "司法风险失信等级：", risk_module.get("is_justice_creditaic_type"), zero_judge=True)
            self.add_content(story, "执行日期等级：", risk_module.get("record_date_type"), zero_judge=True)
            self.add_content(story, "执行金额等级：", risk_module.get("enforce_amount_type"), zero_judge=True)
            self.add_content(story, "诉讼次数等级：", risk_module.get("judge_new_count_type"), zero_judge=True)

            story.append(Paragraph("2.4.2 风险总分", self.level_3_title))
            self.add_content(story, "风险模块加权总分：", risk_module.get("risk_module"), zero_judge=True)
            self.add_content(story, "风险等级：", risk_module.get("risk_module_type"), zero_judge=True)

        else:
            self.missing_story(story, "风险小计")

    def investment_module_pdf(self, story, ent_investment):
        self.add_empty(story)
        story.append(Paragraph("三、投资模块", self.level_1_title))
        story.append(Spacer(1, 4 * mm))
        if ent_investment is None:
            self.missing_story(story, "投资模块")
            return
        self.add_empty(story)
        story.append(Paragraph("3.1 基本投资记录", self.level_2_title))

        if list_is_not_None(ent_investment.get("ent_bid")):
            ent_bid = ent_investment.get("ent_bid")[0]

            self.add_content(story, "中标次数：", ent_bid.get("bidnum"))
        else:
            self.add_content(story, "中标次数：", 0)

        if list_is_not_None(ent_investment.get("ent_branch")):
            ent_branch = ent_bid = ent_investment.get("ent_branch")[0]
            self.add_content(story, "分支个数：", ent_branch.get("branchnum"))
        else:
            self.add_content(story, "分支个数：", 0)

        if list_is_not_None(ent_investment.get("ent_investment")):
            tmp = ent_investment.get("ent_investment")[0]
            self.add_content(story, "投资次数：", tmp.get('investnum'))
        else:
            self.add_content(story, "投资次数：", 0)

        if list_is_not_None(ent_investment.get("ent_onlineshop")):
            tmp = ent_investment.get("ent_onlineshop")[0]
            self.add_content(story, "网店个数：", tmp.get("shopnum"))
        else:
            self.add_content(story, "网店个数：", 0)
        self.add_empty(story)
        story.append(Paragraph("3.2 年报信息", self.level_2_title))
        self.add_empty(story)
        story.append(Paragraph("3.2.1 企业出资信息（股东（自然人）信息）", self.level_3_title))
        if list_is_not_None(ent_investment.get("ent_contribution")):
            ent_contribution = ent_investment.get("ent_contribution")
            index = 0
            self.add_line(story)
            for ent in ent_contribution:
                index += 1
                self.add_content(story, "事件编号：", index)
                self.add_content(story, "投资人类型：", ent.get("invtype"))
                self.add_content(story, "出资方式：", ent.get("conform"))
                self.add_content(story, "认缴出资额（万元）：", ent.get("subconam"))
                self.add_content(story, "持股比例：", ent.get("conprop"))
                self.add_content(story, "出资日期（认缴）：", ent.get("condate"))
                self.add_line(story)

            if list_is_not_None(ent_investment.get("ent_contribution_total")):
                self.add_content(story, "股东出资信息小计：", "")
                ent_contribution_total = ent_investment.get("ent_contribution_total")[0]
                self.add_content(story, "认缴总额：", ent_contribution_total.get("subconam_total"))
            else:
                self.missing_story(story, "股东出资信息小计")

        else:
            self.missing_story(story, "企业出资信息（股东（自然人）信息）")
        self.add_empty(story)
        story.append(Paragraph("3.2.2 企业年报出资信息", self.level_3_title))
        if list_is_not_None(ent_investment.get("ent_contribution_year")):
            ent_contribution_year = ent_investment.get("ent_contribution_year")
            self.add_line(story)
            index = 0
            for ent in ent_contribution_year:
                index += 1
                self.add_content(story, "事件编号：", index)
                self.add_content(story, "认缴币种：", ent.get("subconcurrency"))
                self.add_content(story, "实缴出资时间：", ent.get("accondate"))
                self.add_content(story, "认缴出资方式：", ent.get("subconform"))
                self.add_content(story, "行业分类：", ent.get("anchetype"))
                self.add_content(story, "认缴出资时间：", ent.get("subcondate"))
                self.add_content(story, "实缴币种：", ent.get("acconcurrency"))
                self.add_content(story, "实缴出资方式：", ent.get("acconform"))
                self.add_content(story, "累计实缴额：", ent.get("liacconam"))
                self.add_content(story, "累计认缴额：", ent.get("lisubconam"))
                self.add_line(story)

            if list_is_not_None(ent_investment.get("ent_contribution_year_total")):
                self.add_content(story, "企业年报出资信息小计：", "")
                ent_contribution_year_total = ent_investment.get("ent_contribution_year_total")[0]
                self.add_content(story, "累计实缴总额：", ent_contribution_year_total.get("liacconam"))
                self.add_content(story, "累计认缴总额：", ent_contribution_year_total.get("lisubconam"))
            else:
                self.missing_story(story, "企业年报出资信息小计")
        else:
            self.missing_story(story, "企业年报出资信息")
        self.add_empty(story)
        story.append(Paragraph("3.2.3 年报担保信息", self.level_3_title))
        if list_is_not_None(ent_investment.get("ent_guarantee")):
            ent_guarantee = ent_investment.get("ent_guarantee")
            index = 0
            self.add_line(story)
            for ent in ent_guarantee:
                index += 1
                self.add_content(story, "事件编号：", index)
                self.add_content(story, "主债权种类：", ent.get("priclasseckind"))
                self.add_content(story, "履行债务的期限自：", ent.get("pefperform"))
                self.add_content(story, "是否公示此担保信息（1是2否）：", ent.get("iftopub"))
                self.add_content(story, "主债权数额：", ent.get("priclasecam"))
                self.add_content(story, "履行债务的期限至：", ent.get("pefperto"))
                self.add_content(story, "保证的期间（1期限2未约定）：", ent.get("guaranperiod"))
                self.add_content(story, "保证的方式（1一般保证2连带保证3未约定）：", ent.get("gatype"))
                self.add_content(story, "保证担保的范围：", ent.get("rage"))
                self.add_line(story)
        else:
            self.missing_story(story, "年报担保信息")
        self.add_empty(story)
        story.append(Paragraph("3.4 保险", self.level_2_title))
        if list_is_not_None(ent_investment.get("enterprise_insurance")):
            enterprise_insurance = ent_investment.get("enterprise_insurance")
            index = 0
            self.add_line(story)
            for ent in enterprise_insurance:
                index += 1
                self.add_content(story, "参保日期：", ent.get("cbrq"))
                self.add_content(story, "险种标志：", ent.get("xzbz"))
                self.add_content(story, "社会保险经办机构：", ent.get("sbjgbh"))
                self.add_content(story, "险种标志名称：", ent.get("xzbzmc"))
                self.add_content(story, "参保状态：", ent.get("cbzt"))
                self.add_content(story, "参保状态名称：", ent.get("cbztmc"))
                self.add_content(story, "单位编号：", ent.get("dwbh"))
                self.add_line(story)
        else:
            self.missing_story(story, "保险")

        self.add_empty(story)
        story.append(Paragraph("3.5 投资小计", self.level_2_title))
        if list_is_not_None(ent_investment.get("investment_module")):
            investment_module = ent_investment.get("investment_module")[0]
            story.append(Paragraph("3.5.1 投资属性等级", self.level_3_title))
            self.add_content(story, "年平均缴纳保险等级：", investment_module.get("insurance_num_type"), zero_judge=True)
            self.add_content(story, "中标次数等级：", investment_module.get("bidnum_type"), zero_judge=True)
            self.add_content(story, "分支个数等级：", investment_module.get("branchnum_type"), zero_judge=True)
            self.add_content(story, "企业认缴总额等级：", investment_module.get("subconam_total_type"), zero_judge=True)
            self.add_content(story, "累计实缴等级：", investment_module.get("liacconam_type"), zero_judge=True)
            self.add_content(story, "累计认缴等级：", investment_module.get("lisubconam_type"), zero_judge=True)
            self.add_content(story, "投资次数等级：", investment_module.get("investnum_type"), zero_judge=True)
            self.add_content(story, "网店个数等级：", investment_module.get("shopnum_type"), zero_judge=True)

            story.append(Paragraph("3.5.2 投资总分", self.level_3_title))
            self.add_content(story, "投资模块加权总分：", investment_module.get("investment_module"), zero_judge=True)
            self.add_content(story, "投资等级：", investment_module.get("investment_module_type"), zero_judge=True)


        else:
            self.missing_story(story, "投资小计")

    def creativity_module_pdf(self, story, ent_creativity):
        self.add_empty(story)
        story.append(Paragraph("四、知识产权模块", self.level_1_title))
        story.append(Spacer(1, 4 * mm))
        if ent_creativity is None:
            self.missing_story(story, "知识产权模块")
            return
        self.add_empty(story)
        story.append(Paragraph("4.1 知识产权信息", self.level_2_title))
        if list_is_not_None(ent_creativity.get("intangible_brand")):
            intangible_brand = ent_creativity.get("intangible_brand")[0]
            self.add_content(story, "商标申请次数：", ent_creativity.get("ibrand_num"))
        else:
            self.add_content(story, "商标申请次数：", 0)

        if list_is_not_None(ent_creativity.get("itangible_copyright")):
            itangible_copyright = ent_creativity.get("itangible_copyright")[0]
            self.add_content(story, "软件著作权登记次数：", itangible_copyright.get("icopy_num"))
        else:
            self.add_content(story, "软件著作权登记次数：", 0)

        if list_is_not_None(ent_creativity.get("itangible_patent")):
            itangible_patent = ent_creativity.get("itangible_patent")[0]
            self.add_content(story, "专利申请次数：", itangible_patent.get("ipat_num"))
        else:
            self.add_content(story, "专利申请次数：", 0)

        if list_is_not_None(ent_creativity.get("web_record_info")):
            web_record_info = ent_creativity.get("web_record_info")[0]
            self.add_content(story, "域名知识产权个数：", web_record_info.get("idom_num"))
        else:
            self.add_content(story, "域名知识产权个数：", 0)

        self.add_empty(story)
        story.append(Paragraph("4.2 知识产权小计", self.level_2_title))
        if list_is_not_None(ent_creativity.get("creativity_module")):
            creativity_module = ent_creativity.get("creativity_module")[0]
            story.append(Paragraph("4.2.1 知识产权属性等级", self.level_3_title))
            self.add_content(story, "商标申请次数等级：", creativity_module.get("ibrand_num_type"), zero_judge=True)
            self.add_content(story, "软件著作权登记次数等级：", creativity_module.get("icopy_num_type"), zero_judge=True)
            self.add_content(story, "专利申请次数等级：", creativity_module.get("ipat_num_type"), zero_judge=True)
            self.add_content(story, "域名知识产权个数等级：", creativity_module.get("idom_num_type"), zero_judge=True)

            story.append(Paragraph("4.2.2 知识产权总分", self.level_3_title))
            self.add_content(story, "知识产权模块加权总分：", creativity_module.get("creatity_module"), zero_judge=True)
            self.add_content(story, "知识产权等级：", creativity_module.get("creatity_module_type"), zero_judge=True)
        else:
            self.missing_story(story, "知识产权小计")

    def brand_module_pdf(self, story, ent_brand):
        self.add_empty(story)
        story.append(Paragraph("五、品牌模块", self.level_1_title))
        story.append(Spacer(1, 4 * mm))
        if ent_brand is None:
            self.missing_story(story, "品牌模块")
        self.add_empty(story)
        story.append(Paragraph("5.1 品牌信息", self.level_2_title))

        if list_is_not_None(ent_brand.get("jn_special_new_info")):
            jn_special_new_info = ent_brand.get("jn_special_new_info")[0]
            self.add_content(story, "是否济南市专精特新中小企业（0表示否，其余为是）：", jn_special_new_info.get("is_jnsn"))
        else:
            self.add_content(story, "是否济南市专精特新中小企业：", "否")

        if list_is_not_None(ent_brand.get("jn_tech_center")):
            jn_tech_center = ent_brand.get("jn_tech_center")[0]
            self.add_content(story, "科技等级（省级为2，市级为1，无则为0）：", jn_tech_center.get("level_rank"))
        else:
            self.add_content(story, "科技等级：", "无")

        if list_is_not_None(ent_brand.get("trademark_infoa")):
            trademark_infoa = ent_brand.get("trademark_infoa")[0]
            self.add_content(story, "是否列为驰名商标（0为否，其他为是）：", trademark_infoa.get("is_infoa"))
        else:
            self.add_content(story, "是否列为驰名商标：", "否")

        if list_is_not_None(ent_brand.get("trademark_infob")):
            trademark_infob = ent_brand.get("trademark_infob")[0]
            self.add_content(story, "是否列为著名商标（0为否，其他为是）：", trademark_infob.get('is_infob'))
        else:
            self.add_content(story, "是否列为著名商标：", "否")

        if list_is_not_None(ent_brand.get("product_checkinfo_connect")):
            product_checkinfo_connect = ent_brand.get("product_checkinfo_connect")[0]
            self.add_content(story, "质检通过率：", product_checkinfo_connect.get("passpercent"))
        else:
            self.add_content(story, "质检通过率：", "无")
        
        self.add_empty(story)
        story.append(Paragraph("5.2 品牌小计", self.level_2_title))
        if list_is_not_None(ent_brand.get("brand_module")):
            brand_module = ent_brand.get("brand_module")[0]
            story.append(Paragraph("5.2.1 品牌属性等级", self.level_3_title))

            self.add_content(story, "济南市专精特新中小企业等级：", brand_module.get("is_jnsn_type"), zero_judge=True)
            self.add_content(story, "科技等级标签：", brand_module.get("level_rank_type"), zero_judge=True)
            self.add_content(story, "驰名商标等级：", brand_module.get("is_infoa_type"), zero_judge=True)
            self.add_content(story, "著名商标等级：", brand_module.get("is_infob_type"), zero_judge=True)
            self.add_content(story, "质检通过率等级：", brand_module.get("passpercent_type"), zero_judge=True)

            story.append(Paragraph("5.2.2 品牌总分", self.level_3_title))
            self.add_content(story, "品牌模块加权总分：", brand_module.get("brand_module"), zero_judge=True)
            self.add_content(story, "品牌等级：", brand_module.get("brand_module_type"), zero_judge=True)

        else:
            self.missing_story(story, "品牌小计")

    def recruit_module_pdf(self, story, ent_recruit):
        self.add_empty(story)
        story.append(Paragraph("六、招聘模块", self.level_1_title))
        story.append(Spacer(1, 4 * mm))
        if ent_recruit is None:
            self.missing_story(story, "招聘模块")
        self.add_empty(story)
        story.append(Paragraph("6.1 招聘信息", self.level_2_title))

        if list_is_not_None(ent_recruit.get("recruit_module")):
            recruit_module = ent_recruit.get("recruit_module")[0]
            self.add_content(story, "前程无忧记录数：", recruit_module.get("qcwynum"))
            self.add_content(story, "中华英才记录数：", recruit_module.get("zhycnum"))
            self.add_content(story, "智联招聘记录数：", recruit_module.get("zlzpnum"))
            self.add_content(story, "招聘记录总数：", recruit_module.get("recruit_module"))
            self.add_content(story, "招聘记录总数等级：", recruit_module.get("recruit_module_type"),zero_judge=True)
        else:
            self.missing_story(story, "招聘信息")

    def credit_module_pdf(self, story, ent_credit):
        self.add_empty(story)
        story.append(Paragraph("七、信用模块", self.level_1_title))
        story.append(Spacer(1, 4 * mm))
        if ent_credit is None:
            self.missing_story(story, "信用模块")
        self.add_empty(story)
        story.append(Paragraph("7.1 信用信息", self.level_2_title))
        if list_is_not_None(ent_credit.get("enterprise_keep_contract")):
            enterprise_keep_contract = ent_credit.get("enterprise_keep_contract")[0]
            self.add_content(story, "守合同重信用企业次数：", enterprise_keep_contract.get("is_kcont"))
        else:
            self.add_content(story, "守合同重信用企业次数：", 0)

        if list_is_not_None(ent_credit.get("jn_credit_info")):
            jn_credit_info = ent_credit.get("jn_credit_info")[0]
            self.add_content(story, "企业信用评级：", jn_credit_info.get("credit_grade"))
        else:
            self.add_content(story, "企业信用评级：", "无")

        self.add_empty(story)
        story.append(Paragraph("7.2 信用小计", self.level_2_title))
        if list_is_not_None(ent_credit.get("credit_module")):
            credit_module = ent_credit.get("credit_module")[0]
            story.append(Paragraph("7.2.1 信用属性等级", self.level_3_title))

            self.add_content(story, "守合同重信用企业次数等级：", credit_module.get("is_kcont_type"), zero_judge=True)
            self.add_content(story, "科技等级标签：", credit_module.get("credit_grade_num_type"), zero_judge=True)


            story.append(Paragraph("7.2.2 信用总分", self.level_3_title))
            self.add_content(story, "信用模块加权总分：", credit_module.get("credit_module"), zero_judge=True)
            self.add_content(story, "信用等级：", credit_module.get("credit_module_type"), zero_judge=True)

        else:
            self.missing_story(story, "信用小计")

    def ent_module_pdf(self, story, ent_module):
        self.add_empty(story)
        story.append(Paragraph("八、企业总评", self.level_1_title))
        story.append(Spacer(1, 4 * mm))
        if ent_module is None:
            self.missing_story(story, "企业总评")
            return
        self.add_empty(story)
        story.append(Paragraph("8.1 总评信息", self.level_2_title))
        tmp = ent_module[0]
        self.add_content(story, "风险等级：", tmp.get("risk_module_type"), zero_judge=True)
        self.add_content(story, "投资等级：", tmp.get("investment_module_type"), zero_judge=True)
        self.add_content(story, "创新等级：", tmp.get("creativity_module_type"), zero_judge=True)
        self.add_content(story, "品牌等级：", tmp.get("brand_module_type"), zero_judge=True)
        self.add_content(story, "招聘等级：", tmp.get("recruit_module_type"), zero_judge=True)
        self.add_content(story, "信用等级：", tmp.get("credit_module_type"), zero_judge=True)
        self.add_content(story, "背景等级：", tmp.get("company_baseinfo_module_type"), zero_judge=True)

        story.append(Paragraph("8.2 总评等级", self.level_2_title))
        self.add_content(story, "企业加权总分：", tmp.get("ent"), zero_judge=True)
        self.add_content(story, "综合等级：", tmp.get("ent_type"), zero_judge=True)

    def genTaskPDF(self, filename,entname, ent,header_path,logo_path):
        '''
        
        :param filename:文件全路径 
        :param entname: 企业名称
        :param ent: 企业数据
        :param header_path: pdf页眉路径
        :param logo_path: pdf的logo路径
        :return: 
        '''
        self.entname = entname
        self.header_path = header_path
        story = []
        self.first_page_info(story, self.entname,logo_path)

        # 表格允许单元格内容自动换行格式设置
        self.dir_pdf(story)
        self.baseinfo_module_pdf(story, ent_baseinfo=ent.get('baseinfo'))
        self.risk_module_pdf(story, ent_risk=ent.get('risk'))
        self.investment_module_pdf(story, ent_investment=ent.get('investment'))
        self.creativity_module_pdf(story, ent_creativity=ent.get('creativity'))
        self.brand_module_pdf(story, ent_brand=ent.get("brand"))
        self.recruit_module_pdf(story, ent_recruit=ent.get("recruit"))
        self.credit_module_pdf(story, ent_credit=ent.get("credit"))
        self.ent_module_pdf(story, ent_module=ent.get("ent_module"))
        doc = BaseDocTemplate(filename,topMargin=3.5 * cm)  # 声明一个文档模版类，filename就是存放pdf的地址，
        frame_footer = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')  # 声明一块Frame，存放页码
        template = PageTemplate(id='test', frames=frame_footer, onPage=self.header,
                                onPageEnd=self.footer)  # 设置页面模板，在加载页面时先运行herder函数，在加载完页面后运行footer函数
        doc.addPageTemplates([template])
        doc.build(story)
        story.clear()


