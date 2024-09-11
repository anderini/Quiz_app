from django.contrib import admin
from .models.user import User
from .models.categories import categories
# Register your models here.
admin.site.register(User)
admin.site.register(categories)