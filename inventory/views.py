from django.shortcuts import render

# Create your views here.
def invent(request):
    context = {}
    return render(request, 'inventory/invent.html', context)