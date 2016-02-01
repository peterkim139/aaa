from django.contrib import admin
from .models import Category,SubCategory,Params,Properties,Porperty_values

class CategoryAdmin(admin.ModelAdmin):

    readonly_fields = ['created','modified']
    search_fields = ['name']


class SubCategoryAdmin(admin.ModelAdmin):

    readonly_fields = ['created','modified']
    search_fields = ['name']

class ParamsAdmin(admin.ModelAdmin):

    readonly_fields = ['created','modified']
    search_fields = ['name','price','description']

class PropertiesAdmin(admin.ModelAdmin):

    readonly_fields = ['created','modified']
    search_fields = ['property_name','property_type']

class ValuesAdmin(admin.ModelAdmin):
    readonly_fields = ['created','modified']
    
admin.site.register(Porperty_values,ValuesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Params, ParamsAdmin)
admin.site.register(Properties, PropertiesAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)