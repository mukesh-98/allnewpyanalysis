from django.shortcuts import render


# Create your views here.
vali={}
def selector(request):
    return render(request,'selector.html')
