# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User

# class CustomUserAdmin(BaseUserAdmin):
#     list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'country', 'is_staff')
    
#     # Добавляем кастомные поля в форму редактирования
#     fieldsets = BaseUserAdmin.fieldsets + (
#         ('Дополнительная информация', {'fields': ('phone_number', 'country', 'photo')}),
#     )
    
#     # Добавляем поля в форму создания нового пользователя
#     add_fieldsets = BaseUserAdmin.add_fieldsets + (
#         ('Дополнительная информация', {
#             'classes': ('wide',),
#             'fields': ('email', 'phone_number', 'country', 'photo'),
#         }),
#     )
    
#     search_fields = ('email', 'username', 'first_name', 'last_name')
#     ordering = ('email',)

# # Регистрируем модель User с нашим кастомным админ-классом
# admin.site.register(User, CustomUserAdmin)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "photo",
    )
    search_fields = ("first_name", "last_name", "email", "phone_number", "photo")