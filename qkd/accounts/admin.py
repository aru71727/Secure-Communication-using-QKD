from django.contrib import admin
from.models import secret_keys,Profile,Messages

# Register your models here.

admin.site.register(secret_keys)
admin.site.register(Profile)
admin.site.register(Messages)
