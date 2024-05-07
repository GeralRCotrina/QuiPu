
from django.urls import re_path
from apps.esti   import views
from django.contrib.auth.decorators import login_required

 
urlpatterns = [

	# -------------- E S T I M   P E S O   -------- #

	re_path(r'^estim_cre/$',login_required(views.EstimCre.as_view()),name='estim_cre'),
	re_path(r'^estim_lis/$',login_required(views.EstimLis.as_view()),name='estim_lis'),
	re_path(r'^estim_eli/(?P<pk>\d+)/$',login_required(views.EstimEli.as_view()),name='estim_eli'),
	re_path(r'^estim_edi/(?P<pk>\d+)/$',login_required(views.EstimEdi.as_view()),name='estim_edi'),

	# -------------- E S T I M   D E T A L L E   -------- #
	re_path(r'^etimdet_peso/$',login_required(views.DetPeso.as_view()),name='etimdet_peso'),
	re_path(r'^etimdet_cre/$',login_required(views.DetCre.as_view()),name='etimdet_cre'),
	re_path(r'^etimdet_apro/$',login_required(views.DetApro.as_view()),name='etimdet_apro'),
	re_path(r'^etimdet_lis/$',login_required(views.DetLis.as_view()),name='etimdet_lis'),
	re_path(r'^etimdet_eli/$',login_required(views.DetEli.as_view()),name='etimdet_eli'),
	re_path(r'^etimdet_ajs/$',login_required(views.DetAjs.as_view()),name='etimdet_ajs'),

	re_path(r'^etimdet_exp/$',login_required(views.DetExp.as_view()),name='etimdet_exp'),
	

]

 