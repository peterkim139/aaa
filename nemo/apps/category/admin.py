from django.contrib import admin
from .models import Category,SubCategory,Params

class CategoryAdmin(admin.ModelAdmin):

    readonly_fields = ['created','modified']
    search_fields = ['name']


class SubCategoryAdmin(admin.ModelAdmin):

    readonly_fields = ['created','modified']
    search_fields = ['name']

class ParamsAdmin(admin.ModelAdmin):

    readonly_fields = ['created','modified']
    search_fields = ['name','price','description']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Params, ParamsAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)