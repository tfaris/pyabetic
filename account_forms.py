from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
	email = forms.EmailField(label='Email address', max_length=75)
	
	class Meta:
		model = User
		fields = ('username', 'email',) 	
		
	def clean_email(self):
		email = self.cleaned_data["email"]
		
		try:
			User.objects.get(email__iexact=email)
		except User.DoesNotExist:
			return email
		
		raise forms.ValidationError("A user with that email address already exists.")
	
	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.email = self.cleaned_data["email"]
		user.is_active = True
		if commit:
			user.save()
			
		return user