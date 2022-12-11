from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        db_table = "sql_category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class ContactPerson(models.Model):
    # social media
    # role: Choices
    # is verified: Y/N. id, bvn
    # document
    # image
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "sql_market_extension_officer"

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
        max_length=4,
        choices=PAYMENT_METHODS,
        default=PAYMENT_METHOD_CASH,
    )

    description = models.TextField()
    charges = models.FloatField(default=0.0)

    class Meta:
        db_table = "sql_payment_method"
        verbose_name_plural = "payment methods"

    def __str__(self) -> str:
        return self.type


class Commodity(models.Model):
    # product_name
    # measure : choices, bag, mo
    # local name
    # brief description
    # product grades
    # recent recorded price
    OLD_PRODUCE = "Old"
    NEW_PRODUCE = "New"
    NONE = ""

    PRODUCE_CHOICES = [
        (NONE, ""),
        (NEW_PRODUCE, "New"),
        (OLD_PRODUCE, "Old"),
    ]
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    local_name = models.CharField(max_length=50, blank=True, null=True)
    grade = models.CharField(max_length=3, choices=PRODUCE_CHOICES, default=NONE, blank=True)
    overview = models.TextField(null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name", "grade"], name="unique_commodity")]
        db_table = "sql_commodity"
        verbose_name_plural = "commodities"

    def __str__(self) -> str:
        return f"{self.grade} {self.name}"


# Contributors
# name, email, phone, role


class Market(models.Model):
    # Open Season: All year or seasonal
    # operation days(market days/schedule)
    # sales channels
    # images
    # map
    # market site? limited choices
    # indoor or outdoor or partially
    # next market day and date
    # avialable products (m2m*)
    # number of vendors
    # accepted payment methods? limited choices
    # contributors: foreign key
    # local taxes/levies
    # Government programs related to markets: choices
    market_code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=500, editable=False, null=True)
    # location address
    # status
    accepted_payment_types = models.ManyToManyField(
        AcceptedPaymentMethod, verbose_name="list of payment methods"
    )
    commodities = models.ManyToManyField(
        Commodity,
        through="MarketInstance",
        verbose_name="list of commodities",
    )
    contact_person = models.ForeignKey(
        ContactPerson, on_delete=models.SET_NULL, null=True, blank=True
    )

    brief_detail = models.TextField()
    num_vendor = models.SmallIntegerField()
    market_days_interval = models.SmallIntegerField(default=5)
    location_description = models.TextField(verbose_name="Market site")
    reference_mkt_date = models.DateField(verbose_name=("confirmed market date"))
    is_approved = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sql_market"
        ordering = ["market_code"]

    def __str__(self):
        return self.name


# the date the commodity was sold at that price


# Commodity Price Monitor Class
class MarketInstance(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.RESTRICT)
    commodity_price = models.DecimalField(
        verbose_name=("price per bag"), help_text="Price per bag", max_digits=8, decimal_places=2
    )
    market_date = models.DateField()

    class Meta:
        db_table = "sql_market_instance"
        verbose_name = "market instance"
        constraints = [
            models.UniqueConstraint(
                fields=["commodity", "market", "market_date"],
                name="unique_item",
            )
        ]

    # get the market dates only

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
