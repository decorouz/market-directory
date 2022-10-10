from cgitb import lookup
from django.urls import path

from mktdirectory import views
from rest_framework_nested import routers

# from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter()
router.register("categories", views.CategoryViewSet)
router.register("commodities", views.CommodityViewSet)
router.register("markets", views.MarketViewSet)

markets_router = routers.NestedDefaultRouter(
    router, "markets", lookup="market"
)
markets_router.register(
    "reviews", views.ReviewViewSet, basename="market-reviews"
)


urlpatterns = router.urls + markets_router.urls
