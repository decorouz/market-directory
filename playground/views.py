from django.http import HttpResponse
from django.shortcuts import render
from mktdirectory.models import Commodity

# Create your views here.
def say_hello(request):
    query_set = Commodity.objects.all()

    for product in query_set:
        print(product.category_id)
    return render(request, "hello.html", {"name": "james"})
