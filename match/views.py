from django.shortcuts import render

# Create your views here.
def show_match(request):
    return render(request, "match.html")

def add_match(request):
    return render(request, "add_match.html")