from djongo import models
from pygments.formatters.html import HtmlFormatter


class User(models.Model):
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=1000)
    user_name = models.CharField(max_length=1000, unique=True, blank=False)
    password = models.CharField(max_length=1000, blank=False)

    # class Meta:
    #     ordering = ('created',)

    #     abstract = True

    # def save(self, *args, **kwargs):  # new
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code snippet.
    #     """
    # options = {'user_name': self.user_name} if self.user_name else {}
    # formatter = HtmlFormatter(style=self.style, linenos=linenos,
    #                           full=True, **options)
    # self.highlighted = highlight(self.code, lexer, formatter)
    # super(Snippet, self).save(*args, **kwargs)
    #
    def __str__(self):
        return self.first_name + " " + self.last_name
