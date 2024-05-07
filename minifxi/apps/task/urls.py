
from django.urls import path, re_path
from apps.task import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login

 
urlpatterns = [

	# ----------------  T A S K  -----------------
	re_path(r'^task_crear/$',login_required(views.TaskCrear.as_view()),name='task_crear'),
	re_path(r'^task_crear1/(?P<pk>\d+)/$',login_required(views.TaskCrearRef.as_view()),name='task_crear1'),
	#re_path(r'^task_crear1/(?P<pk>\d+)/$',login_required(views.TaskCrearRef_GRCL.as_view()),name='task_crear1'),
	re_path(r'^task_eliminar/(?P<pk>\d+)/$',login_required(views.TaskEliminar.as_view()),name='task_eliminar'),

	re_path(r'^task_listar/$',login_required(views.TaskListar.as_view()),name='task_listar'),
	re_path(r'^task_sf/$',login_required(views.SubidaAFenix.as_view()),name='task_sf'),
	re_path(r'^task_x_codigo/$',login_required(views.TaskPorCodigo.as_view()),name='task_x_codigo'),
	re_path(r'^task_x_req/$',login_required(views.TaskPorReq.as_view()),name='task_x_req'),
	re_path(r'^act_task/$',login_required(views.ActTask.as_view()),name='act_task'),
	re_path(r'^task_acc/$',login_required(views.TaskACC.as_view()),name='task_acc'),
	re_path(r'^task_editar/(?P<pk>\d+)/$',login_required(views.TaskEditar.as_view()),name='task_editar'),

	re_path(r'^task_x_pet/$',login_required(views.TaskXPet.as_view()),name='task_x_pet'),

	# Crea varias tarea para un requerimiento
	re_path(r'^tsk_cre_lst/$',login_required(views.TaskCreLst.as_view()),name='tsk_cre_lst'),
	re_path(r'^tsk_lst_ext/$',login_required(views.TaskLstExt.as_view()),name='tsk_lst_ext'),


]



