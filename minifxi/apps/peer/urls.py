
from django.urls import path, re_path
from apps.peer import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
#from django.contrib.auth.views import logout_then_login

 
urlpatterns = [

	# ------------ P E E R   R E V I E W -----
	re_path(r'^pr_cre/(?P<pk>\d+)/$',login_required(views.PrCre.as_view()),name='pr_cre'),
	re_path(r'^pr_lis/$',login_required(views.PrLis.as_view()),name='pr_lis'),
	re_path(r'^pr_edi/(?P<pk>\d+)/$',login_required(views.PrEdi.as_view()),name='pr_edi'),
	re_path(r'^pr_eli/(?P<pk>\d+)/$',login_required(views.PrEli.as_view()),name='pr_eli'),

]

