from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        db_table = "sql_category"
        verbose_name_plural = "Categories"

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
        return f"{self.first_name} {self.last_name} "


class AcceptedPaymentMethod(models.Model):

    PAYMENT_METHOD_CASH = "CASH"
    PAYMENT_METHOD_POS = "POS"
    PAYMENT_METHOD_TRANSFER = "TF"
    PAYMENT_METHOD_OTHERS = "O"

    PAYMENT_METHODS = [
        (PAYMENT_METHOD_CASH, "Cash Payment"),
        (PAYMENT_METHOD_POS, "POS"),
        (PAYMENT_METHOD_TRANSFER, "Bank Transfer"),
        (PAYMENT_METHOD_OTHERS, "Others"),
    ]
    type = models.CharField(
        verbose_name="Accepted Payments",
        max_length=4,
        choices=PAYMENT_METHODS,
        default=PAYMENT_METHOD_CASH,
    )

    description = models.TextField()
    charges = models.FloatField(default=0.0)

    class Meta:
        db_table = "sql_payment_method"
        verbose_name_plural = "Payment Methods"

    def __str__(self) -> str:
        return self.type


class Commodity(models.Model):

    OLD_PRODUCE = "Old"
    NEW_PRODUCE = "New"
    NONE = ""

    PRODUCE_CHOICES = [
        (NONE, "---"),
        (NEW_PRODUCE, "New"),
        (OLD_PRODUCE, "Old"),
    ]
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    grade = models.CharField(
        max_length=3,
        choices=PRODUCE_CHOICES,
        default=NONE,
    )
    overview = models.TextField(
        verbose_name="Commodity Description", null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "grade"], name="unique_commodity"
            )
        ]
        db_table = "sql_commodity"
        verbose_name_plural = "Commodities"

    def __str__(self) -> str:
        return f"{self.grade} {self.name}"


class Market(models.Model):
    market_code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    accepted_payment_types = models.ManyToManyField(AcceptedPaymentMethod)
    contact_person = models.ForeignKey(
        ContactPerson, on_delete=models.SET_NULL, null=True, blank=True
    )
    commodities = models.ManyToManyField(Commodity, through="MarketDay")
    brief_detail = models.TextField()
    num_vendor = models.SmallIntegerField()
    market_days_interval = models.SmallIntegerField(default=5)

    location_description = models.TextField(verbose_name="Market site")
    reference_mkt_date = models.DateField(
        verbose_name=("confirmed market date")
    )
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sql_market"
        ordering = ["market_code"]

    def __str__(self):
        return self.name


class MarketDay(models.Model):

    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
    )
    commodity = models.ForeignKey(
        Commodity,
        on_delete=models.RESTRICT,
    )

    commodity_price = models.DecimalField(
        verbose_name=("Price per bag"),
        help_text="Price per bag",
        max_digits=8,
        decimal_places=2,
    )
    market_date = models.DateField(verbose_name="Market date")

    class Meta:
        db_table = "sql_market_date"
        verbose_name = "Market Date"
        constraints = [
            models.UniqueConstraint(
                fields=["commodity", "market_date"], name="unique_item"
            )
        ]

    def __str__(self) -> str:
        return self.market.name


class Review(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
 
    class Meta:
        db_table = "sql_market_review"

    def __str__(self):
        return self.name
