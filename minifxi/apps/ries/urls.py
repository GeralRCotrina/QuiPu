
from django.urls import path, re_path
from apps.ries import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login


 
urlpatterns = [

	# --------------R I E S G O   --------
	re_path(r'^rie_cre/(?P<pk>\d+)/$',login_required(views.RieCre.as_view()),name='rie_cre'),
	re_path(r'^rie_lis/$',login_required(views.RieLis.as_view()),name='rie_lis'),
	re_path(r'^rie_eli/(?P<pk>\d+)/$',login_required(views.RieEli.as_view()),name='rie_eli'),
	re_path(r'^rie_edi/(?P<pk>\d+)/$',login_required(views.RieEdi.as_view()),name='rie_edi'),
	re_path(r'^rie_xreq/$',login_required(views.RieXReq.as_view()),name='rie_xreq'),
	re_path(r'^rie_xpet/$',login_required(views.RieXPet.as_view()),name='rie_xpet'),

]




