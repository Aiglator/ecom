from django.contrib import admin
from .models import Category, Product

class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'date_added')

class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image', 'category', 'date_added')  # Ajout de description et image
    list_filter = ('category', 'date_added')  # Filtres dans l'interface admin
    search_fields = ('name', 'description')  # Recherche par nom ou description

admin.site.register(Category, AdminCategory)
admin.site.register(Product, AdminProduct)
