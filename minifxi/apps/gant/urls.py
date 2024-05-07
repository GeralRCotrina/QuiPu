
from django.urls import path, re_path
from apps.gant import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
#from django.contrib.auth.views import logout_then_login

 
urlpatterns = [

	# ----------------  G A N T  -----------------
	re_path(r'^gant/$',login_required(views.GantIni),name='gant'),
	re_path(r'^gnt_c1/$',login_required(views.Gnt_c1.as_view()),name='gnt_c1'), # Valida cada click en el gant y crea/actualiza
	re_path(r'^gnt_vd1/$',login_required(views.Gnt_vd1.as_view()),name='gnt_vd1'),
	re_path(r'^gnt_d1/$',login_required(views.Gnt_d1.as_view()),name='gnt_d1'),
	#re_path(r'^gnt_lst/$',login_required(views.GntLst.as_view()),name='gnt_lst'),
	re_path(r'^gnt_asg/$',login_required(views.ObtAsignaciones.as_view()),name='gnt_asg'),
	re_path(r'^gnt_d2/$',login_required(views.Gnt_d2.as_view()),name='gnt_d2'), # Datalle del gant

	#re_path(r'^gnt_sjd/$',login_required(views.Gnt_Ajd.as_view()),name='gnt_sjd'), #  Ajuste de H.Acuerdo diarios
	re_path(r'^gnt_haj_get/$',login_required(views.GntHajLst.as_view()),name='gnt_haj_get'), #  Ajuste de H.Acuerdo diarios
	re_path(r'^gnt_haj_mdf/$',login_required(views.GntHajMdf.as_view()),name='gnt_haj_mdf'), 
	re_path(r'^gnt_dnl_get/$',login_required(views.GntDnlLst.as_view()),name='gnt_dnl_get'), # Días no laborables
	re_path(r'^gnt_dnl_upd/$',login_required(views.GntDnlUpd.as_view()),name='gnt_dnl_upd'),
	re_path(r'^gnt_dnl_ref/$',login_required(views.GntDnlRef.as_view()),name='gnt_dnl_ref'),

]
 
