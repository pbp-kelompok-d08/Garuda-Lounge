from django.shortcuts import render

def show_merch(request):
    return render(request, 'merchandise.html')
# Create your views here.
