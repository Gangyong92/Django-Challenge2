from django.db import models
from . import managers


class CoreModel(models.Model):

    """ Core Model """

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True