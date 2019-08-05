from django.db import models

from user.models import User, MarketRate, MarketComment, RoleMarket


class Market(models.Model):
    market_name = models.CharField(max_length=125, blank=False)
    description = models.CharField(max_length=5000, blank=True, default="")
    address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to="market_image/", blank=True, default="default_market_image.png")
    register_data = models.DateTimeField(auto_now_add=True)
    last_edit_data = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    rules = models.ManyToManyField(RoleMarket, blank=True)
    rates = models.ManyToManyField(MarketRate, blank=True)
    rates_result = models.PositiveIntegerField(default=0)
    rates_count = models.PositiveIntegerField(default=0)
    comments = models.ManyToManyField(MarketComment, blank=True)
    comments_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.market_name
