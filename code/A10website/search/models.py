# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# from ent_manage.models import CompanyBaseinfoSummary


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
    # baseinfo = models.OneToOneField(CompanyBaseinfoSummary, to_field="id",on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'ent_module'
