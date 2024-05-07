from django import forms

from apps.gestion.models import PeerReview



class PeerReviewForm(forms.ModelForm):
	class Meta:
		model = PeerReview
		fields = [ 'idperer', 'codigo', 'requerimiento' , 'revisor' , 'resultado' , 'version' , 'nota', 'fecha' ]

		widgets={ 'nota':forms.Textarea(attrs={'rows':'4','cols':'70'}),
				  'codigo':forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),
				  'version':forms.TextInput(attrs={'readonly':'readonly'}) ,
				  'revisor':forms.Select(attrs={'class':'form-control','readonly':'readonly'}),
				  'requerimiento':forms.Select(attrs={'class':'form-control','readonly':'readonly'}),
				  'fecha':forms.TextInput(attrs={'readonly':'readonly'}),
				  }

class PeerReviewEdiForm(forms.ModelForm):
	class Meta:
		model = PeerReview
		fields = [ 'idperer', 'codigo', 'requerimiento' , 'revisor' , 'resultado' , 'version' , 'nota', 'fecha' ]

		widgets={ 
			'nota':forms.Textarea(attrs={'rows':'4','cols':'70'}),
			'codigo':forms.TextInput(attrs={'class':'form-control'}) ,
			'revisor':forms.Select(attrs={'class':'form-control'}),
			'fecha':forms.TextInput(attrs={'type':'date','readonly':'readonly'}),
		}