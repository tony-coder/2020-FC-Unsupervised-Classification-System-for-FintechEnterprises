from rest_framework import serializers

# from ent_manage import models
from dataTojson import models
from dataTojson.models import EntModule, CompanyBaseinfoSummary


class BasicInfoSerializer(serializers.ModelSerializer):
    legalRepresentative = serializers.SerializerMethodField("get_legalRepresentative")
    phoneNumber = serializers.SerializerMethodField("get_phoneNumber")
    address = serializers.SerializerMethodField("get_address")
    registrationCode = serializers.SerializerMethodField("get_registrationCode")

    def get_legalRepresentative(self, obj):
        return ""

    def get_phoneNumber(self, obj):
        return ""

    def get_registrationCode(self, obj):
        return ""

    def get_address(self, obj):
        return ""

    def to_representation(self, instance):
        old_dict = super().to_representation(instance)
        dict = {}
        dict['enterpriseName'] = old_dict["entname"]
        dict["registrationStatus"] = old_dict["entstatus"]
        dict['id'] = old_dict["entname"]
        dict["legalRepresentative"] = old_dict["legalRepresentative"]
        dict["dateOfEstablishment"] = old_dict["estdate"]
        dict["phoneNumber"] = old_dict["phoneNumber"]
        dict["type"] = old_dict["enttype"]
        dict["registeredCapital"] = old_dict["regcap"]
        dict["businessTermStart"] = old_dict["opfrom"]
        dict["businessTermEnd"] = old_dict["opto"]
        dict["scopeOfBusiness"] = old_dict["industryphy"]
        dict["registrationCode"] = old_dict["registrationCode"]
        dict["address"] = old_dict["address"]
        dict["empnum"] = old_dict["empnum"]
        del old_dict

        return dict

    class Meta:
        model = models.CompanyBaseinfoSummary
        fields = ["entname","entstatus","estdate","enttype", \
                 "regcap","opfrom","opto","empnum","industryphy","legalRepresentative","phoneNumber","address","empnum","registrationCode"]


class RecruitInfoSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        old_dict = super().to_representation(instance)
        dict = {}
        dict['qcwynum'] = old_dict["qcwynum"]
        dict["zhycnum"] = old_dict["zhycnum"]
        dict['zlzpnum'] = old_dict["zlzpnum"]
        dict["recruit_sum"] = old_dict["recruit_module"]
        dict["rank"] = old_dict["recruit_module_type"]
        del old_dict

        return dict

    class Meta:
        model = models.RecruitModule
        fields = ["qcwynum","zhycnum","zlzpnum","recruit_module","recruit_module_type"]

class JusticeDeclareSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JusticeDeclare
        fields = ["declaredate","appellant","defendant","declarestyle"]

class EntSocialSecuritySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EntSocialSecurity
        fields = ["unpaidsocialins_so110","unpaidsocialins_so210","unpaidsocialins_so310","unpaidsocialins_so410","unpaidsocialins_so510","updatetime"]


class TagInfoSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        old_dict = super().to_representation(instance)
        dict = {}
        dict['totScore'] = old_dict["ent_type"]
        dict["riskScore"] = old_dict["risk_module_type"]
        dict['investmentScore'] = old_dict["investment_module_type"]
        dict["intellectualPropertyScore"] = old_dict["creativity_module_type"]
        dict["brandScore"] = old_dict["brand_module_type"]
        dict["recruitScore"] = old_dict["recruit_module_type"]
        dict["creditScore"] = old_dict["credit_module_type"]
        del old_dict

        return dict

    class Meta:
        model = models.EntModule
        fields = ['risk_module_type','investment_module_type','creativity_module_type','brand_module_type','recruit_module_type','credit_module_type','ent_type']

class RecommendSerializer(serializers.ModelSerializer):
    enttype = serializers.CharField(source='baseinfo.enttype')

    def to_representation(self, instance):
        old_dict = super().to_representation(instance)
        dict = {}
        dict['id'] = old_dict["entname"]
        dict['entname'] = old_dict["entname"]
        dict["type"] = old_dict["enttype"]
        del old_dict

        return dict

    class Meta:
        model = models.EntModule
        fields = ['entname', 'enttype']


class CompareEntSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        old_dict = super().to_representation(instance)
        dict = {}
        dict['name'] = old_dict["entname"]
        dict['type'] = 'bar'
        dict['barWidth'] = 20
        data = []
        data.append(old_dict['risk_module_type'])
        data.append(old_dict['investment_module_type'])
        data.append(old_dict['creativity_module_type'])
        data.append(old_dict['brand_module_type'])
        data.append(old_dict['recruit_module_type'])
        data.append(old_dict['credit_module_type'])
        data.append(old_dict['company_baseinfo_module_type'])

        dict['data'] = data
        dict['animationDuration'] = 6000

        del old_dict

        return dict


    class Meta:
        model = models.EntModule
        fields = ['entname','risk_module_type', 'investment_module_type', 'creativity_module_type', 'brand_module_type',
                  'recruit_module_type', 'credit_module_type', 'company_baseinfo_module_type']

class EntSearchSerializer(serializers.ModelSerializer):
    legalRepresentative = serializers.SerializerMethodField()
    phoneNumber = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    risk_module_type = serializers.IntegerField(source='entmodule.risk_module_type')
    investment_module_type = serializers.IntegerField(source='entmodule.investment_module_type')
    creativity_module_type = serializers.IntegerField(source='entmodule.creativity_module_type')
    brand_module_type = serializers.IntegerField(source='entmodule.brand_module_type')
    recruit_module_type = serializers.IntegerField(source='entmodule.recruit_module_type')
    credit_module_type = serializers.IntegerField(source='entmodule.credit_module_type')
    company_baseinfo_module_type = serializers.IntegerField(source='entmodule.company_baseinfo_module_type')

    class Meta:
        model = CompanyBaseinfoSummary
        fields = ["entname", "regcap", "estdate", "entstatus", "imag", "legalRepresentative", "phoneNumber",
                  "email", "address","entmodule","risk_module_type","investment_module_type","creativity_module_type",
                  "brand_module_type","recruit_module_type","credit_module_type","company_baseinfo_module_type"]

    def get_legalRepresentative(self, obj):
        return ""

    def get_phoneNumber(self, obj):
        return ""

    def get_email(self, obj):
        return ""

    def get_address(self, obj):
        return ""

    def to_representation(self, instance):
        old_dict = super().to_representation(instance)
        dict = {}
        dict['id'] = old_dict["entname"]
        dict['enterpriseName'] = old_dict["entname"]
        dict["registeredCapital"] = old_dict["regcap"]
        dict["dateOfEstablishment"] = old_dict["estdate"]
        # dict["entstatus"] = old_dict["entstatus"]
        # dict["imag"] = old_dict["imag"]
        dict["legalRepresentative"] = old_dict["legalRepresentative"]
        dict["phoneNumber"] = old_dict["phoneNumber"]
        dict["email"] = old_dict["email"]
        dict["address"] = old_dict["address"]
        tagListRank = []
        tagListRank.append(old_dict["risk_module_type"])
        tagListRank.append(old_dict["investment_module_type"])
        tagListRank.append(old_dict["creativity_module_type"])
        tagListRank.append(old_dict["brand_module_type"])
        tagListRank.append(old_dict["recruit_module_type"])
        tagListRank.append(old_dict["credit_module_type"])
        tagListRank.append(old_dict["company_baseinfo_module_type"])
        dict["tagRankList"] = tagListRank
        dict["riskRank"] = old_dict["risk_module_type"]
        dict["investmentRank"] = old_dict["investment_module_type"]
        dict["creativityRank"] = old_dict["creativity_module_type"]
        dict["brandRank"] = old_dict["brand_module_type"]
        dict["recruitRank"] = old_dict["recruit_module_type"]
        dict["creditRank"] = old_dict["credit_module_type"]


        del old_dict

        return dict
