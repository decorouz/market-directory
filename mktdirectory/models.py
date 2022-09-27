from django.db import models
import uuid


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        db_table = "sql_category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Commodity(models.Model):

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    overview = models.TextField(
        verbose_name="Brief description of the commodity"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sql_commodity"
        verbose_name_plural = "Commodities"

    def __str__(self) -> str:
        return self.name


class ContactPerson(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)

    class Meta:
        db_table = "sql_contact_person"

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} "


class AcceptedPaymentMethod(models.Model):
    PAYMENT_METHOD_CASH = "CAS"
    PAYMENT_METHOD_POS = "POS"
    PAYMENT_METHOD_TRANSFER = "TF"
    PAYMENT_METHOD_OTHERS = "O"

    PAYMENT_METHODS = [
        (PAYMENT_METHOD_CASH, "Cash Payment"),
        (PAYMENT_METHOD_POS, "POS"),
        (PAYMENT_METHOD_TRANSFER, "Bank Transfer"),
        (PAYMENT_METHOD_OTHERS, "Others"),
    ]

    name = models.CharField(
        verbose_name="Accepted Payments",
        max_length=3,
        choices=PAYMENT_METHODS,
        default=PAYMENT_METHOD_CASH,
    )
    description = models.TextField()
    charges = models.FloatField(default=0.0)

    class Meta:
        db_table = "sql_payment_method"
        verbose_name_plural = "Payment Methods"

    def __str__(self) -> str:
        return self.name


class Market(models.Model):
    market_code = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    accepted_payment_types = models.ManyToManyField(AcceptedPaymentMethod)
    contact_person = models.ForeignKey(
        ContactPerson, on_delete=models.SET_NULL, null=True, blank=True
    )
    brief_details = models.TextField()
    num_vendors = models.SmallIntegerField()
    market_days_interval = models.SmallIntegerField(default=5)

    location_description = models.TextField(verbose_name="Market site")
    slug = models.SlugField()
    reference_mkt_date = models.DateField(
        verbose_name=("Most recent market date")
    )
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sql_market"

    def __str__(self):
        return self.name


class MarketDay(models.Model):
    OLD_PRODUCE = "O"
    NEW_PRODUCE = "N"

    PRODUCE_CHOICES = [
        (OLD_PRODUCE, "New"),
        (NEW_PRODUCE, "Old"),
    ]

    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
    )
    commodity = models.ForeignKey(
        Commodity,
        on_delete=models.CASCADE,
    )
    grade = models.CharField(
        max_length=1, choices=PRODUCE_CHOICES, default=NEW_PRODUCE
    )
    commodity_price = models.DecimalField(
        verbose_name=("Price per bag at market date"),
        help_text="Price per bag",
        max_digits=8,
        decimal_places=2,
    )
    market_date = models.DateField(verbose_name="Market day")

    class Meta:
        db_table = "sql_market_date"


# class MarketAcceptedPayment(models.Model):
#     market = models.ForeignKey(Market, on_delete=models.CASCADE)
#     payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
#     charges = models.DecimalField(
#         max_digits=5, decimal_places=2, verbose_name="Payment charges"
#     )

#     class Meta:
#         db_table = "sql_accepted_payment"
#         verbose_name_plural = "Market Accepted Payments"
