from rest_framework import serializers
from rest_framework.utils import json

from ent_manage.models import CompanyBaseinfoSummary


class TipSerializer(serializers.ModelSerializer):
    searchType = serializers.SerializerMethodField('get_searchType')

    def to_representation(self, instance):
        old_dict = super().to_representation(instance)
        dict = {}
        dict['id'] = old_dict["entname"]
        dict['enterpriseName'] = old_dict["entname"]
        dict['Field'] = old_dict["searchType"]
        dict['Value'] = old_dict["entname"]
        del old_dict

        return dict

    class Meta:
        model = CompanyBaseinfoSummary
        fields = ["entname","searchType"]

    def get_searchType(self, obj):
        request = self.context['request']

        req = json.loads(request.body.decode())
        searchType = int(req['searchType'][0])
        # searchType = int(request.POST.get('searchType'))
        return searchType