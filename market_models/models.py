from djongo import models


class Model(models.Model):
    name = models.CharField(max_length=125, blank=False)
    price = models.IntegerField(blank=False)
    count = models.IntegerField(blank=False)
    image = models.FileField()
