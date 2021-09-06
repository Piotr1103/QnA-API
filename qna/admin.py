from django.contrib import admin
from qna.models import users

# Register your models here.
class usersAdmin(admin.ModelAdmin):
    list_display = ('uid','question')

admin.site.register(users,usersAdmin)