from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.utils import json

from dataTojson.models import *
from entInfo.serializers import *
from dataTojson.models import CompanyBaseinfoSummary


class basicInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = BasicInfoSerializer

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())

        id = req['id']
        print(id)


        queryset = CompanyBaseinfoSummary.objects.filter(entname__exact=id)

        print(queryset)

        serializer = self.get_serializer(queryset,many=True)
        data = serializer.data
        data = data[0]
        res = {}
        res['code'] = 2000
        res.update(data)
        print(res)
        return JsonResponse(res)

class creditInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):


    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())

        id = req['id']
        print(id)

        enterprise_keep_contract = EnterpriseKeepContract.objects.filter(entname__exact=id).values("is_kcont")
        jn_credit_info = JnCreditInfo.objects.filter(entname__exact=id).values("credit_grade")

        res = {}
        res['code'] = 2000
        res['is_kcont'] = 0
        res['credit_grade'] = 0

        if len(enterprise_keep_contract):
            res['is_kcont'] = enterprise_keep_contract[0]['is_kcont']
        if len(jn_credit_info):
            res['credit_grade'] = jn_credit_info[0]['credit_grade']

        print(res)

        return JsonResponse(res)


class recruitInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = RecruitInfoSerializer

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())

        id = req['id']
        print(id)


        queryset = RecruitModule.objects.filter(entname__exact=id)

        print(queryset)

        serializer = self.get_serializer(queryset,many=True)
        data = serializer.data
        res = {}
        res['code'] = 2000
        if len(data) > 0:
            data = data[0]
            res.update(data)
        else:
            res['qcwynum'] = 0
            res['zhycnum'] = 0
            res['zlzpnum'] = 0
            res['recruit_sum'] = 0
            res['rank'] = 0      
        
        print(res)
        return JsonResponse(res)

class creativityInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())

        id = req['id']
        print(id)

        ibrand_num = IntangibleBrand.objects.filter(entname__exact=id).values("ibrand_num")
        icopy_num = IntangibleCopyright.objects.filter(entname__exact=id).values("icopy_num")
        ipat_num = IntangiblePatent.objects.filter(entname__exact=id).values("ipat_num")
        idom_num = WebRecordInfo.objects.filter(entname__exact=id).values("idom_num")

        print(ibrand_num)

        res = {}

        res['code'] = 2000
        res['ibrand_num'] = 0
        res['icopy_num'] = 0
        res['ipat_num'] = 0
        res['idom_num'] = 0

        if len(ibrand_num) :
            res['ibrand_num'] = ibrand_num[0]['ibrand_num']
        if len(icopy_num):
            res['icopy_num'] = icopy_num[0]['icopy_num']
        if len(ipat_num):
            res['ipat_num'] = ipat_num[0]['ipat_num']
        if len(idom_num):
            res['idom_num'] = idom_num[0]['idom_num']

        print(res)

        return JsonResponse(res)


class investmentInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())

        id = req['id']
        print(id)

        ent_investment = EntInvestment.objects.filter(entname__exact=id).values("investnum")
        ent_branch = EntBranch.objects.filter(entname__exact=id).values("branchnum")
        ent_onlineshop = EntOnlineshop.objects.filter(entname__exact=id).values("shopnum")
        ent_contribution_total  = EntContributionTotal.objects.filter(entname__exact=id).values("subconam_total")
        ent_contribution_year = EntContributionYear.objects.filter(entname__exact=id).values("liacconam","lisubconam")

        res = {}

        res['code'] = 2000
        res['investnum'] = 0
        res['branchnum'] = 0
        res['shopnum'] = 0
        res['totalSubscription'] = 0
        res['lisubconam'] = 0
        res['liacconam'] = 0

        if len(ent_investment) :
            res['investnum'] = ent_investment[0]['investnum']
        if len(ent_branch):
            res['branchnum'] = ent_branch[0]['branchnum']
        if len(ent_onlineshop):
            res['shopnum'] = ent_onlineshop[0]['shopnum']
        if len(ent_contribution_total):
            res['totalSubscription'] = ent_contribution_total[0]['subconam_total']
        if len(ent_contribution_year):
            res['lisubconam'] = ent_contribution_year[0]['lisubconam']
            res['liacconam'] = ent_contribution_year[0]['liacconam']

        print(res)

        return JsonResponse(res)


class punishmentInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())

        id = req['id']
        print(id)

        administrative_punishment = AdministrativePunishment.objects.filter(entname__exact=id).values("is_punish")
        business_risk_abnormal= BusinessRiskAbnormal.objects.filter(entname__exact=id).values("is_bra")
        business_risk_all_punish= BusinessRiskAllPunish.objects.filter(entname__exact=id).values("is_brap")

        exception_list= ExceptionList.objects.filter(entname__exact=id).values("is_except")
        justice_credit= JusticeCredit.objects.filter(entname__exact=id).values("is_justice_credit")
        justice_credit_aic= JusticeCreditAic.objects.filter(entname__exact=id).values("is_justice_creditaic")
        business_risk_rightpledge= BusinessRiskRightpledge.objects.filter(entname__exact=id).values("pledgenum")




        res = {}

        res['code'] = 2000
        res['is_punish'] = 0
        res['is_bra'] = 0
        res['is_brap'] = 0
        res['is_except'] = 0
        res['equity_pledge'] = 0
        res['is_justice_credit'] = 0
        res['is_justice_creditaic'] = 0

        if len(administrative_punishment) :
            res['is_punish'] = administrative_punishment[0]['is_punish']
        if len(business_risk_abnormal):
            res['is_bra'] = business_risk_abnormal[0]['is_bra']
        if len(business_risk_all_punish):
            res['is_brap'] = business_risk_all_punish[0]['is_brap']
        if len(exception_list):
            res['is_except'] = exception_list[0]['is_except']
        if len(justice_credit):
            res['is_justice_credit'] = justice_credit[0]['is_justice_credit']
        if len(justice_credit_aic):
            res['is_justice_creditaic'] = justice_credit_aic[0]['is_justice_creditaic']
        if len(business_risk_rightpledge):
            res['equity_pledge'] = business_risk_rightpledge[0]['pledgenum']

        print(res)

        return JsonResponse(res)


class justicDeclareInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = JusticeDeclareSerializer

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())

        id = req['id']
        page = req['page']
        row = req['row']

        print(id)

        queryset = JusticeDeclare.objects.filter(entname__exact=id)\

        pre_index = (page-1) * row
        lat_index = page * row
        if lat_index > len(queryset):
            lat_index = len(queryset)

        return_queryset = queryset[pre_index:lat_index]

        print(queryset)

        serializer = self.get_serializer(return_queryset, many=True)
        data = serializer.data
        res = {}
        res['code'] = 2000
        res['total'] = len(queryset)
        res['data'] = data
        print(res)

        return JsonResponse(res)

class entSocialSecurityInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = EntSocialSecuritySerializer

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())

        id = req['id']
        page = req['page']
        row = req['row']

        print(id)

        queryset = EntSocialSecurity.objects.filter(entname__exact=id)\

        pre_index = (page-1) * row
        lat_index = page * row
        if lat_index > len(queryset):
            lat_index = len(queryset)

        return_queryset = queryset[pre_index:lat_index]

        print(queryset)

        serializer = self.get_serializer(return_queryset, many=True)
        data = serializer.data
        res = {}
        res['code'] = 2000
        res['total'] = len(queryset)
        res['data'] = data
        print(res)

        return JsonResponse(res)



class tagInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = TagInfoSerializer

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())

        id = req['id']

        print(id)

        queryset = EntModule.objects.filter(entname__exact=id)
        print(queryset)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        res = {}
        res['code'] = 2000
        res['data'] = data[0]
        print(res)

        return JsonResponse(res)

class brandInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())
        id = req['id']
        print(id)

        jn_special_new_info = JnSpecialNewInfo.objects.filter(entname__exact=id).values("is_jnsn")
        jn_tech_center = JnTechCenter.objects.filter(entname__exact=id).values("level_rank")
        trademark_infoa = TrademarkInfoa.objects.filter(entname__exact=id).values("is_infoa")
        trademark_infob = TrademarkInfob.objects.filter(entname__exact=id).values("is_infob")
        product_checkinfo_connect = ProductCheckinfoConnect.objects.filter(entname__exact=id).values("passpercent")

        res = {}

        res['code'] = 2000
        res['is_jnsn'] = 0
        res['level_rank'] = 0
        res['is_infoa'] = 0
        res['is_infob'] = 0
        res['passpercent'] = 0

        if len(jn_special_new_info):
            res['is_jnsn'] = jn_special_new_info[0]['is_jnsn']
        if len(jn_tech_center):
            res['level_rank'] = jn_tech_center[0]['level_rank']
        if len(trademark_infoa):
            res['is_infoa'] = trademark_infoa[0]['is_infoa']
        if len(trademark_infob):
            res['is_infob'] = trademark_infob[0]['is_infob']
        if len(product_checkinfo_connect):
            res['passpercent'] = product_checkinfo_connect[0]['passpercent']

        print(res)

        return JsonResponse(res)


class recommendView(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = EntSearchSerializer

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())
        id = req['id']
        page = req['page']
        row = req['rows']
        print(id)

        Q_entname = Q(entname__exact=id)

        searchEnt_base = CompanyBaseinfoSummary.objects.get(Q_entname)
        searchEnt_module = EntModule.objects.get(Q_entname)

        industryPhy = searchEnt_base.industryphy
        inner_type = searchEnt_module.ent_inner_type
        ent_type = searchEnt_module.ent_type

        Q_entstatus = Q(entstatus__exact='注销企业')

        Q_industryPhy = Q(industryphy__exact=industryPhy)
        Q_inner_type = Q(entmodule_id__ent_inner_type__exact=inner_type)
        Q_ent_type = Q(entmodule_id__ent_type__exact=ent_type)

        recommendEnt1 = CompanyBaseinfoSummary.objects.exclude(Q_entname).exclude(Q_entstatus).filter(Q_industryPhy & Q_inner_type & Q_ent_type)
        print(len(recommendEnt1))

        resEnt = list(recommendEnt1)

        if len(resEnt) >= 20:
            resEnt = resEnt[0:20]
        else:
            rest = 20-len(resEnt)
            recommendEnt2 = CompanyBaseinfoSummary.objects.exclude(Q_entname).exclude(Q_entstatus).filter(Q_industryPhy & Q_inner_type & ~Q_ent_type)

            print(len(recommendEnt2))

            print(rest)

            if len(recommendEnt2) >= rest:
                recommendEnt2 = recommendEnt2[0:rest]
                print(len(recommendEnt2))
                resEnt = resEnt + recommendEnt2
                # print(resEnt)
            else:
                resEnt = resEnt + recommendEnt2
                recommendEnt3 = CompanyBaseinfoSummary.objects.exclude(Q_entname).exclude(Q_entstatus).filter(Q_industryPhy & ~Q_inner_type)

                rest = 20 - len(resEnt)

                if len(recommendEnt3) >= rest:
                    recommendEnt3 =recommendEnt3[:rest]
                    resEnt = resEnt + recommendEnt3
                else:
                    resEnt = resEnt + recommendEnt2
                    recommendEnt4 = CompanyBaseinfoSummary.objects.exclude(Q_entname).exclude(Q_entstatus).filter(~Q_industryPhy & Q_inner_type & Q_ent_type)

                    rest = 20 - len(resEnt)

                    if len(recommendEnt4) >= rest:
                        recommendEnt4 = recommendEnt3[:rest]

                    resEnt = resEnt + recommendEnt4

            print(len(resEnt))

        pre_index = (page-1)*row
        lat_index = page * row

        returnEnt = resEnt[pre_index:lat_index]
        res = {}
        res['code'] = 2000
        res['totalNumber'] = len(resEnt)
        serializer = self.get_serializer(returnEnt, many=True)
        data = serializer.data
        res['data'] = data
        return JsonResponse(res)


class compareEntView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CompareEntSerializer

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())
        data = req['ent']
        print(data)

        Q_entname = Q(entname__in = data)
        print(Q_entname)
        queryset = EntModule.objects.filter(Q_entname)
        print(queryset)

        res = {}
        res['code'] = 2000

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        data = serializer.data
        res['data'] = data

        print(res)

        return JsonResponse(res)




from dataTojson.models import *
from utils.ent_evaluate import PDFGenerator


class dataToJsonView(mixins.ListModelMixin, viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())
        keyword = req["id"]
        # print(req)
        Q_entname = Q(entname__contains=keyword)

        '''
        administrativePunishment
        business_risk_abnormal
        business_risk_all_punish
        business_risk_taxunpaid
        business_risk_rightpledge
        ent_social_security
        ent_social_security_p
        exception_list
        justice_declare
        judge_declare_p
        justice_enforced
        justice_enforced_p
        justice_judge_new
        justice_judge_new_count
        justice_credit
        justice_credit_aic
        risk_module


        '''

        # risk
        administrativePunishment = AdministrativePunishment.objects.filter(Q_entname)
        business_risk_abnormal = BusinessRiskAbnormal.objects.filter(Q_entname)
        business_risk_all_punish = BusinessRiskAllPunish.objects.filter(Q_entname)
        business_risk_taxunpaid = BusinessRiskTaxunpaid.objects.filter(Q_entname)
        business_risk_rightpledge = BusinessRiskRightpledge.objects.filter(Q_entname)
        ent_social_security = EntSocialSecurity.objects.filter(Q_entname)
        ent_social_security_p = EntSocialSecurityP.objects.filter(Q_entname)
        exception_list = ExceptionList.objects.filter(Q_entname)
        justice_declare = JusticeDeclare.objects.filter(Q_entname)
        judge_declare_p = JudgeDeclareP.objects.filter(Q_entname)
        justice_enforced = JusticeEnforced.objects.filter(Q_entname)
        justice_enforced_p = JusticeEnforcedP.objects.filter(Q_entname)
        justice_judge_new = JusticeJudgeNew.objects.filter(Q_entname)
        justice_judge_new_count = JusticeJudgeNewCount.objects.filter(Q_entname)
        justice_credit = JusticeCredit.objects.filter(Q_entname)
        justice_credit_aic = JusticeCreditAic.objects.filter(Q_entname)
        risk_module = RiskModule.objects.filter(Q_entname)

        # investment
        '''
        ent_bid =
        ent_branch
        ent_contribution
        ent_contribution_total
        ent_contribution_year
        ent_contribution_year_total
        ent_guarantee
        ent_investment
        ent_onlineshop
        enterprise_insurance
        enterprise_insurance_year_avg
        investment_module
        '''

        ent_bid = EntBid.objects.filter(Q_entname)
        ent_branch = EntBranch.objects.filter(Q_entname)
        ent_contribution = EntContribution.objects.filter(Q_entname)
        ent_contribution_total = EntContributionTotal.objects.filter(Q_entname)
        ent_contribution_year = EntContributionYear.objects.filter(Q_entname)
        ent_contribution_year_total = EntContributionYearTotal.objects.filter(Q_entname)
        ent_guarantee = EntGuarantee.objects.filter(Q_entname)
        ent_investment = EntInvestment.objects.filter(Q_entname)
        ent_onlineshop = EntOnlineshop.objects.filter(Q_entname)
        enterprise_insurance = EnterpriseInsurance.objects.filter(Q_entname)
        enterprise_insurance_year_avg = EnterpriseInsuranceYearAvg.objects.filter(Q_entname)
        investment_module = InvestmentModule.objects.filter(Q_entname)

        # creativity

        intangible_brand = IntangibleBrand.objects.filter(Q_entname)
        intangible_copyright = IntangibleCopyright.objects.filter(Q_entname)
        intangible_patent = IntangiblePatent.objects.filter(Q_entname)
        web_record_info = WebRecordInfo.objects.filter(Q_entname)
        creativity_module = CreativityModule.objects.filter(Q_entname)

        # brand
        jn_special_new_info = JnSpecialNewInfo.objects.filter(Q_entname)
        jn_tech_center = JnTechCenter.objects.filter(Q_entname)
        trademark_infoa = TrademarkInfoa.objects.filter(Q_entname)
        trademark_infob = TrademarkInfob.objects.filter(Q_entname)
        product_checkinfo_connect = ProductCheckinfoConnect.objects.filter(Q_entname)
        brand_module = BrandModule.objects.filter(Q_entname)

        # recruit
        recruit_module = RecruitModule.objects.filter(Q_entname)

        # credit
        enterprise_keep_contract = EnterpriseKeepContract.objects.filter(Q_entname)
        jn_credit_info = JnCreditInfo.objects.filter(Q_entname)
        credit_module = CreditModule.objects.filter(Q_entname)

        # baseinfo
        company_baseinfo_summary = CompanyBaseinfoSummary.objects.filter(Q_entname)
        company_baseinfo_module = CompanyBaseinfoModule.objects.filter(Q_entname)
        change_info = ChangeInfo.objects.filter(Q_entname)

        # ent_module
        ent_module = EntModule.objects.filter(Q_entname)

        # print(administrativePunishment.values("is_punish"))

        ent_pdf_dict = {}
        ent_pdf_dict[keyword] = {}

        res = {}

        risk = {}

        administrativepunishment = list(administrativePunishment.values("is_punish", "is_punish_type"))
        businessriskabnormal = list(business_risk_abnormal.values("is_bra", "is_bra_type"))
        businessriskallpunish = list(business_risk_all_punish.values("is_brap", "is_brap_type"))
        businessrisktaxunpaid = list(business_risk_taxunpaid.values("taxunpaidnum", "taxunpaidnum_type"))
        businessriskrightpledge = list(business_risk_rightpledge.values("pledgenum", "pledgenum_type"))
        entsocialsecurity = list(
            ent_social_security.values("unpaidsocialins_so110", "unpaidsocialins_so210", "unpaidsocialins_so310",
                                       "unpaidsocialins_so410", "unpaidsocialins_so510", "updatetime"))
        entsocialsecurityp = list(ent_social_security_p.values("unpaid_sum", "unpaid_sum_type"))
        exceptionlist = list(exception_list.values("is_except", "is_except_type"))
        justicedeclare = list(justice_declare.values("declaredate", "appellant", "defendant", "declarestyle"))
        judgedeclarep = list(
            judge_declare_p.values("declaredate", "appellant_amount", "defendant_amount", "declaredate_type",
                                   "appellant_amount_type", "defendant_amount_type"))
        justiceenforced = list(justice_enforced.values("record_date", "enforce_amount"))
        justiceenforcedp = list(
            justice_enforced_p.values("record_date", "enforce_amount", "record_date_type", "enforce_amount_type"))
        justicejudge_new = list(
            justice_judge_new.values("time", "title", "casetype", "judgeresult", "casecause", "evidence", "courtrank",
                                     "datatype", "latypes"))
        justicejudgenewcount = list(justice_judge_new_count.values("judge_new_count", "judge_new_count_type"))
        justicecredit = list(justice_credit.values("is_justice_credit", "is_justice_credit_type"))
        justicecreditaic = list(justice_credit_aic.values("is_justice_creditaic", "is_justice_creditaic_type"))
        riskmodule = list(
            risk_module.values("is_punish_type", "is_bra_type", "is_brap_type", "pledgenum_type", "taxunpaidnum_type",
                               "unpaid_sum_type", "is_except_type", "declaredate_type", "appellant_amount_type",
                               "defendant_amount_type", "is_justice_credit_type", "is_justice_creditaic_type",
                               "record_date_type", "enforce_amount_type", "judge_new_count_type",
                               "risk_module_inner_type", "risk_module", "risk_module_type"))

        risk['administrative_punishmen'] = administrativepunishment
        risk['business_risk_abnormal'] = businessriskabnormal
        risk['business_risk_all_punish'] = businessriskallpunish
        risk['business_risk_taxunpaid'] = businessrisktaxunpaid
        risk['business_risk_rightpledge'] = businessriskrightpledge
        risk['ent_social_security'] = entsocialsecurity
        risk['ent_social_security_p'] = entsocialsecurityp
        risk['exception_list'] = exceptionlist
        risk['justice_declare'] = justicedeclare
        risk['judge_declare_p'] = judgedeclarep
        risk['justice_enforced'] = justiceenforced
        risk['justice_enforced_p'] = justiceenforcedp
        risk['justice_judge_new'] = justicejudge_new
        risk['justice_judge_new_count'] = justicejudgenewcount
        risk['justice_credit'] = justicecredit
        risk['justice_credit_aic'] = justicecreditaic
        risk['risk_module'] = riskmodule

        res['risk'] = risk

        investment = {}

        entbid = list(ent_bid.values("bidnum", "bidnum_type"))
        entbranch = list(ent_branch.values("branchnum", "branchnum_type"))
        entcontribution = list(ent_contribution.values("invtype", "conform", "subconam", "conprop", "condate"))
        entcontributiontotal = list(ent_contribution_total.values("subconam_total", "subconam_total_type"))
        entcontributionyear = list(
            ent_contribution_year.values("subconcurrency", "accondate", "subconform", "anchetype", "subcondate",
                                         "acconcurrency", "acconform", "liacconam", "lisubconam"))
        entcontributionyeartotal = list(
            ent_contribution_year_total.values("liacconam", "lisubconam", "liacconam_type", "lisubconam_type"))
        entguarantee = list(
            ent_guarantee.values("priclaseckind", "pefperfrom", "iftopub", "priclasecam", "pefperto", "guaranperiod",
                                 "gatype", "rage"))
        entinvestment = list(ent_investment.values("investnum", "investnum_type"))
        entonlineshop = list(ent_onlineshop.values("shopnum", "shopnum_type"))
        enterpriseinsurance = list(
            enterprise_insurance.values("cbrq", "xzbz", "sbjgbh", "xzbzmc", "cbzt", "cbztmc", "dwbh"))
        enterpriseinsuranceyearavg = list(enterprise_insurance_year_avg.values("insurance_num", "insurance_num_type"))
        investmentmodule = list(
            investment_module.values("insurance_num_type", "bidnum_type", "branchnum_type", "subconam_total_type",
                                     "liacconam_total_type", "lisubconam_total_type", "investnum_type", "shopnum_type",
                                     "investment_module", "investment_module_type", "investment_module_inner_type"))

        investment["ent_bid"] = entbid
        investment["ent_branch"] = entbranch
        investment["ent_contribution"] = entcontribution
        investment["ent_contribution_total"] = entcontributiontotal
        investment["ent_contribution_year"] = entcontributionyear
        investment["ent_contribution_year_total"] = entcontributionyeartotal
        investment["ent_guarantee"] = entguarantee
        investment["ent_investment"] = entinvestment
        investment["ent_onlineshop"] = entonlineshop
        investment["enterprise_insurance"] = enterpriseinsurance
        investment["enterprise_insurance_year_avg"] = enterpriseinsuranceyearavg
        investment["investment_module"] = investmentmodule

        res['investment'] = investment

        creativity = {}

        intangiblebrand = list(intangible_brand.values("ibrand_num", "ibrand_num_type"))
        intangiblecopyright = list(intangible_copyright.values("icopy_num", "icopy_num_type"))
        intangiblepatent = list(intangible_patent.values("ipat_num", "ipat_num_type"))
        webrecordinfo = list(web_record_info.values("idom_num", "idom_num_type"))
        creativitymodule = list(
            creativity_module.values("ibrand_num_type", "icopy_num_type", "ipat_num_type", "idom_num_type",
                                     "creativity_module", "creativity_module_type", "creativity_module_inner_type"))

        creativity['intangible_brand'] = intangiblebrand
        creativity['intangible_copyright'] = intangiblecopyright
        creativity['intangible_patent'] = intangiblepatent
        creativity['web_record_info'] = webrecordinfo
        creativity['creativity_module'] = creativitymodule

        res['creativity'] = creativity

        brand = {}

        jnspecialnewinfo = list(jn_special_new_info.values("is_jnsn", "is_jnsn_type"))
        jntechcenter = list(jn_tech_center.values("level_rank", "level_rank_type"))
        trademarkinfoa = list(trademark_infoa.values("is_infoa", "is_infoa_type"))
        trademarkinfob = list(trademark_infob.values("is_infob", "is_infob_type"))
        productcheckinfo_connect = list(product_checkinfo_connect.values("passpercent", "passpercent_type"))
        brandmodule = list(
            brand_module.values("is_jnsn_type", "level_rank_type", "passpercent_type", "is_infoa_type", "is_infob_type",
                                "brand_module", "brand_module_type", "brand_module_inner_type"))

        brand["jn_special_new_info"] = jnspecialnewinfo
        brand["jn_tech_center"] = jntechcenter
        brand["trademark_infoa"] = trademarkinfoa
        brand["trademark_infob"] = trademarkinfob
        brand["product_checkinfo_connect"] = productcheckinfo_connect
        brand["brand_module"] = brandmodule

        res['brand'] = brand

        recruit = {}
        recruitmodule = list(
            recruit_module.values("qcwynum", "zhycnum", "zlzpnum", "recruit_module", "recruit_module_type"))
        recruit['recruit_module'] = recruitmodule

        res['recruit'] = recruit

        credit = {}
        enterprisekeepcontract = list(enterprise_keep_contract.values("is_kcont", "is_kcont_type"))
        jncreditinfo = list(jn_credit_info.values("credit_grade", "credit_grade_num", "credit_grade_num_type"))
        creditmodule = list(
            credit_module.values("is_kcont_type", "credit_grade_num_type", "credit_module", "credit_module_type"))
        credit['enterprise_keep_contract'] = enterprisekeepcontract
        credit['jn_credit_info'] = jncreditinfo
        credit['credit_module'] = creditmodule
        res['credit'] = credit

        baseinfo = {}
        companybaseinfosummary = list(
            company_baseinfo_summary.values("regcap", "empnum", "estdate", "candate", "revdate", "entstatus", "opto",
                                            "enttype", "entcat", "industryphy", "regcapcur", "industryco", "opfrom",
                                            "regcap_type"))
        companybaseinfomodule = list(
            company_baseinfo_module.values("regcap_type", "empnum_type", "estdate_type", "company_baseinfo_module",
                                           "company_baseinfo_module_type"))
        changeinfo = list(
            change_info.values("remark", "dataflag", "alttime", "altitem", "cxstatus", "altdate", "openo"))
        baseinfo['company_baseinfo_summary'] = companybaseinfosummary
        baseinfo['company_baseinfo_module'] = companybaseinfomodule
        baseinfo['change_info'] = changeinfo

        res['baseinfo'] = baseinfo

        ent_module1 = {}
        entmodule = list(ent_module.values("risk_module_type", "investment_module_type", "creativity_module_type",
                                           "brand_module_type", "recruit_module_type", "credit_module_type",
                                           "company_baseinfo_module_type", "ent", "ent_type", "ent_inner_type"))
        # ent_module1['ent_module'] = entmodule

        res['ent_module'] = entmodule

        ent_pdf_dict[keyword] = res

        # print(risk)

        # print(ent_pdf_dict)
        ent_name = list(ent_pdf_dict.keys())[0]
        ent_data = ent_pdf_dict[ent_name]

        pdf = PDFGenerator()  # pdf生成对象

        dirname = 'static/pdf/'
        url = dirname + keyword + '.pdf'

        print(url)

        pdf.genTaskPDF(filename=url, entname=ent_name, ent=ent_data,
                       header_path=r'static/header.jpg', logo_path='static/pdflogo.jpg')

        print(url)

        host = 'http://121.36.13.179/'

        url = host + url
        res = {}
        res['code'] = 2000

        data = {}
        data['reportURL'] = url
        res['data'] = data

        return JsonResponse(res)





