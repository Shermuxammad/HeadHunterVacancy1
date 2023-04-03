from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class MenuItem(MPTTModel):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']
