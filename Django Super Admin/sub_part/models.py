from django.db import models

# Create your models here.

class couponcodes(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    discount = models.IntegerField()
    limit = models.IntegerField()
    used = models.IntegerField()
    def __str__(self):
        return self.name

class orderslists(models.Model):
    order_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    plan_name = models.CharField(max_length=100)
    price = models.IntegerField()
    status = models.CharField(max_length=100)
    date = models.DateTimeField()
    def __str__(self):
        return self.name

class ownerslists(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    total_users=models.IntegerField()
    plan_name = models.CharField(max_length=100)
    price = models.IntegerField()
    status = models.CharField(max_length=100)
    date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    def __str__(self):
        return self.name

class planlists(models.Model):
    colour = models.CharField(max_length=100)
    price = models.IntegerField()
    name = models.CharField(max_length=100)
    users=models.IntegerField()
    customers=models.IntegerField()
    vendors=models.IntegerField()
    def __str__(self):
        return self.name

class todolists(models.Model):
    sentense=models.CharField(max_length=100)
    def __str__(self):
        return self.sentense