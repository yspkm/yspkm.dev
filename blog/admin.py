from django.contrib import admin

# Register your models here.
from .models import Post, Category, Tag

admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    # name 입력시 자동으로 slug 생성
    prepopulated_fields = {'slug': ('name', )}
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)