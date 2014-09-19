from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from trafficUser.forms import RegistrationForm
from django.contrib.auth.models import User
from trafficUser.models import TrafficUser

# Create your views here.
def TrafficUserRegistration(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
			user.save()
			# traffic_user = user.get_profile()
			# traffic_user.name = form.cleaned_data['name']
			# traffic_user = form.cleaned_data['birthday']
			# traffic_user.save()
			traffic_user = TrafficUser(user=user, name=form.cleaned_data['name'], birthday=form.cleaned_data['birthday'])
			traffic_user.save()
			return HttpResponseRedirect('/profile/' + form.cleaned_data['username'])
		else:
			return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
	else:
		'''user is not submitting the form. Show them blank registration form.'''
		form = RegistrationForm()
		context = {'form': form}
		return render_to_response('register.html', context, context_instance=RequestContext(request))

def Profile(request, username=None):
	try:
		user = User.objects.get(username=username)
	except:
		return render_to_response('profile.html', {}, context_instance=RequestContext(request))
	traffic_user = TrafficUser.objects.filter(user=user)
	traffic_user_obj = traffic_user.values()[0]
	context = {}
	context['user_name'] = traffic_user_obj.get('name')
	context['user_birthday'] = traffic_user_obj.get('birthday')
	context['user_username'] = user.username
	context['user_email'] = user.email
	return render_to_response('profile.html', context, context_instance=RequestContext(request))