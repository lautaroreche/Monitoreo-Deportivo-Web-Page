from django.shortcuts import render


def home(requests):
    context = {}
    return render(requests, 'index.html', context)
