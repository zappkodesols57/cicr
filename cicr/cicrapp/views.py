from django.shortcuts import render

def home_view(request):
    """
    Renders the modern Welcome Home Page for CICR.
    """
    return render(request, "home.html")

