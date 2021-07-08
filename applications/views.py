from django.shortcuts import render


def my_applications(request):
    context = {}
    return render(request, 'applications/my_applications.html', context)