from django.shortcuts import render

# Create your views here.
def shiju(request):
    return render(request, 'shiju/index.html',{})