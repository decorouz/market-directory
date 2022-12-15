from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Address(TimeStampedModel):
    """Adress model to be used across the project"""

    address = models.CharField(verbose_name="address", max_length=100, null=True)
    town = models.CharField(verbose_name="town", max_length=100, null=True)
    local_govt = models.CharField(
        verbose_name="local government area", max_length=100, null=True
    )
    post_code = models.CharField(verbose_name="post code", max_length=8, null=True)
    country = models.CharField(verbose_name="country", max_length=100, null=True)
    longitude = models.CharField(verbose_name="address", max_length=50, null=True)
    latitude = models.CharField(verbose_name="address", max_length=50, null=True)

    class Meta:
        abstract = True
