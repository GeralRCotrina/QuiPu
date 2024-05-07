
from django.urls import path, re_path
from apps.duda import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login

 
urlpatterns = [

	# --------------D U D A S  --------
	re_path(r'^dud_cre1/(?P<pk>\d+)/$',login_required(views.DudCreRef.as_view()),name='dud_cre1'),
	re_path(r'^dud_lis/$',login_required(views.DudLis.as_view()),name='dud_lis'),
	re_path(r'^dud_eli/(?P<pk>\d+)/$',login_required(views.DudEli.as_view()),name='dud_eli'),
	re_path(r'^dud_edi/(?P<pk>\d+)/$',login_required(views.DudEdi.as_view()),name='dud_edi'),
	re_path(r'^dud_exp/$',login_required(views.DudExp.as_view()),name='dud_exp'),
	re_path(r'^dud_xreq/$',login_required(views.DudXReq.as_view()),name='dud_xreq'),
	re_path(r'^dud_xpet/$',login_required(views.DudXPet.as_view()),name='dud_xpet'),

]



