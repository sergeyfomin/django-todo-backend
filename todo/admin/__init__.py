from django.contrib import admin
from django.contrib.auth.models import Group
from todo.admin.user import UserAdmin
from todo.admin.todo import TodoAdmin
from todo.models import User, Todo


admin.site.register(User, UserAdmin)
admin.site.register(Todo, TodoAdmin)

admin.site.unregister(Group)
