from django.shortcuts import render

# Create your views here.


def Home(request):
    if request.method == "GET":
        return render(request, "home.html")
