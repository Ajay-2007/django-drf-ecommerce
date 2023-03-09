from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Brand, Category, Product, ProductLine, ProductImage, AttributeValue, Attribute


# class ProductLineInline(admin.TabularInline):
#     model = ProductLine


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     # in addition to all the information that the product table includes let's add a new section
#     # which is inline
#     inlines = [ProductLineInline]


# # admin.site.register(Product) # we don't wanna register it twice
# admin.site.register(Category)
# admin.site.register(Brand)
# admin.site.register(ProductLine)

class EditLinkInline(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change", args=[instance.pk],
        )
        if instance.pk:
            link = mark_safe('<a href="{u}">edit</a>'.format(u=url))
            return link
        else:
            return ""

class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductLineInline(EditLinkInline, admin.TabularInline):
    model = ProductLine
    # to access readonly field edit, we have to inherit from EditLinkInline
    readonly_fields = ("edit",) # reference to our edit function above


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductLineInline,
    ]


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue.product_line_attribute_value.through # in order to get through this table we have to specify it to get through that related_name attribute value table


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        AttributeValueInline,
    ]

admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Attribute)
admin.site.register(AttributeValue)