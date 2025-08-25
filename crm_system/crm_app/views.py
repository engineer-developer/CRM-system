from django.shortcuts import render


def index_page(request):
    return render(request, "crm_app/index.html")
