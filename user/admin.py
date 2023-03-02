from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor,Patient,User,Blog
# Register your models here.
admin.site.register(Doctor)
admin.site.register(User,UserAdmin)
admin.site.register(Patient)
admin.site.register(Blog)

