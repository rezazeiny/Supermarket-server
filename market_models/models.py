from django.db import models

from market.models import Market
from user.models import User, ModelRate, ModelComment


class Model(models.Model):
    product_name = models.CharField(max_length=125, blank=False)
    category = models.CharField(max_length=125, blank=False, default="")
    description = models.CharField(max_length=5000, blank=True, default="")
    price = models.IntegerField(blank=False)
    count = models.IntegerField(blank=False)
    register_data = models.DateTimeField(auto_now_add=True)
    last_edit_data = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="product_image/", blank=True, default="default_model_image.png")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    rates = models.ManyToManyField(ModelRate, blank=True)
    rates_result = models.PositiveIntegerField(default=0)
    rates_count = models.PositiveIntegerField(default=0)
    comments = models.ManyToManyField(ModelComment, blank=True)
    comments_count = models.PositiveIntegerField(default=0)

