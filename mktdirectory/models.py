from django.db import models
import uuid

# Create your models here.


# ltr
# Kg
# bag
# module
# Cup
# heap(tubbers)
# load
# basket


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        db_table = "sql_category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Commodity(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(
        verbose_name="Brief description of the commodity"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sql_commodity"
        verbose_name_plural = "Commodities"

    def __str__(self) -> str:
        return self.name


class Market(models.Model):
    market_code = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(max_length=50)
    brief_details = models.TextField()
    num_vendors = models.SmallIntegerField()
    market_schedule = models.CharField(max_length=50)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    location_description = models.TextField(verbose_name="Market site")
    slug = models.SlugField(max_length=200)
    referene_mkt_date = models.DateField(
        verbose_name=("Most recent market date")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sql_market"

    def __str__(self):
        return self.name


class MarketInstance(models.Model):

    GRADES = (
        ("O", "Old"),
        ("N", "New"),
    )
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.DO_NOTHING)
    grade = models.CharField(
        max_length=1, choices=GRADES, null=True, blank=True
    )
    commodity_price = models.DecimalField(
        verbose_name=("Price per bag at market date"),
        help_text="Price per bag",
        max_digits=6,
        decimal_places=2,
    )
    market_date = models.DateField(verbose_name="Market day")

    class Meta:
        db_table = "sql_market_instance"


class PaymentMethod(models.Model):
    name = models.CharField(
        verbose_name="Accepted Payments",
        max_length=50,
    )

    class Meta:
        db_table = "sql_payment_method"
        verbose_name_plural = "Payment Methods"

    def __str__(self) -> str:
        return self.name


class MarketAcceptedPayment(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    charges = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Payment charges"
    )

    class Meta:
        db_table = "sql_accepted_payment"
        verbose_name_plural = "Market Accepted Payments"
