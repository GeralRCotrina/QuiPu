

from django.urls import re_path
from apps.requ import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
#from django.contrib.auth.views import logout_then_login

 
urlpatterns = [

	# ----------------  R E Q U E R I M E N T O -----------------
	re_path(r'^req_crear/$',login_required(views.ReqCrear.as_view()),name='req_crear'),
	re_path(r'^req_eliminar/(?P<pk>\d+)/$',login_required(views.ReqEliminar.as_view()),name='req_eliminar'),
	re_path(r'^req_listar/$',login_required(views.ReqListar.as_view()),name='req_listar'),
	re_path(r'^req_editar/(?P<pk>\d+)/$',login_required(views.ReqEditar.as_view()),name='req_editar'),
	re_path(r'^req_duplic/(?P<pk>\d+)/$',login_required(views.ReqDuplic.as_view()),name='req_duplic'),
	re_path(r'^req_agr_comn/$',login_required(views.ReqAgrComn.as_view()),name='req_agr_comn'),
	re_path(r'^req_x_pet/$',login_required(views.ReqPorPet.as_view()),name='req_x_pet'),

	re_path(r'^req_crear1/(?P<pk>\d+)/$',login_required(views.ReqCrearRef.as_view()),name='req_crear1'),
	re_path(r'^req_bita/(?P<pk>\d+)/$',login_required(views.ReqBita.as_view()),name='req_bita'),
	re_path(r'^req_upd_bit/(?P<pk>\d+)/$',login_required(views.ReqUpdBit.as_view()),name='req_upd_bit'), # Ajax POST
	
	re_path(r'^req_filt/$',login_required(views.ReqFilt.as_view()),name='req_filt'),

]


"""

	# ----------------  E S T A T U S  -----------------
	re_path(r'^est_cre/$',login_required(views.EstCrear.as_view()),name='est_cre'),
	
 	# ----------------  P E T C I Ó N -----------------
 	re_path(r'^pet_crear/$',login_required(views.PetCrear.as_view()),name='pet_crear'),
 	re_path(r'^pet_eliminar/(?P<pk>\d+)/$',login_required(views.PetEliminar.as_view()),name='pet_eliminar'),
 	re_path(r'^pet_listar/$',login_required(views.PetListar.as_view()),name='pet_listar'),
 	re_path(r'^pet_editar/(?P<pk>\d+)/$',login_required(views.PetEditar.as_view()),name='pet_editar'),
         

"""