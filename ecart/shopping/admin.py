from django.contrib import admin

# Register your models here.
from .models import Task, Contact, Product, Lead, Room, Message

admin.site.register(Room)
admin.site.register(Message)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'attachment', 'title', 'subject', 'related_to', 'deadline', 'status', 'description', 'addedby', )
admin.site.register(Task, TaskAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', "user_image", "full_name", "user_email", "user_phone", "user_position", "company_name", "company_location", "addedby", )
admin.site.register(Contact, ContactAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', "product_image", "product_name", "product_category", "height", "width", "product_weight", "product_color", "product_description", "product_price", "product_manufacture", "expirydate", "manufacture_price", "product_code", "product_warranty", "query_contact", "product_gurantee", "query_email", "addedby", )
admin.site.register(Product, ProductAdmin)

class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', "company_name", "website", "email", "phone", "contact_person", "country", "state", "city", "czip", "title", "status", "source", "assigned_to", "addedby", )
admin.site.register(Lead, LeadAdmin)