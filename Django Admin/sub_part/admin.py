from django.contrib import admin
from .models import userslists,roleslists,customerlists,vendorlists,productslists,categorieslists,taxlists,saleslists,stock_analysislists,customer_analysislists,tax_reportslists,expenseslists,exp_categorieslists,todolists

# Register your models here.
admin.site.register(todolists)
admin.site.register(userslists)
admin.site.register(roleslists)
admin.site.register(customerlists)
admin.site.register(vendorlists)
admin.site.register(productslists)
admin.site.register(categorieslists)
admin.site.register(taxlists)
admin.site.register(saleslists)
admin.site.register(stock_analysislists)
admin.site.register(customer_analysislists)
admin.site.register(tax_reportslists)
admin.site.register(expenseslists)
admin.site.register(exp_categorieslists)


