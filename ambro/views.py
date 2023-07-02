from django.shortcuts import render


def index(request):
    return render(request, 'ambro/index.html')


def contact(request):
    return render(request, 'ambro/contact.html')


def about(request):
    return render(request, 'ambro/about.html')


def product(request):
    return render(request, 'ambro/product.html')
