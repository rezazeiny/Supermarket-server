from django.db import models


class Market(models.Model):
    name = models.CharField(max_length=125, blank=False)
    address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to="market_image/", blank=True)

    def __str__(self):
        return self.name
