from django.conf.urls import url

from entInfo import views

urlpatterns = [
    url(r'^basic$',views.basicInfoView.as_view({'post':'list'}),name='basicInfo'),
    url(r'^intellectualProperty$',views.creativityInfoView.as_view({'post':'list'}),name='creativityInfo'),
    url(r'^recruit$',views.recruitInfoView.as_view({'post':'list'}),name='recruitInfo'),
    url(r'^investment$',views.investmentInfoView.as_view({'post':'list'}),name='investmentInfo'),
    url(r'^judicialDispute$',views.justicDeclareInfoView.as_view({'post':'list'}),name='justicDeclareInfoInfo'),
    url(r'^punishment$',views.punishmentInfoView.as_view({'post':'list'}),name='punishmentInfo'),
    url(r'^overdraft$',views.entSocialSecurityInfoView.as_view({'post':'list'}),name='entSocialSecurityInfo'),
    url(r'^credit$',views.creditInfoView.as_view({'post':'list'}),name='creditInfo'),
    url(r'^brand$', views.brandInfoView.as_view({'post': 'list'}), name='brandInfo'),
    url(r'^tag$',views.tagInfoView.as_view({'post':'list'}),name='tagInfo'),
    url(r'^recommend$',views.recommendView.as_view({'post':'list'}),name='Recommend'),
    url(r'^compareEnt$',views.compareEntView.as_view({'post':'list'}),name='compareEnt'),
    url(r'^reporturl$',views.dataToJsonView.as_view({'post':'list'}),name='report'),

]