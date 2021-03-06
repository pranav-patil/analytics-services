from django.db import models


class BlogPost(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=True, blank=True, default='')
    content = models.TextField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField("Timestamp", auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.user

    objects = models.Manager()
