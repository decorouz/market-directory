from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from tag.models import TaggedItem
from mktdirectory.models import Category, Commodity

# Create your views here.
def say_hello(request):

    return render(
        request,
        "hello.html",
        {"name": "james"},
    )
