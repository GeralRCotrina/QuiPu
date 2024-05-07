
from django.urls import re_path
from apps.esta   import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login

 
urlpatterns = [

	# ----------------  E S T A T U S  ----------------- # 
	re_path(r'^est_cre/$',login_required(views.EstCrear.as_view()),name='est_cre'),


	# ----------------  D A I L Y  ----------------- # 
	re_path(r'^dai_lis/$',login_required(views.Daily.as_view()),name='dai_lis'),
	re_path(r'^dai_upd/$',login_required(views.DaiUpd.as_view()),name='dai_upd'),

]

