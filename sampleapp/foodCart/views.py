from django.http import HttpResponse
from django.template import Context, loader


def foodCart(request):
	t = loader.get_template('food_cart.html')
	return HttpResponse(t.render(Context({})))