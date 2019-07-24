from django.contrib import admin
from user.models import User
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
                    "id",
                    "full_name",
                    "email",
                    "username",
                    "avatar",
                    "verified_email"
                  ]
