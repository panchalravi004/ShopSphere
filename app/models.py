from itertools import product
from math import prod
import os
from uuid import uuid4
from django.db import models
from distutils.command.upload import upload
from django.contrib.auth.models import User
from autoslug import AutoSlugField

class Category(models.Model):
    image = models.ImageField(upload_to="categories",null=True)
    title = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.title
    
class Product(models.Model):

    sts = (
        ("PUBLISH","PUBLISH"),
        ("DRAFT","DRAFT"),
    )
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to="products",null=True,blank=True)
    title = models.CharField(max_length=200,null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True,default=0)
    stock = models.IntegerField(null=True,default=0)
    date = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='title',unique=True,null=True,default=None)
    status = models.CharField(choices=sts,null=True,max_length=200)

    def __str__(self):
        return self.title
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.user.username+" - "+self.product.title


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    street = models.CharField(null=True,max_length=200)
    pin = models.IntegerField(null=True)
    subdistrict = models.CharField(null=True,max_length=200)
    district = models.CharField(null=True,max_length=200)
    state = models.CharField(null=True,max_length=200)
    def __str__(self):
        return self.user.username

class Order(models.Model):
    sts = (
        ("PENDING","PENDING"),
        ("CANCEL","CANCEL"),
        ("SHIPPING","SHIPPING"),
        ("SHIPED","SHIPED"),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    total = models.IntegerField(null=True,default=0)
    orderdate = models.DateTimeField(auto_now_add=True)
    shipdate = models.DateField()
    status = models.CharField(choices=sts,max_length=200,null=True,blank=True)

    def __str__(self):
        return self.user.username+' '+str(self.total)

class OrderItem(models.Model):
    
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    total = models.IntegerField(null=True,default=0)
    quantity = models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.order.user.username+' '+self.product.title+' '+self.order.status
