from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Market
from .serializers import MarketDirectorySerializer

# Create your views here.

class MarketListView(ListCreateAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketDirectorySerializer

class MarketDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Market.objects.all() 
    serializer_class = MarketDirectorySerializer


