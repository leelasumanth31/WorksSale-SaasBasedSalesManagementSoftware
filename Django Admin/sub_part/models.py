from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.

class todolists(models.Model):
    sentense=models.CharField(max_length=100)
    def __str__(self):
        return self.sentense

class userslists(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    user_role = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class roleslists(models.Model):
    role = models.CharField(max_length=100)
    Profile_box= models.CharField(max_length=200)
    Vendor_box= models.CharField(max_length=200)
    Customer_box= models.CharField(max_length=200)
    user_box= models.CharField(max_length=200)
    roles_list = (
        ('edit hello','edit hello'),
        ('edit bolo','edit bolo'),
    )
    title=MultiSelectField(choices= roles_list)
    def __str__(self):
        return self.role

class customerlists(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    # phone number is used on cusomer analysis page
    phone_number = models.IntegerField()
    date = models.DateTimeField()
    # these fields should not be given by user this will be handled in views assigned zero they will be used in customer analysis page
    total_sales = models.IntegerField()
    total = models.IntegerField()
    def __str__(self):
        return self.name

class vendorlists(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    # phone number is used on cusomer analysis page
    phone_number = models.IntegerField()
    date = models.DateTimeField()
    # these fields should not be given by user this will be handled in views assigned zero they will be used in customer analysis page
    total_sales = models.IntegerField()
    total = models.IntegerField()
    def __str__(self):
        return self.name

class productslists(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    # these fields should not be given by user they are assgned to default in view.productslist
    stock = models.IntegerField()
    def __str__(self):
        return self.name

class categorieslists(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class taxlists(models.Model):
    tax_percentage = models.IntegerField()
    is_default = models.BooleanField(default=False)
    def __str__(self):
        return str(self.tax_percentage)

class saleslists(models.Model):
    invoice_id = models.CharField(max_length=100)
    date = models.DateTimeField()
    sold = (
        ('Walk in Customer','Walk in Customer'),
        ('Vendor','vendor'),
    )
    sold_to = models.CharField(max_length = 100, choices = sold)
    items_sold = models.IntegerField()
    total = models.IntegerField()
    payment = (
        ('Success','Success'),
        ('Pending','Pending'),
    )
    payment_status = models.CharField(max_length = 100, choices = payment)
    # name(product name) is used in stock_analysis page 
    # it is used in views.stock_analysis to compare product names
    name = models.CharField(max_length=100)
    # customer_name is used in views.customer_analysis page to compare customer names
    customer_name = models.CharField(max_length=100)
    # these three are used for tax analysis calculation 
    tax=models.IntegerField()
    # these fields should not be given by user they are assgned to default in view.tax_report
    tax_amount=models.IntegerField()
    grand_total=models.IntegerField()
    def __str__(self):
        return self.invoice_id

class stock_analysislists(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    def __str__(self):
        return self.name

class customer_analysislists(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    email = models.EmailField()
    total_sales = models.IntegerField()
    total = models.IntegerField()
    def __str__(self):
        return self.name

class tax_reportslists(models.Model):
    reference_no = models.CharField(max_length=100)
    date = models.DateTimeField()
    sold = (
        ('Walk in Customer','Walk in Customer'),
        ('Vendor','vendor'),
    )
    vendor = models.CharField(max_length = 100, choices = sold)
    product_tax = models.IntegerField()
    grand_total = models.IntegerField()
    def __str__(self):
        return self.reference_no

class expenseslists(models.Model):
    branch = models.CharField(max_length=100)
    amount = models.IntegerField()
    expense_category = models.CharField(max_length=100)
    expense_date = models.DateTimeField()
    def __str__(self):
        return self.branch

class exp_categorieslists(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name