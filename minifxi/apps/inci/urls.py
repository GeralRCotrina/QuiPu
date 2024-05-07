
from django.urls import re_path
from apps.inci import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login

 
urlpatterns = [
	# --------------I N C I D E N C I A  --------
	re_path(r'^inc_cre/(?P<pk>\d+)/$',login_required(views.IncCre.as_view()),name='inc_cre'),
	re_path(r'^inc_lis/$',login_required(views.IncLis.as_view()),name='inc_lis'),
	re_path(r'^inc_eli/(?P<pk>\d+)/$',login_required(views.IncEli.as_view()),name='inc_eli'),
	re_path(r'^inc_edi/(?P<pk>\d+)/$',login_required(views.IncEdi.as_view()),name='inc_edi'),
	re_path(r'^inc_exp/$',login_required(views.IncExp.as_view()),name='inc_exp'),
	re_path(r'^inc_xreq/$',login_required(views.IncXReq.as_view()),name='inc_xreq'),
	re_path(r'^inc_xpet/$',login_required(views.IncXPet.as_view()),name='inc_xpet'),

]

