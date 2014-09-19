from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from trafficUser.models import TrafficUser


class RegistrationForm(ModelForm):
	username 		= forms.CharField(label=(u'Username'))
	email			= forms.EmailField(label=(u'Email Address'))
	password 		= forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
	confirm_password = forms.CharField(label=(u'Confirm Password'),
									   widget=forms.PasswordInput(render_value=False))

	class Meta:
		model = TrafficUser
		exclude = ('user',)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Username is already taken')

	def clean(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']

		if password != confirm_password:
			raise Forms.ValidationError('Passwords did not match.')
		return self.cleaned_data