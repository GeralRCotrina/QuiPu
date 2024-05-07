
from django.urls import path, re_path
from apps.gestion import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
#from django.contrib.auth.views import logout_then_login

 
urlpatterns = [
	re_path(r'^mylogin$', views.mylogin,name='mylogin'),
	re_path(r'^logout$',login_required(logout_then_login),name='logout'),
	re_path(r'^$',login_required(views.panel.as_view()),name='index'),
	re_path(r'^panel/$',login_required(views.panel.as_view()),name='panel'),
    re_path(r'^log/$',login_required(views.LogDeAccion1),name='log'),
    re_path(r'^err/$',login_required(views.ErrorPage),name='err'),
    

	# ----------------  E S T A T U S  -----------------


    # ----------------  P E T C I Ó N -----------------


	# ----------------  R E Q U E R I M E N T O -----------------


	# ----------------  T A S K  -----------------
	

	# ----------------  S F   -----------------
	re_path(r'^act_sf/$',login_required(views.ActSF.as_view()),name='act_sf'),


	# ----------------  G A N T  -----------------


	# ----------------  G R A F I C O S   -----------------


	# ----------------  T E A M  -----------------
	re_path(r'^col_cre/$',login_required(views.ColCre.as_view()),name='col_cre'),
	re_path(r'^col_lis/$',login_required(views.ColLis.as_view()),name='col_lis'),
	re_path(r'^col_lis2/$',login_required(views.ColLis2.as_view()),name='col_lis2'),
	re_path(r'^col_eli/(?P<pk>\d+)/$',login_required(views.ColEli.as_view()),name='col_eli'),
	re_path(r'^col_edi/(?P<pk>\d+)/$',login_required(views.ColEdi.as_view()),name='col_edi'),
	re_path(r'^col/fot/$',login_required(views.ColFot.as_view()),name='col/fot'),
	re_path(r'^col_ediu/(?P<pk>\d+)/$',login_required(views.ColEdiU.as_view()),name='col_ediu'),
	#re_path(r'^col_edif/$',login_required(views.ColEdiF.as_view()),name='col_edif'),
	re_path(r'^col_edif/(?P<pk>\d+)/$',login_required(views.ColEdiF.as_view()),name='col_edif'),
	re_path(r'^col_set_pas/$',login_required(views.CambPass1.as_view()),name='col_pas'),
	re_path(r'^col_pas/$',login_required(views.CambPass2.as_view()),name='col_pas'),




	# --------------D O M --------
	re_path(r'^dom_cre/$',login_required(views.DomCre.as_view()),name='dom_cre'),
	re_path(r'^dom_lis/$',login_required(views.DomLis.as_view()),name='dom_lis'),
	re_path(r'^dom_eli/(?P<pk>\d+)/$',login_required(views.DomEli.as_view()),name='dom_eli'),
	re_path(r'^dom_edi/(?P<pk>\d+)/$',login_required(views.DomEdi.as_view()),name='dom_edi'),

	# --------------E Q U  --------
	re_path(r'^equ_cre/$',login_required(views.EquCre.as_view()),name='equ_cre'),
	re_path(r'^equ_lis/$',login_required(views.EquLis.as_view()),name='equ_lis'),
	re_path(r'^equ_eli/(?P<pk>\d+)/$',login_required(views.EquEli.as_view()),name='equ_eli'),
	re_path(r'^equ_edi/(?P<pk>\d+)/$',login_required(views.EquEdi.as_view()),name='equ_edi'),

	re_path(r'^equ_det_lis/$',login_required(views.EquDetLis.as_view()),name='equ_det_lis'),# grcl4
	re_path(r'^equ_det_cre/$',login_required(views.EquDetCre.as_view()),name='equ_det_cre'),
	re_path(r'^equ_det_eli/$',login_required(views.EquDetEli.as_view()),name='equ_det_eli'),
	
	

	# --------------C L I  --------
	re_path(r'^cli_cre/$',login_required(views.CliCre.as_view()),name='cli_cre'),
	re_path(r'^cli_lis/$',login_required(views.CliLis.as_view()),name='cli_lis'),
	re_path(r'^cli_eli/(?P<pk>\d+)/$',login_required(views.CliEli.as_view()),name='cli_eli'),
	re_path(r'^cli_edi/(?P<pk>\d+)/$',login_required(views.CliEdi.as_view()),name='cli_edi'),
	re_path(r'^cli_lis2/$',login_required(views.CliLis2.as_view()),name='cli_lis2'),

	# --------------P A I  --------
	re_path(r'^pai_cre/$',login_required(views.PaiCre.as_view()),name='pai_cre'),
	re_path(r'^pai_lis/$',login_required(views.PaiLis.as_view()),name='pai_lis'),
	re_path(r'^pai_eli/(?P<pk>\d+)/$',login_required(views.PaiEli.as_view()),name='pai_eli'),
	re_path(r'^pai_edi/(?P<pk>\d+)/$',login_required(views.PaiEdi.as_view()),name='pai_edi'),

	# --------------I N C   T I P O  --------
	re_path(r'^inc_t_cre/$',login_required(views.IncTipCre.as_view()),name='inc_t_cre'),
	re_path(r'^inc_t_lis/$',login_required(views.IncTipLis.as_view()),name='inc_t_lis'),
	re_path(r'^inc_t_eli/(?P<pk>\d+)/$',login_required(views.IncTipEli.as_view()),name='inc_t_eli'),
	re_path(r'^inc_t_edi/(?P<pk>\d+)/$',login_required(views.IncTipEdi.as_view()),name='inc_t_edi'),

	# --------------I N C   E N C. E N  --------
	re_path(r'^inc_ee_cre/$',login_required(views.IncEECre.as_view()),name='inc_ee_cre'),
	re_path(r'^inc_ee_lis/$',login_required(views.IncEELis.as_view()),name='inc_ee_lis'),
	re_path(r'^inc_ee_eli/(?P<pk>\d+)/$',login_required(views.IncEEEli.as_view()),name='inc_ee_eli'),
	re_path(r'^inc_ee_edi/(?P<pk>\d+)/$',login_required(views.IncEEEdi.as_view()),name='inc_ee_edi'),

	# --------------I N C   E N C. E N  --------
	re_path(r'^pet_est_cre/$',login_required(views.PetEstCre.as_view()),name='pet_est_cre'),
	re_path(r'^pet_est_lis/$',login_required(views.PetEstLis.as_view()),name='pet_est_lis'),
	re_path(r'^pet_est_eli/(?P<pk>\d+)/$',login_required(views.PetEstEli.as_view()),name='pet_est_eli'),
	re_path(r'^pet_est_edi/(?P<pk>\d+)/$',login_required(views.PetEstEdi.as_view()),name='pet_est_edi'),

	# --------------I N C I D E N C I A  --------


	# --------------R I E S G O   --------

	# --------------R I E   C A T  --------
	re_path(r'^rie_cat_cre/$',login_required(views.RieCatCre.as_view()),name='rie_cat_cre'),
	re_path(r'^rie_cat_lis/$',login_required(views.RieCatLis.as_view()),name='rie_cat_lis'),
	re_path(r'^rie_cat_eli/(?P<pk>\d+)/$',login_required(views.RieCatEli.as_view()),name='rie_cat_eli'),
	re_path(r'^rie_cat_edi/(?P<pk>\d+)/$',login_required(views.RieCatEdi.as_view()),name='rie_cat_edi'),

	# --------------D U D   R E L  --------
	re_path(r'^dud_ra_cre/$',login_required(views.DudRACre.as_view()),name='dud_ra_cre'),
	re_path(r'^dud_ra_lis/$',login_required(views.DudRALis.as_view()),name='dud_ra_lis'),
	re_path(r'^dud_ra_eli/(?P<pk>\d+)/$',login_required(views.DudRAEli.as_view()),name='dud_ra_eli'),
	re_path(r'^dud_ra_edi/(?P<pk>\d+)/$',login_required(views.DudRAEdi.as_view()),name='dud_ra_edi'),

	# --------------D U D   F A S  -------- #
	re_path(r'^dud_fl_cre/$',login_required(views.DudFLCre.as_view()),name='dud_fl_cre'),
	re_path(r'^dud_fl_lis/$',login_required(views.DudFLLis.as_view()),name='dud_fl_lis'),
	re_path(r'^dud_fl_eli/(?P<pk>\d+)/$',login_required(views.DudFLEli.as_view()),name='dud_fl_eli'),
	re_path(r'^dud_fl_edi/(?P<pk>\d+)/$',login_required(views.DudFLEdi.as_view()),name='dud_fl_edi'),

	# -------------- P R I O R I D A D  -------- #
	re_path(r'^prio_cre/$',login_required(views.PrioCre.as_view()),name='prio_cre'),
	re_path(r'^prio_lis/$',login_required(views.PrioLis.as_view()),name='prio_lis'),
	re_path(r'^prio_eli/(?P<pk>\d+)/$',login_required(views.PrioEli.as_view()),name='prio_eli'),
	re_path(r'^prio_edi/(?P<pk>\d+)/$',login_required(views.PrioEdi.as_view()),name='prio_edi'),

	# --------------  M Ó D U L O S   S A P    -------- #
	re_path(r'^modu_cre/$',login_required(views.ModuCre.as_view()),name='modu_cre'),
	re_path(r'^modu_lis/$',login_required(views.ModuLis.as_view()),name='modu_lis'),
	re_path(r'^modu_eli/(?P<pk>\d+)/$',login_required(views.ModuEli.as_view()),name='modu_eli'),
	re_path(r'^modu_edi/(?P<pk>\d+)/$',login_required(views.ModuEdi.as_view()),name='modu_edi'),

	# --------------  R E Q   C R I T I C D A D    -------- #
	re_path(r'^req_cri_cre/$',login_required(views.ReqCriCre.as_view()),name='req_cri_cre'),
	re_path(r'^req_cri_lis/$',login_required(views.ReqCriLis.as_view()),name='req_cri_lis'),
	re_path(r'^req_cri_eli/(?P<pk>\d+)/$',login_required(views.ReqCriEli.as_view()),name='req_cri_eli'),
	re_path(r'^req_cri_edi/(?P<pk>\d+)/$',login_required(views.ReqCriEdi.as_view()),name='req_cri_edi'),

	# -------------- I N P U T   F I N A L   P E T    -------- #
	re_path(r'^pet_inpf_cre/$',login_required(views.PetInpFCre.as_view()),name='pet_inpf_cre'),
	re_path(r'^pet_inpf_lis/$',login_required(views.PetInpFLis.as_view()),name='pet_inpf_lis'),
	re_path(r'^pet_inpf_eli/(?P<pk>\d+)/$',login_required(views.PetInpFEli.as_view()),name='pet_inpf_eli'),
	re_path(r'^pet_inpf_edi/(?P<pk>\d+)/$',login_required(views.PetInpFEdi.as_view()),name='pet_inpf_edi'),

	# -------------- I N P U T   F I N A L   P E T    -------- #
	re_path(r'^req_cal_cre/$',login_required(views.ReqCalInputCre.as_view()),name='req_cal_cre'),
	re_path(r'^req_cal_lis/$',login_required(views.ReqCalInputLis.as_view()),name='req_cal_lis'),
	re_path(r'^req_cal_eli/(?P<pk>\d+)/$',login_required(views.ReqCalInputEli.as_view()),name='req_cal_eli'),
	re_path(r'^req_cal_edi/(?P<pk>\d+)/$',login_required(views.ReqCalInputEdi.as_view()),name='req_cal_edi'),

	# -------------- I N P U T   F I N A L   R E Q    -------- #
	re_path(r'^req_inpf_cre/$',login_required(views.ReqInpFCre.as_view()),name='req_inpf_cre'),
	re_path(r'^req_inpf_lis/$',login_required(views.ReqInpFLis.as_view()),name='req_inpf_lis'),
	re_path(r'^req_inpf_eli/(?P<pk>\d+)/$',login_required(views.ReqInpFEli.as_view()),name='req_inpf_eli'),
	re_path(r'^req_inpf_edi/(?P<pk>\d+)/$',login_required(views.ReqInpFEdi.as_view()),name='req_inpf_edi'),






	# --------------D U D A S  --------


	# ------------- D E T  A U T H   C L I E N T E  --------
	re_path(r'^au_c_cre/$',login_required(views.AuthCCre.as_view()),name='au_c_cre'),
	re_path(r'^au_c_lis/$',login_required(views.AuthCLis.as_view()),name='au_c_lis'),
	re_path(r'^au_c_eli/(?P<pk>\d+)/$',login_required(views.AuthCEli.as_view()),name='au_c_eli'),
	re_path(r'^au_c_edi/(?P<pk>\d+)/$',login_required(views.AuthCEdi.as_view()),name='au_c_edi'),


	# ------------ P E E R   R E V I E W -----


	# ------------ O T R O S -----
	re_path(r'^act/$',login_required(views.Actualizaciones),name='act'),


	# ----------------  H A R D C O D E  ----------------- # 
	re_path(r'^hrd_svd/$',login_required(views.HrdSvd.as_view()),name='hrd_svd'),
	re_path(r'^hrd_rmv/$',login_required(views.HrdRmv.as_view()),name='hrd_rmv'),
	re_path(r'^hrd_lst/$',login_required(views.HrdLst.as_view()),name='hrd_lst'),


	# --------------------- L O G  ----------------------- # 
	re_path(r'^log_mdf/$',login_required(views.LogLis.as_view()),name='log_mdf'),

]


"""
	# ----------------  G R A F I C O S   -----------------
	re_path(r'^rep001$',login_required(views.Graficos.as_view()),name='rep001'),
	re_path(r'^rep002$',login_required(views.Rep002.as_view()),name='rep002'),
	re_path(r'^rep003$',login_required(views.Rep003.as_view()),name='rep003'),
	re_path(r'^rep004$',login_required(views.Rep004.as_view()),name='rep004'),   # Acotamiento de error en incurrido

	
	# ----------------  E S T A T U S  -----------------
	re_path(r'^est_cre/$',login_required(views.EstCrear.as_view()),name='est_cre'),
	
 	# ----------------  P E T C I Ó N -----------------
 	re_path(r'^pet_crear/$',login_required(views.PetCrear.as_view()),name='pet_crear'),
 	re_path(r'^pet_eliminar/(?P<pk>\d+)/$',login_required(views.PetEliminar.as_view()),name='pet_eliminar'),
 	re_path(r'^pet_listar/$',login_required(views.PetListar.as_view()),name='pet_listar'),
 	re_path(r'^pet_editar/(?P<pk>\d+)/$',login_required(views.PetEditar.as_view()),name='pet_editar'),
         

	# ----------------  R E Q U E R I M E N T O -----------------
	re_path(r'^req_crear/$',login_required(views.ReqCrear.as_view()),name='req_crear'),
	re_path(r'^req_eliminar/(?P<pk>\d+)/$',login_required(views.ReqEliminar.as_view()),name='req_eliminar'),
	re_path(r'^req_listar/$',login_required(views.ReqListar.as_view()),name='req_listar'),
	re_path(r'^req_agr_comn/$',login_required(views.ReqAgrComn.as_view()),name='req_agr_comn'),
	re_path(r'^req_editar/(?P<pk>\d+)/$',login_required(views.ReqEditar.as_view()),name='req_editar'),
	re_path(r'^req_x_pet/$',login_required(views.ReqPorPet.as_view()),name='req_x_pet'),

	re_path(r'^req_crear1/(?P<pk>\d+)/$',login_required(views.ReqCrearRef.as_view()),name='req_crear1'),
	re_path(r'^req_bita/(?P<pk>\d+)/$',login_required(views.ReqBita.as_view()),name='req_bita'),



	# --------------I N C I D E N C I A  --------
	re_path(r'^inc_cre/(?P<pk>\d+)/$',login_required(views.IncCre.as_view()),name='inc_cre'),
	re_path(r'^inc_lis/$',login_required(views.IncLis.as_view()),name='inc_lis'),
	re_path(r'^inc_eli/(?P<pk>\d+)/$',login_required(views.IncEli.as_view()),name='inc_eli'),
	re_path(r'^inc_edi/(?P<pk>\d+)/$',login_required(views.IncEdi.as_view()),name='inc_edi'),
	re_path(r'^inc_exp/$',login_required(views.IncExp.as_view()),name='inc_exp'),
	re_path(r'^inc_xreq/$',login_required(views.IncXReq.as_view()),name='inc_xreq'),
	re_path(r'^inc_xpet/$',login_required(views.IncXPet.as_view()),name='inc_xpet'),

	
	# --------------R I E S G O   --------
	re_path(r'^rie_cre/(?P<pk>\d+)/$',login_required(views.RieCre.as_view()),name='rie_cre'),
	re_path(r'^rie_lis/$',login_required(views.RieLis.as_view()),name='rie_lis'),
	re_path(r'^rie_eli/(?P<pk>\d+)/$',login_required(views.RieEli.as_view()),name='rie_eli'),
	re_path(r'^rie_edi/(?P<pk>\d+)/$',login_required(views.RieEdi.as_view()),name='rie_edi'),
	re_path(r'^rie_xreq/$',login_required(views.RieXReq.as_view()),name='rie_xreq'),
	re_path(r'^rie_xpet/$',login_required(views.RieXPet.as_view()),name='rie_xpet'),


	# ----------------  T A S K  -----------------
	re_path(r'^task_crear/$',login_required(views.TaskCrear.as_view()),name='task_crear'),
	re_path(r'^task_crear1/(?P<pk>\d+)/$',login_required(views.TaskCrearRef.as_view()),name='task_crear1'),
	re_path(r'^task_eliminar/(?P<pk>\d+)/$',login_required(views.TaskEliminar.as_view()),name='task_eliminar'),

	re_path(r'^task_listar/$',login_required(views.TaskListar.as_view()),name='task_listar'),
	re_path(r'^task_sf/$',login_required(views.SubidaAFenix.as_view()),name='task_sf'),
	re_path(r'^task_x_codigo/$',login_required(views.TaskPorCodigo.as_view()),name='task_x_codigo'),
	re_path(r'^task_x_req/$',login_required(views.TaskPorReq.as_view()),name='task_x_req'),
	re_path(r'^act_task/$',login_required(views.ActTask.as_view()),name='act_task'),
	re_path(r'^task_acc/$',login_required(views.TaskACC.as_view()),name='task_acc'),
	re_path(r'^task_editar/(?P<pk>\d+)/$',login_required(views.TaskEditar.as_view()),name='task_editar'),

	re_path(r'^task_x_pet/$',login_required(views.TaskXPet.as_view()),name='task_x_pet'),
	

	# ----------------  G A N T  -----------------
	re_path(r'^gant/$',login_required(views.GantIni),name='gant'),
	re_path(r'^gnt_c1/$',login_required(views.Gnt_c1.as_view()),name='gnt_c1'),
	re_path(r'^gnt_vd1/$',login_required(views.Gnt_vd1.as_view()),name='gnt_vd1'),
	re_path(r'^gnt_d1/$',login_required(views.Gnt_d1.as_view()),name='gnt_d1'),
	re_path(r'^gnt_lst/$',login_required(views.GntLst.as_view()),name='gnt_lst'),
	re_path(r'^gnt_asg/$',login_required(views.ObtAsignaciones.as_view()),name='gnt_asg'),
	re_path(r'^gnt_d2/$',login_required(views.Gnt_d2.as_view()),name='gnt_d2'), # Datalle del gant



	# ------------ P E E R   R E V I E W -----
	re_path(r'^pr_cre/(?P<pk>\d+)/$',login_required(views.PrCre.as_view()),name='pr_cre'),
	re_path(r'^pr_lis/$',login_required(views.PrLis.as_view()),name='pr_lis'),
	re_path(r'^pr_edi/(?P<pk>\d+)/$',login_required(views.PrEdi.as_view()),name='pr_edi'),
	re_path(r'^pr_eli/(?P<pk>\d+)/$',login_required(views.PrEli.as_view()),name='pr_eli'),



	# --------------D U D A S  --------
	re_path(r'^dud_cre1/(?P<pk>\d+)/$',login_required(views.DudCreRef.as_view()),name='dud_cre1'),
	re_path(r'^dud_lis/$',login_required(views.DudLis.as_view()),name='dud_lis'),
	re_path(r'^dud_eli/(?P<pk>\d+)/$',login_required(views.DudEli.as_view()),name='dud_eli'),
	re_path(r'^dud_edi/(?P<pk>\d+)/$',login_required(views.DudEdi.as_view()),name='dud_edi'),
	re_path(r'^dud_exp/$',login_required(views.DudExp.as_view()),name='dud_exp'),
	re_path(r'^dud_xreq/$',login_required(views.DudXReq.as_view()),name='dud_xreq'),
	re_path(r'^dud_xpet/$',login_required(views.DudXPet.as_view()),name='dud_xpet'),


"""