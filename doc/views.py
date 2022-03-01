from django.shortcuts import render


def doc(request):
    return render(request, 'api-doc.html')


# Create your views here.
