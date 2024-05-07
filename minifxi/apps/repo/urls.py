
from django.urls import path, re_path
from apps.repo import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login


 
urlpatterns = [

	# ----------------  G R A F I C O S   -----------------
	re_path(r'^rep001$',login_required(views.Graficos.as_view()),name='rep001'),
	re_path(r'^rep002$',login_required(views.Rep002.as_view()),name='rep002'),
	re_path(r'^rep003$',login_required(views.Rep003.as_view()),name='rep003'),
	re_path(r'^rep004$',login_required(views.Rep004.as_view()),name='rep004'), # Acotamiento de error en incurrido

	# Acumulados por Equipo y intervalos de fechas
	re_path(r'^rep005/$',login_required(views.Rep005.as_view()),name='rep005'),  
	re_path(r'^rep006/$',login_required(views.Rep006.as_view()),name='rep006'), 

	# --- IBM ---
	re_path(r'^rep007/$',login_required(views.Rep007.as_view()),name='rep007'),  

]

