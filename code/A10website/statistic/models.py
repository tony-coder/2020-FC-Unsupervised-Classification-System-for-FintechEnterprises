from django.db import models

# Create your models here.

from django.db import models


class EntModuleWeight(models.Model):
    risk_module_type = models.FloatField(blank=True, null=True, default=0.0)
    investment_module_type = models.FloatField(blank=True, null=True, default=0.0)
    creativity_module_type = models.FloatField(blank=True, null=True, default=0.0)
    brand_module_type = models.FloatField(blank=True, null=True, default=0.0)
    recruit_module_type = models.FloatField(blank=True, null=True, default=0.0)
    credit_module_type = models.FloatField(blank=True, null=True, default=0.0)
    base_module_type = models.FloatField(blank=True, null=True, default=0.0)

    class Meta:
        managed = False
        db_table = 'ent_module_weight'


class RiskModuleWeight(models.Model):
    is_punish_type = models.FloatField(blank=True, null=True, default=0.0)
    is_bra_type = models.FloatField(blank=True, null=True, default=0.0)
    is_brap_type = models.FloatField(blank=True, null=True, default=0.0)
    pledgenum_type = models.FloatField(blank=True, null=True, default=0.0)
    taxunpaidnum_type = models.FloatField(blank=True, null=True, default=0.0)
    unpaid_sum_type = models.FloatField(blank=True, null=True, default=0.0)
    is_except_type = models.FloatField(blank=True, null=True, default=0.0)
    declaredate_type = models.FloatField(blank=True, null=True, default=0.0)
    appellant_amount_type = models.FloatField(blank=True, null=True, default=0.0)
    defendant_amount_type = models.FloatField(blank=True, null=True, default=0.0)
    record_date_type = models.FloatField(blank=True, null=True, default=0.0)
    enforce_amount_type = models.FloatField(blank=True, null=True, default=0.0)
    judge_new_count_type = models.FloatField(blank=True, null=True, default=0.0)
    is_justice_credit_type = models.FloatField(blank=True, null=True, default=0.0)
    is_justice_creditaic_type = models.FloatField(blank=True, null=True, default=0.0)

    class Meta:
        managed = False
        db_table = 'risk_module_weight'