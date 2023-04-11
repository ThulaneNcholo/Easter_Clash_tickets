from django.contrib import admin
from .models import TicketModel

# Register your models here.
class TicketModelAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_number','first_name','last_name','phone','email','date_created'
    )

admin.site.register(TicketModel,TicketModelAdmin)
