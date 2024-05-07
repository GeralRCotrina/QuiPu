
from django.urls import path, re_path
from apps.peti import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
#from django.contrib.auth.views import logout_then_login

 
urlpatterns = [
   
	# ----------------  P E T C I Ó N -----------------
	re_path(r'^pet_crear/$',login_required(views.PetCrear.as_view()),name='pet_crear'),
	re_path(r'^pet_eliminar/(?P<pk>\d+)/$',login_required(views.PetEliminar.as_view()),name='pet_eliminar'),
	re_path(r'^pet_listar/$',login_required(views.PetListar.as_view()),name='pet_listar'),
	re_path(r'^pet_editar/(?P<pk>\d+)/$',login_required(views.PetEditar.as_view()),name='pet_editar'),

]

