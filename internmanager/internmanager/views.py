from django.http import HttpResponse


def Home(request):
    return HttpResponse("HELLO,word.welcome in Django contact page")