from django.urls import path

from mktdirectory import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("categories", views.CategoryViewSet)
router.register("commodities", views.CommodityViewSet)
router.register("markets", views.MarketViewSet)


urlpatterns = router.urls
