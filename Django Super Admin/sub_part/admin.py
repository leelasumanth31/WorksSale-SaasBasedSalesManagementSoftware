from django.contrib import admin
from .models import couponcodes,orderslists,ownerslists,planlists,todolists
# Register your models here.
admin.site.register(couponcodes)
admin.site.register(orderslists)
admin.site.register(ownerslists)
admin.site.register(planlists)
admin.site.register(todolists)
