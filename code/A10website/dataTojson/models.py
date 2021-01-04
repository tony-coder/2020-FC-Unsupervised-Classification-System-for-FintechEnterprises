# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.core.cache import cache
from django.db import models



class AdministrativePunishment(models.Model):
    entname = models.CharField(max_length=255)
    is_punish = models.IntegerField(blank=True, null=True)
    is_punish_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'administrative_punishment'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BaseInfoModule(models.Model):
    entname = models.CharField(max_length=255)
    regcap_type = models.IntegerField(blank=True, null=True)
    empnum_type = models.IntegerField(blank=True, null=True)
    estdate_type = models.IntegerField(blank=True, null=True)
    base_info_module_mark = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_info_module'


class Baseinfotest(models.Model):
    entname = models.CharField(max_length=255)
    empnum = models.IntegerField(blank=True, null=True)
    regcap = models.FloatField(blank=True, null=True)
    ma = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baseinfotest'


class BrandModule(models.Model):
    entname = models.CharField(max_length=255)
    is_jnsn_type = models.IntegerField(blank=True, null=True)
    level_rank_type = models.IntegerField(blank=True, null=True)
    passpercent_type = models.IntegerField(blank=True, null=True)
    is_infoa_type = models.IntegerField(blank=True, null=True)
    is_infob_type = models.IntegerField(blank=True, null=True)
    brand_module = models.FloatField(blank=True, null=True)
    brand_module_type = models.IntegerField(blank=True, null=True)
    brand_module_inner_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brand_module'


class BusinessRiskAbnormal(models.Model):
    entname = models.CharField(max_length=255)
    is_bra = models.IntegerField(blank=True, null=True)
    is_bra_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business_risk_abnormal'


class BusinessRiskAllPunish(models.Model):
    entname = models.CharField(max_length=255)
    is_brap = models.IntegerField(blank=True, null=True)
    is_brap_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business_risk_all_punish'


class BusinessRiskRightpledge(models.Model):
    entname = models.CharField(max_length=255)
    pledgenum = models.IntegerField(blank=True, null=True)
    pledgenum_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business_risk_rightpledge'


class BusinessRiskTaxunpaid(models.Model):
    entname = models.CharField(max_length=255)
    taxunpaidnum = models.FloatField(blank=True, null=True)
    taxunpaidnum_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business_risk_taxunpaid'


class BusinessRiskTaxunpaidSocialSecurity(models.Model):
    entname = models.CharField(max_length=255)
    tax_social_security_unpaidnum = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business_risk_taxunpaid_social_security'


class ChangeInfo(models.Model):
    entname = models.CharField(max_length=255)
    remark = models.CharField(max_length=255, blank=True, null=True)
    dataflag = models.CharField(max_length=255, blank=True, null=True)
    alttime = models.IntegerField(blank=True, null=True)
    altitem = models.CharField(max_length=255, blank=True, null=True)
    cxstatus = models.CharField(max_length=255, blank=True, null=True)
    altdate = models.CharField(max_length=255, blank=True, null=True)
    openo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'change_info'


class CompanyBaseinfo(models.Model):
    entname = models.CharField(max_length=255)
    regcap = models.FloatField(blank=True, null=True)
    empnum = models.IntegerField(blank=True, null=True)
    estdate = models.CharField(max_length=255, blank=True, null=True)
    candate = models.CharField(max_length=255, blank=True, null=True)
    revdate = models.CharField(max_length=255, blank=True, null=True)
    entstatus = models.CharField(max_length=255, blank=True, null=True)
    opto = models.CharField(max_length=255, blank=True, null=True)
    enttype = models.CharField(max_length=255, blank=True, null=True)
    entcat = models.CharField(max_length=255, blank=True, null=True)
    industryphy = models.CharField(max_length=255, blank=True, null=True)
    regcapcur = models.CharField(max_length=255, blank=True, null=True)
    industryco = models.CharField(max_length=255, blank=True, null=True)
    opfrom = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_baseinfo'


class CompanyBaseinfoModule(models.Model):
    entname = models.CharField(max_length=255)
    regcap = models.FloatField(blank=True, null=True)
    empnum = models.IntegerField(blank=True, null=True)
    estdate = models.CharField(max_length=255, blank=True, null=True)
    regcap_type = models.IntegerField(blank=True, null=True)
    empnum_type = models.IntegerField(blank=True, null=True)
    estdate_type = models.IntegerField(blank=True, null=True)
    company_baseinfo_module = models.FloatField(blank=True, null=True)
    company_baseinfo_module_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_baseinfo_module'


class CompanyBaseinfoP1(models.Model):
    entname = models.CharField(max_length=255)
    regcap = models.FloatField(blank=True, null=True)
    empnum = models.IntegerField(blank=True, null=True)
    estdate = models.CharField(max_length=255, blank=True, null=True)
    regcap_type = models.IntegerField(blank=True, null=True)
    empnum_type = models.IntegerField(blank=True, null=True)
    estdate_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_baseinfo_p1'

class EntModule(models.Model):
    entname = models.CharField(max_length=255)
    risk_module_type = models.IntegerField(blank=True, null=True)
    investment_module_type = models.IntegerField(blank=True, null=True)
    creativity_module_type = models.IntegerField(blank=True, null=True)
    brand_module_type = models.IntegerField(blank=True, null=True)
    recruit_module_type = models.IntegerField(blank=True, null=True)
    credit_module_type = models.IntegerField(blank=True, null=True)
    company_baseinfo_module_type = models.IntegerField(blank=True, null=True)
    ent = models.FloatField(blank=True, null=True)
    ent_type = models.IntegerField(blank=True, null=True)
    ent_inner_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_module'

class CompanyBaseinfoSummary(models.Model):
    entname = models.CharField(max_length=255)
    regcap = models.FloatField(blank=True, null=True)
    empnum = models.IntegerField(blank=True, null=True)
    estdate = models.CharField(max_length=255, blank=True, null=True)
    candate = models.CharField(max_length=255, blank=True, null=True)
    revdate = models.CharField(max_length=255, blank=True, null=True)
    entstatus = models.CharField(max_length=255, blank=True, null=True)
    opto = models.CharField(max_length=255, blank=True, null=True)
    enttype = models.CharField(max_length=255, blank=True, null=True)
    entcat = models.CharField(max_length=255, blank=True, null=True)
    industryphy = models.CharField(max_length=255, blank=True, null=True)
    regcapcur = models.CharField(max_length=255, blank=True, null=True)
    industryco = models.CharField(max_length=255, blank=True, null=True)
    opfrom = models.CharField(max_length=255, blank=True, null=True)
    regcap_type = models.IntegerField(blank=True, null=True)
    company_baseinfo_module = models.FloatField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    searchnum = models.IntegerField(db_column='searchNum', blank=True, null=True,default=0)  # Field name made lowercase.
    imag = models.CharField(max_length=255, blank=True, null=True)
    entmodule = models.ForeignKey('EntModule', models.DO_NOTHING, related_name='EntModule',  blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_baseinfo_summary'


class CreativityModule(models.Model):
    entname = models.CharField(max_length=255)
    ibrand_num_type = models.IntegerField(blank=True, null=True)
    icopy_num_type = models.IntegerField(blank=True, null=True)
    ipat_num_type = models.IntegerField(blank=True, null=True)
    idom_num_type = models.IntegerField(blank=True, null=True)
    creativity_module = models.IntegerField(blank=True, null=True)
    creativity_module_type = models.IntegerField(blank=True, null=True)
    creativity_module_inner_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'creativity_module'


class CreditModule(models.Model):
    entname = models.CharField(max_length=255)
    is_kcont_type = models.IntegerField(blank=True, null=True)
    credit_grade_num_type = models.IntegerField(blank=True, null=True)
    credit_module = models.FloatField(blank=True, null=True)
    credit_module_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'credit_module'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EntBid(models.Model):
    entname = models.CharField(max_length=255)
    bidnum = models.IntegerField(blank=True, null=True)
    bidnum_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_bid'


class EntBranch(models.Model):
    entname = models.CharField(max_length=255)
    branchnum = models.IntegerField(blank=True, null=True)
    branchnum_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_branch'


class EntContribution(models.Model):
    entname = models.CharField(max_length=255)
    invtype = models.CharField(max_length=255, blank=True, null=True)
    conform = models.CharField(max_length=255, blank=True, null=True)
    subconam = models.FloatField(blank=True, null=True)
    conprop = models.IntegerField(blank=True, null=True)
    condate = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_contribution'


class EntContributionTotal(models.Model):
    entname = models.CharField(max_length=255)
    subconam_total = models.FloatField(blank=True, null=True)
    subconam_total_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_contribution_total'


class EntContributionYear(models.Model):
    entname = models.CharField(max_length=255)
    subconcurrency = models.CharField(max_length=255, blank=True, null=True)
    accondate = models.CharField(max_length=255, blank=True, null=True)
    subconform = models.CharField(max_length=255, blank=True, null=True)
    anchetype = models.CharField(max_length=255, blank=True, null=True)
    subcondate = models.CharField(max_length=255, blank=True, null=True)
    acconcurrency = models.CharField(max_length=255, blank=True, null=True)
    acconform = models.CharField(max_length=255, blank=True, null=True)
    liacconam = models.CharField(max_length=45, blank=True, null=True)
    lisubconam = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_contribution_year'


class EntContributionYearTotal(models.Model):
    entname = models.CharField(max_length=255)
    liacconam = models.FloatField(blank=True, null=True)
    lisubconam = models.FloatField(blank=True, null=True)
    liacconam_type = models.IntegerField(blank=True, null=True)
    lisubconam_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_contribution_year_total'


class EntGuarantee(models.Model):
    entname = models.CharField(max_length=45)
    priclaseckind = models.CharField(max_length=255, blank=True, null=True)
    pefperfrom = models.CharField(max_length=255, blank=True, null=True)
    iftopub = models.CharField(max_length=255, blank=True, null=True)
    priclasecam = models.FloatField(blank=True, null=True)
    pefperto = models.CharField(max_length=255, blank=True, null=True)
    guaranperiod = models.CharField(max_length=255, blank=True, null=True)
    gatype = models.CharField(max_length=255, blank=True, null=True)
    rage = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_guarantee'


class EntInvestment(models.Model):
    entname = models.CharField(max_length=255)
    investnum = models.IntegerField(blank=True, null=True)
    investnum_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_investment'





class EntOnlineshop(models.Model):
    entname = models.CharField(max_length=255)
    shopnum = models.IntegerField(blank=True, null=True)
    shopnum_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_onlineshop'


class EntSocialSecurity(models.Model):
    entname = models.CharField(max_length=255)
    unpaidsocialins_so110 = models.FloatField(blank=True, null=True)
    unpaidsocialins_so210 = models.FloatField(blank=True, null=True)
    unpaidsocialins_so310 = models.FloatField(blank=True, null=True)
    unpaidsocialins_so410 = models.FloatField(blank=True, null=True)
    unpaidsocialins_so510 = models.FloatField(blank=True, null=True)
    updatetime = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_social_security'


class EntSocialSecurityP(models.Model):
    entname = models.CharField(max_length=255)
    unpaid_sum = models.IntegerField(blank=True, null=True)
    unpaid_sum_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ent_social_security_p'


class EnterpriseInsurance(models.Model):
    entname = models.CharField(max_length=255)
    cbrq = models.CharField(max_length=255, blank=True, null=True)
    xzbz = models.CharField(max_length=255, blank=True, null=True)
    sbjgbh = models.CharField(max_length=255, blank=True, null=True)
    xzbzmc = models.CharField(max_length=255, blank=True, null=True)
    cbzt = models.CharField(max_length=255, blank=True, null=True)
    cbztmc = models.CharField(max_length=255, blank=True, null=True)
    dwbh = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_insurance'


class EnterpriseInsuranceYearAvg(models.Model):
    entname = models.CharField(max_length=45)
    insurance_num = models.FloatField(blank=True, null=True)
    insurance_num_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_insurance_year_avg'


class EnterpriseKeepContract(models.Model):
    entname = models.CharField(max_length=255)
    is_kcont = models.IntegerField(blank=True, null=True)
    is_kcont_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_keep_contract'


class ExceptionList(models.Model):
    entname = models.CharField(max_length=255)
    is_except = models.IntegerField(blank=True, null=True)
    is_except_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exception_list'


class IntangibleBrand(models.Model):
    entname = models.CharField(max_length=45)
    ibrand_num = models.IntegerField(blank=True, null=True)
    ibrand_num_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'intangible_brand'


class IntangibleCopyright(models.Model):
    entname = models.CharField(max_length=255)
    icopy_num = models.IntegerField(blank=True, null=True)
    icopy_num_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'intangible_copyright'


class IntangiblePatent(models.Model):
    entname = models.CharField(max_length=255)
    ipat_num = models.IntegerField(blank=True, null=True)
    ipat_num_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'intangible_patent'


class InvestmentModule(models.Model):
    entname = models.CharField(max_length=255)
    insurance_num_type = models.IntegerField(blank=True, null=True)
    bidnum_type = models.IntegerField(blank=True, null=True)
    branchnum_type = models.IntegerField(blank=True, null=True)
    subconam_total_type = models.IntegerField(blank=True, null=True)
    liacconam_total_type = models.IntegerField(blank=True, null=True)
    lisubconam_total_type = models.IntegerField(blank=True, null=True)
    investnum_type = models.IntegerField(blank=True, null=True)
    shopnum_type = models.IntegerField(blank=True, null=True)
    investment_module = models.FloatField(blank=True, null=True)
    investment_module_type = models.IntegerField(blank=True, null=True)
    investment_module_inner_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'investment_module'


class JnCreditInfo(models.Model):
    entname = models.CharField(max_length=255)
    credit_grade = models.CharField(max_length=255, blank=True, null=True)
    credit_grade_num = models.IntegerField(blank=True, null=True)
    credit_grade_num_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jn_credit_info'


class JnSpecialNewInfo(models.Model):
    entname = models.CharField(max_length=255)
    is_jnsn = models.IntegerField(blank=True, null=True)
    is_jnsn_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jn_special_new_info'


class JnTechCenter(models.Model):
    entname = models.CharField(max_length=255)
    level_rank = models.IntegerField(blank=True, null=True)
    level_rank_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jn_tech_center'


class JudgeDeclareP(models.Model):
    entname = models.CharField(max_length=255)
    declaredate = models.CharField(max_length=255,blank=True, null=True)
    appellant_amount = models.IntegerField(blank=True, null=True)
    defendant_amount = models.IntegerField(blank=True, null=True)
    declaredate_type = models.IntegerField(blank=True, null=True)
    appellant_amount_type = models.IntegerField(blank=True, null=True)
    defendant_amount_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'judge_declare_p'


class JusticeCredit(models.Model):
    entname = models.CharField(max_length=255)
    is_justice_credit = models.IntegerField(blank=True, null=True)
    is_justice_credit_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'justice_credit'


class JusticeCreditAic(models.Model):
    entname = models.CharField(max_length=45)
    is_justice_creditaic = models.IntegerField(blank=True, null=True)
    is_justice_creditaic_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'justice_credit_aic'


class JusticeDeclare(models.Model):
    entname = models.CharField(max_length=255)
    declaredate = models.DateField(blank=True, null=True)
    appellant = models.IntegerField(blank=True, null=True)
    defendant = models.IntegerField(blank=True, null=True)
    declarestyle = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'justice_declare'


class JusticeDeclareTotal(models.Model):
    entname = models.CharField(max_length=255)
    appellant_total = models.IntegerField(blank=True, null=True)
    defendant_total = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'justice_declare_total'


class JusticeEnforced(models.Model):
    entname = models.CharField(max_length=255)
    record_date = models.DateField()
    enforce_amount = models.FloatField(blank=True, null=True)
    record_date_type = models.IntegerField(blank=True, null=True)
    enforce_amount_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'justice_enforced'


class JusticeEnforcedDealed(models.Model):
    entname = models.CharField(max_length=255)
    record_date = models.IntegerField(blank=True, null=True)
    enforced_amount = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'justice_enforced_dealed'


class JusticeEnforcedP(models.Model):
    entname = models.CharField(max_length=255)
    record_date = models.IntegerField(blank=True, null=True)
    enforce_amount = models.IntegerField(blank=True, null=True)
    record_date_type = models.IntegerField(blank=True, null=True)
    enforce_amount_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'justice_enforced_p'


class JusticeJudgeNew(models.Model):
    entname = models.CharField(max_length=255)
    time = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    casetype = models.CharField(max_length=255, blank=True, null=True)
    judgeresult = models.TextField(blank=True, null=True)
    casecause = models.CharField(max_length=255, blank=True, null=True)
    evidence = models.CharField(max_length=255, blank=True, null=True)
    courtrank = models.CharField(max_length=255, blank=True, null=True)
    datatype = models.CharField(max_length=255, blank=True, null=True)
    latypes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'justice_judge_new'


class JusticeJudgeNewCount(models.Model):
    entname = models.CharField(max_length=255)
    judge_new_count = models.IntegerField(blank=True, null=True)
    judge_new_count_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'justice_judge_new_count'


class JusticeRiskModule(models.Model):
    entname = models.CharField(max_length=255)
    appellant_total_type = models.IntegerField(blank=True, null=True)
    defendant_total_type = models.IntegerField(blank=True, null=True)
    enforce_amount_type = models.IntegerField(blank=True, null=True)
    record_date_type = models.IntegerField(blank=True, null=True)
    judge_new_count_type = models.IntegerField(blank=True, null=True)
    is_justice_credit_type = models.IntegerField(blank=True, null=True)
    is_justice_creditaic_type = models.IntegerField(blank=True, null=True)
    justice_risk_module_mark = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'justice_risk_module'


class ProductCheckinfoConnect(models.Model):
    entname = models.CharField(max_length=255)
    passpercent = models.FloatField(blank=True, null=True)
    passpercent_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_checkinfo_connect'


class QualityModule(models.Model):
    entname = models.CharField(max_length=255)
    passpercent = models.FloatField(blank=True, null=True)
    quality_module_mark = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quality_module'


class RecruitModule(models.Model):
    entname = models.CharField(max_length=255)
    qcwynum = models.IntegerField(blank=True, null=True)
    zhycnum = models.IntegerField(blank=True, null=True)
    zlzpnum = models.IntegerField(blank=True, null=True)
    recruit_module = models.IntegerField(blank=True, null=True)
    recruit_module_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recruit_module'


class RiskModule(models.Model):
    entname = models.CharField(max_length=255)
    is_punish_type = models.IntegerField(blank=True, null=True,default=0)
    is_bra_type = models.IntegerField(blank=True, null=True,default=0)
    is_brap_type = models.IntegerField(blank=True, null=True,default=0)
    pledgenum_type = models.IntegerField(blank=True, null=True,default=0)
    taxunpaidnum_type = models.IntegerField(blank=True, null=True,default=0)
    unpaid_sum_type = models.IntegerField(blank=True, null=True,default=0)
    is_except_type = models.IntegerField(blank=True, null=True,default=0)
    declaredate_type = models.IntegerField(blank=True, null=True,default=0)
    appellant_amount_type = models.IntegerField(blank=True, null=True,default=0)
    defendant_amount_type = models.IntegerField(blank=True, null=True,default=0)
    is_justice_credit_type = models.IntegerField(blank=True, null=True,default=0)
    is_justice_creditaic_type = models.IntegerField(blank=True, null=True,default=0)
    record_date_type = models.IntegerField(blank=True, null=True,default=0)
    enforce_amount_type = models.IntegerField(blank=True, null=True,default=0)
    judge_new_count_type = models.IntegerField(blank=True, null=True,default=0)
    risk_module_inner_type = models.IntegerField(blank=True, null=True,default=0)
    risk_module_type = models.IntegerField(blank=True, null=True,default=0)
    risk_module = models.FloatField(blank=True, null=True,default=0)

    class Meta:
        managed = False
        db_table = 'risk_module'


class TrademarkInfoa(models.Model):
    entname = models.CharField(max_length=255)
    is_infoa = models.IntegerField(blank=True, null=True)
    is_infoa_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trademark_infoa'


class TrademarkInfob(models.Model):
    entname = models.CharField(max_length=255)
    is_infob = models.IntegerField(blank=True, null=True)
    is_infob_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trademark_infob'


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'


class UserUserprofile(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=100, blank=True, null=True)
    roles = models.IntegerField(blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_userprofile'


class UserUserprofileGroups(models.Model):
    userprofile = models.ForeignKey(UserUserprofile, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_userprofile_groups'
        unique_together = (('userprofile', 'group'),)


class UserUserprofileUserPermissions(models.Model):
    userprofile = models.ForeignKey(UserUserprofile, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_userprofile_user_permissions'
        unique_together = (('userprofile', 'permission'),)


class WebRecordInfo(models.Model):
    entname = models.CharField(max_length=255)
    idom_num = models.IntegerField(blank=True, null=True)
    idom_num_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'web_record_info'
