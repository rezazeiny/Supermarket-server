from django.db import models

from market.models import Market

from market_models.models import Model
import sys


class MarketRate(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    star = models.PositiveSmallIntegerField(default=0)


class ModelRate(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    star = models.PositiveSmallIntegerField(default=0)


class User(models.Model):
    email = models.EmailField(max_length=125, unique=True, blank=True)
    user_name = models.CharField(max_length=125, unique=True, blank=False)
    password = models.CharField(max_length=125, blank=False)
    first_name = models.CharField(max_length=125, blank=True)
    last_name = models.CharField(max_length=125, blank=True)
    email_validation = models.BooleanField(default=False)
    email_random = models.CharField(max_length=6, blank=True)
    forgot_password_random = models.CharField(max_length=6, blank=True)
    image = models.ImageField(upload_to="user_image/", blank=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True)
    phone_validation = models.BooleanField(default=False)
    phone_random = models.CharField(max_length=6, blank=True)
    register_data = models.DateTimeField(auto_now_add=True)
    last_edit_data = models.DateTimeField(auto_now=True)
    api = models.CharField(max_length=65, blank=True)
    api_expire_data = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    market_list = models.ManyToManyField(Market, blank=True)

    market_rate_list = models.ManyToManyField(MarketRate, blank=True)
    model_rate_list = models.ManyToManyField(ModelRate, blank=True)

    def __str__(self):
        return self.user_name

    # def save(self, *args, **kwargs):
    #     print("################################salam######################", file=sys.stderr)
    #     super(User, self).save(*args, **kwargs)
