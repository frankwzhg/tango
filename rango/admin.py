from django.contrib import admin
from rango.models import Category, Page
# Register your models here.

# admin.site.register(Category)

# admin.site.register(PageAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'Category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    perpopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
