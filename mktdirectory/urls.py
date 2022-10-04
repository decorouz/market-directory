from django.urls import path

from mktdirectory import views

urlpatterns = [
    path("commodities/", views.commodity_list),
    path("commodities/<int:pk>/", views.commodity_detail),
    path("markets/", views.market_list),
    path("markets/<int:pk>/", views.market_detail),
    path("categories/", views.category_list),
    path("categories/<int:pk>/", views.category_detail),
]
