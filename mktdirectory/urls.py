from django.urls import path

from mktdirectory import views

urlpatterns = [
    path("commodities/", views.CommodityList.as_view()),
    path("commodities/<int:pk>/", views.CommodityDetail.as_view()),
    path("markets/", views.MarketList.as_view()),
    path("markets/<int:pk>/", views.MarketDetail.as_view()),
    path("categories/", views.CategoryList.as_view()),
    path("categories/<int:pk>/", views.CategoryDetail.as_view()),
]
