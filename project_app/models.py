from django.db import models

class Space(models.Model):
    img=models.ImageField(upload_to='images/')    #save image as blob
    email = models.EmailField('email address')
    capacity = models.CharField(max_length=1000)
    address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True)
    comments= models.CharField(max_length=1000)
