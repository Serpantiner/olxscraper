from django.db import models
from PIL import Image
# Create your models here.

class Search(models.Model):
    search= models.CharField(max_length=300) #one of the fields called search
    created= models.DateTimeField(auto_now=True) #timestamping

    def __str__(self):  #we return out search as a string
        return '{}'.format(self.search)
    class Meta:
        verbose_name_plural = 'Searches'



