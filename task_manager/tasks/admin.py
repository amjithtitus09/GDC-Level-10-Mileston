from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from task_manager.tasks.models import Task, History

admin.sites.site.register(Task)
admin.sites.site.register(History)
