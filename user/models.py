from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=125, blank=True, default="")
    user_name = models.CharField(max_length=125, unique=True, blank=False)
    password = models.CharField(max_length=125, blank=False, null=False)
    first_name = models.CharField(max_length=125, blank=True, default="")
    last_name = models.CharField(max_length=125, blank=True, default="")
    email_validation = models.BooleanField(blank=False, default=False)
    email_random = models.CharField(max_length=6, blank=True, default="")
    forgot_password_random = models.CharField(max_length=6, blank=True, default="")
    image = models.ImageField(upload_to="user_image/", blank=True, default="default_user_image.jpg")
    phone_number = models.CharField(max_length=20, blank=True, default="")
    phone_validation = models.BooleanField(blank=False, default=False)
    phone_random = models.CharField(max_length=6, blank=True, default="")
    register_data = models.DateTimeField(auto_now_add=True)
    last_edit_data = models.DateTimeField(auto_now=True)
    api = models.CharField(max_length=65, blank=True, default="")
    api_expire_data = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user_name


class MarketRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.PositiveSmallIntegerField(default=0)
    register_data = models.DateTimeField(auto_now_add=True)
    last_edit_data = models.DateTimeField(auto_now=True)


class MarketComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=5000, blank=True, default="")
    register_data = models.DateTimeField(auto_now_add=True)
    last_edit_data = models.DateTimeField(auto_now=True)


class ModelRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.PositiveSmallIntegerField(default=0)
    register_data = models.DateTimeField(auto_now_add=True)
    last_edit_data = models.DateTimeField(auto_now=True)


class ModelComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=5000, blank=True, default="")
    register_data = models.DateTimeField(auto_now_add=True)
    last_edit_data = models.DateTimeField(auto_now=True)


class RoleMarket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=125)
    register_data = models.DateTimeField(auto_now_add=True)
    last_edit_data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user_name + ": " + self.role
