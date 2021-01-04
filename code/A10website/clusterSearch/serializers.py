from rest_framework import serializers

from ent_manage.models import CompanyBaseinfoSummary

class clusterSearchSerializer(serializers.ModelSerializer):
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
        fields = ["entname", "regcap", "estdate","legalRepresentative", "phoneNumber",
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
        dict["legalRepresentative"] = old_dict["legalRepresentative"]
        dict["phoneNumber"] = old_dict["phoneNumber"]
        dict["email"] = old_dict["email"]
        dict["address"] = old_dict["address"]
        dict["riskRank"] = old_dict["risk_module_type"]
        dict["investmentRank"] = old_dict["investment_module_type"]
        dict["creativityRank"] = old_dict["creativity_module_type"]
        dict["brandRank"] = old_dict["brand_module_type"]
        dict["recruitRank"] = old_dict["recruit_module_type"] 
        dict["creditRank"] = old_dict["credit_module_type"]
        dict["baseRank"] = old_dict["company_baseinfo_module_type"]
        tagListRank = []
        tagListRank.append(old_dict["risk_module_type"])
        tagListRank.append(old_dict["investment_module_type"])
        tagListRank.append(old_dict["creativity_module_type"])
        tagListRank.append(old_dict["brand_module_type"])
        tagListRank.append(old_dict["recruit_module_type"])
        tagListRank.append(old_dict["credit_module_type"])
        tagListRank.append(old_dict["company_baseinfo_module_type"])
        dict["tagRankList"] = tagListRank


        del old_dict

        return dict