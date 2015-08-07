from django.shortcuts import render

def index(request):
    # View code here...
    return render(request, 'app/index.html', {},
        content_type="application/xhtml+xml")