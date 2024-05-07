from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.gestion.models import PeerReview, Requerimientos, AuthUser, AuthCliente
from apps.peer.forms import *




"""  =================================  P E E R   R E V I E W  --------------------- """

#		Crear PeerRevies
class PrCre(CreateView):
	model=PeerReview
	form_class=PeerReviewForm
	template_name='peer/cre.html'
	success_url=reverse_lazy('req_listar')

	def get_form(self, form_class=None):
		# Get User and Req
		req1 = Requerimientos.objects.get(idrequerimiento=self.kwargs['pk'])
		req2 = Requerimientos.objects.filter(idrequerimiento=self.kwargs['pk'])
		usr1 = AuthUser.objects.get(pk=self.request.user.pk)
		
		# Build codex
		coun_reqs = PeerReview.objects.filter(requerimiento=self.kwargs['pk']).count()
		cod1 = "PeerReview_"+str(req1.codigo)+"_v"+str(coun_reqs+1)

		form=super(CreateView,self).get_form(form_class=self.form_class)
		form.fields["requerimiento"].queryset = req2
		form.fields["requerimiento"].initial = req1
		form.fields["codigo"].initial = cod1
		form.fields["revisor"].initial = usr1
		form.fields["version"].initial = coun_reqs+1
		form.fields["fecha"].initial = '01/04/2021'

		print(" -------------->>>><<<")
		return form





class PrLis(ListView):
	model=PeerReview
	template_name='peer/lis.html'

	def get(self,request,*args,**kwargs):

		idr = self.request.GET.get('idr')
		req_lst = []

		if idr == '0':
			req_lst = PeerReview.objects.all()
		else:
			req_lst = PeerReview.objects.filter(requerimiento=idr)

		#	Build response
		dicc = {  
			'object_list':req_lst,
			'msj': 'PeerReview del requerimiento' 
		}
		return render(request,self.template_name,dicc)





class PrEdi(UpdateView):
	model=PeerReview
	form_class=PeerReviewEdiForm
	template_name='peer/cre.html'
	success_url=reverse_lazy('req_listar')

	def get_form(self, form_class=None):
		# Get User and Req
		per = PeerReview.objects.get(pk=self.kwargs['pk'])
		rqs = Requerimientos.objects.filter(peticion=per.requerimiento.peticion)

		form=super(UpdateView,self).get_form(form_class=self.form_class)
		#form.fields["revisor"].queryset = ahcs.idauth.all()
		form.fields["requerimiento"].queryset = rqs
		return form




class PrEli(DeleteView):
	model=PeerReview
	form_class=PeerReviewForm
	template_name='peer/eli.html'
	success_url=reverse_lazy('req_listar')





