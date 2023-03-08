from django.contrib import admin

from .models import Brand, Category, Product, ProductLine


class ProductLineInline(admin.TabularInline):
    model = ProductLine


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # in addition to all the information that the product table includes let's add a new section
    # which is inline
    inlines = [ProductLineInline]


# admin.site.register(Product) # we don't wanna register it twice
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductLine)