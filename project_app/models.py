from django.db import models

class Space(models.Model):
    img=models.ImageField(upload_to='images/')    #save image as blob
    email = models.EmailField('email address')
    capacity = models.CharField(max_length=1000)
    address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True)
    comments= models.CharField(max_length=1000)

class hubData(models.Model):
    name    =   models.CharField(max_length=100)
    email   =   models.EmailField('email address') 
    address =   models.CharField(verbose_name="address",max_length=100, null=True, blank=True)   
    city    =   models.CharField(verbose_name="city",max_length=100, null=True, blank=True)
    country =   models.CharField(verbose_name="country",max_length=100, null=True, blank=True) 
    state   =   models.CharField(verbose_name="state",max_length=100, null=True, blank=True)    
    zipcode =   models.CharField(verbose_name="zipcode",max_length=100, null=True, blank=True)  
    wifi    =   models.CharField(verbose_name="wifi",max_length=100, null=True, blank=True)
    water   =   models.CharField(verbose_name="water",max_length=100, null=True, blank=True)
    electricity =models.CharField(verbose_name="electricity",max_length=100, null=True, blank=True)
    washroom =  models.CharField(verbose_name="washroom",max_length=100, null=True, blank=True)  
    capacity =  models.CharField(verbose_name="capacity",max_length=100, null=True, blank=True)   
    description =   models.TextField()
    file    = models.ImageField(upload_to='images/',null=True, blank=True)
    lat     = models.FloatField(blank=True,null=True)
    long    = models.FloatField(blank=True,null=True)
