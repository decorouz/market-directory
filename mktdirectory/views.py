from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.filters import SearchFilter
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from .pagination import DefaultPagination
from .filters import MarketFilter


from .models import Category, Commodity, Market, Review
from .serializers import (
    CommoditySerializer,
    MarketSerializer,
    CategorySerializer,
    ReviewSerializer,
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        commodities_count=Count("commodity")
    ).all()

    serializer_class = CategorySerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if Commodity.objects.filter(category_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Category can not be deleted because it is associated with one or more Commodity"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CommodityViewSet(ModelViewSet):
    queryset = Commodity.objects.all()

    serializer_class = CommoditySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category_id", "grade"]

    # filter by category
    # def get_queryset(self):
    #     queryset = Commodity.objects.all()
    #     print(self.request)
    #     category_id = self.request.query_params.get("category_id")
    #     print(category_id)
    #     if category_id is not None:
    #         queryset = queryset.filter(category_id=category_id)
    #     return queryset


class MarketViewSet(ModelViewSet):

    queryset = Market.objects.prefetch_related(
        "accepted_payment_types", "contact_person"
    )

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MarketFilter
    search_fields = ["accepted_payment_types__type"]
    serializer_class = MarketSerializer
    pagination_class = DefaultPagination


class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(market_id=self.kwargs["market_pk"])

    # Goto Serializer create method
    def get_serializer_context(self):
        return {"market_id": self.kwargs["market_pk"]}
