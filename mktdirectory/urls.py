from django.urls import path
from .views import MarketDetailView, MarketListView

urlpatterns = [
    path("", MarketListView.as_view()),
    path("<str:pk>/", MarketDetailView.as_view()),
]
