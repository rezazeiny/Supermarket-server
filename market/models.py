from djongo import models


class Market(models.Model):
    name = models.CharField(max_length=1000, unique=True, blank=False)
    address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=20)
    owner = models.CharField(max_length=1000, blank=False)
    # image = models.ImageField()
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
        return self.name + " " + self.owner
